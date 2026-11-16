---
title: What is a PSUM bank conflict?
short: Bank conflict
abbr:
---

A **PSUM bank conflict** occurs when two engines try to access the same
bank of [partial-sum memory](/neuron-glossary/device-hardware/psum)
at the same time and the accesses have to take turns.

On v2 through v4, PSUM holds 2 MiB across 128 partitions. Each partition
contains eight banks of 2 KiB each. A bank holds 512 FP32 values.

![PSUM banks per partition. A matmul writes one bank on v3 and can span all eight banks on v4.](themed-image://psum-banks.svg)

## Tile width by generation

On [NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3), one
`nc_matmul` writes one PSUM bank per partition, giving a moving free-axis limit
of **512 FP32 elements**. On
[NeuronCore-v4](/neuron-glossary/device-hardware/neuroncore-v4), one
destination can span all eight banks. The moving limit becomes **4,096 with
FP32 output** or **8,192 with BF16 output**. The Tensor Engine still uses FP32
for internal accumulation.
[NKI `nc_matmul` reference](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/api/generated/nki.isa.nc_matmul.html)

## The conflict itself

On [NeuronCore-v2](/neuron-glossary/device-hardware/neuroncore-v2), the
[Vector](/neuron-glossary/device-hardware/vector-engine) and
[Scalar](/neuron-glossary/device-hardware/scalar-engine) engines take turns
accessing PSUM. On v3 they can access separate banks at full bandwidth
in parallel. If both request bank 3 at the same time, one waits.
[Trainium2 NKI architecture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium2_arch.html#data-movement-updates)

## Banks and overlap

On v3, separate banks allow the Tensor Engine to accumulate one output tile
while another engine copies a completed tile to
[SBUF](/neuron-glossary/device-hardware/sbuf). On v4 a wider output can
consume several banks, leaving less space for other accumulation groups.
[Little's Law](/neuron-glossary/perf/littles-law) explains why enough
independent work has to be available to use that overlap.

A [GPU shared-memory bank conflict](https://modal.com/gpu-glossary/perf/bank-conflict)
also serializes accesses. There the contention is among threads in a warp.
The v3 example here is contention between two engines.
