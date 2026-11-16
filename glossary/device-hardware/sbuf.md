---
title: What is SBUF?
short: State Buffer
abbr: SBUF
---

**SBUF**, the **State Buffer**, is the main on-chip working memory in a
[NeuronCore](/neuron-glossary/device-hardware/neuroncore). The compiler or
kernel loads data into SBUF from device memory so the compute engines can use
it. Like GPU shared memory, the program controls what goes into it and when.

## Partitions and capacity

SBUF has **128 partitions**, each a region of memory. The partitions line up
with the 128 rows of the
[systolic array](/neuron-glossary/device-hardware/systolic-array) in the
[Tensor Engine](/neuron-glossary/device-hardware/tensor-engine).

| Core | Total SBUF | Per partition |
|---|---|---|
| [NeuronCore-v2](/neuron-glossary/device-hardware/neuroncore-v2) | 24 MiB | 192 KiB |
| [NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3) | 28 MiB | 224 KiB |
| [NeuronCore-v4](/neuron-glossary/device-hardware/neuroncore-v4) | 32 MiB | — |

Per chip that is 48 MiB on [Trainium](/neuron-glossary/device-hardware/trainium),
224 MiB on [Trainium2](/neuron-glossary/device-hardware/trainium2), and
256 MiB on [Trainium3](/neuron-glossary/device-hardware/trainium3).

## Access rules

- The Vector, Scalar and GpSimd engines can read and write SBUF.
- The [Tensor Engine](/neuron-glossary/device-hardware/tensor-engine)
  reads its inputs **only** from SBUF, and writes its outputs **only** to
  [PSUM](/neuron-glossary/device-hardware/psum).
- Data moves between SBUF and [HBM](/neuron-glossary/device-hardware/hbm)
  by [DMA](/neuron-glossary/device-hardware/dma-engine) only.
- Data moves between SBUF and PSUM by compute-engine instructions, not DMA.

Reusing data in SBUF reduces the bytes read from HBM and raises
[arithmetic intensity](/neuron-glossary/perf/arithmetic-intensity).

## Who moves data

An [NKI](/neuron-glossary/device-software/nki) kernel or the
[Neuron compiler](/neuron-glossary/host-software/neuronx-cc) schedules
transfers into and out of SBUF. Keeping data there for reuse depends on the
schedule and available capacity.
See [software-managed memory](/neuron-glossary/device-software/software-managed-memory).

If the live data in a kernel exceeds SBUF capacity, the compiler inserts spills
and refills to [HBM](/neuron-glossary/device-hardware/hbm). This is
called [spilling](/neuron-glossary/perf/spilling) and adds HBM traffic.
[Tiling](/neuron-glossary/device-software/tiling) helps keep the working set
small enough to fit.

## Layouts

On [Trainium](/neuron-glossary/device-hardware/trainium), SBUF was
row-major only. [Trainium2](/neuron-glossary/device-hardware/trainium2)
added `Col-major-2B` and `Col-major-4B` layouts, which removes some transposes
that previously had to be done explicitly.

[NeuronCore-v4](/neuron-glossary/device-hardware/neuroncore-v4) adds
near-memory accumulation: DMA engines can do a read-add-write into existing
SBUF contents in a single transfer. AWS documents the hardware feature
without an `nki.isa` API in Neuron 2.33.1.
[Trainium3 NKI architecture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium3_arch.html#sbuf-read-add-write)
