---
title: What is PSUM?
short: Partial Sum Buffer
abbr: PSUM
---

**PSUM**, the **Partial Sum Buffer**, is a small on-chip memory in a
[NeuronCore](/neuron-glossary/device-hardware/neuroncore), dedicated to
holding [Tensor Engine](/neuron-glossary/device-hardware/tensor-engine)
matrix multiplication results and partial sums.

It is **2 MiB** on
[NeuronCore-v2](/neuron-glossary/device-hardware/neuroncore-v2),
[v3](/neuron-glossary/device-hardware/neuroncore-v3) and [NeuronCore-v4](/neuron-glossary/device-hardware/neuroncore-v4).
It has 128 partitions of 16 KiB each. Each partition has eight 2 KiB banks.
[Trainium3 NKI architecture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium3_arch.html)

## How it accumulates partial results

In a standard, unpacked matrix multiplication, the Tensor Engine can handle
up to 128 values along the contraction dimension `K`, the axis it sums over.
For `K = 4096`, computing one output tile takes 32 `nc_matmul` calls whose
results add up to the final tile.

The Tensor Engine can add each partial result to the running total in PSUM.
That is **near-memory accumulation**. It saves a separate reduction pass and
avoids copying the partial results through SBUF.

## PSUM banks and matmul tile width

On [NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3), one `nc_matmul` output fits in one bank per partition,
which holds **512 FP32 elements**. On [NeuronCore-v4](/neuron-glossary/device-hardware/neuroncore-v4), one output can span
all eight banks for up to **4,096 FP32** or **8,192 BF16** elements per
partition. A wide output can leave fewer banks available for other tiles.
[NKI `nc_matmul` reference](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/api/generated/nki.isa.nc_matmul.html)

## Getting data back out

The Tensor Engine writes all matmul results to PSUM. The
[Vector](/neuron-glossary/device-hardware/vector-engine) or
[Scalar](/neuron-glossary/device-hardware/scalar-engine) Engine typically
copies a finished result to SBUF so the next matmul can reuse the space.

On [NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3), the
Vector and Scalar engines can access PSUM **in parallel** at full bandwidth, as
long as they do not target the same bank — a restriction on
[v2](/neuron-glossary/device-hardware/neuroncore-v2), where those accesses
had to serialize.

## Orientation

Input streams into the [systolic array](/neuron-glossary/device-hardware/systolic-array)
along one axis and results come out along the other. In
[`stationary.T @ moving`](/neuron-glossary/device-software/stationary-and-moving),
the free dimension of `stationary` becomes the partition dimension of the
PSUM output.

Floating-point matmul accumulates in **FP32 inside the Tensor Engine**. On v4 it can write
a BF16 destination in PSUM. When adding to a BF16 partial sum, it upcasts
the stored value, adds in FP32 and rounds back to BF16 on each write.
The v3 transpose mode also supports FP16/BF16 destinations.
[Trainium3 NKI architecture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium3_arch.html)
