---
title: What is a DMA engine?
short: DMA engine
---

**Direct memory access (DMA) engines** move data independently of the hardware
that performs computations. On a
[Neuron device](/neuron-glossary/device-hardware/neuron-device) they carry tensors between
[HBM](/neuron-glossary/device-hardware/hbm) and
[SBUF](/neuron-glossary/device-hardware/sbuf), between SBUF and SBUF, and
between chips.

These counts and peak DMA bandwidths are per chip.

| Chip | DMA engines | DMA bandwidth |
|---|---|---|
| [Trainium](/neuron-glossary/device-hardware/trainium) / [Inferentia2](/neuron-glossary/device-hardware/inferentia2) | 32 | 1 TB/s |
| [Trainium2](/neuron-glossary/device-hardware/trainium2) | 128 | 3.5 TB/s |
| [Trainium3](/neuron-glossary/device-hardware/trainium3) | 128 | 4.9 TB/s |

[Trainium3 NKI architecture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium3_arch.html),
[Trainium3 chip architecture](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trainium3.html)

On [Trainium2](/neuron-glossary/device-hardware/trainium2), each
[NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3) is
typically uses **16 DMA engines** in parallel to make use of its SBUF
bandwidth.

DMA transfers run **in parallel with computation**. This is the mechanism
behind [latency hiding](/neuron-glossary/perf/latency-hiding): while the
[Tensor Engine](/neuron-glossary/device-hardware/tensor-engine) works on
tile `n`, DMA engines can fetch tile `n+1`. If the next tile arrives in
time, computation can continue without waiting for the load.

A sequencer starts a transfer with a control instruction. The
[Sync Engine](/neuron-glossary/device-hardware/sync-engine) can issue that
instruction on a separate stream from the compute engines.

## Inline compression

Neuron DMA engines perform **inline memory compression and decompression** as
data moves, from [Trainium](/neuron-glossary/device-hardware/trainium)
and Inferentia2 onward. The benefit depends on how well the data compresses.
[Trainium3](/neuron-glossary/device-hardware/trainium3) also introduces
operations such as adding incoming values to an existing SBUF tensor during
a transfer.

## DMA transpose

From [Trainium2](/neuron-glossary/device-hardware/trainium2), DMA engines
can **swap tensor axes during a transfer** from HBM to SBUF or between
SBUF tensors. This lets a transfer place the axis the
[Tensor Engine](/neuron-glossary/device-hardware/tensor-engine) needs
across the partitions in SBUF.

For example, attention may store keys as `[seqlen, d_head]` in the KV cache.
When the Tensor Engine computes attention scores, it sums over `d_head`.
A [DMA transpose](/neuron-glossary/device-software/dma-transpose) puts that
axis in the SBUF partition dimension during the load.

For Trainium2, AWS reports up to 90% DMA throughput utilization for an
HBM-to-SBUF transpose with suitable access patterns, up to 100% for a plain
copy, and up to 50% for an SBUF-to-SBUF transpose.
[Trainium2 NKI architecture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium2_arch.html#dma-transpose)

## Descriptors

A DMA transfer uses **descriptors** that give the source and destination
addresses, sizes and strides. Neuron can generate them in several ways.

- **Static.** Descriptors generated on the host when the
  [NEFF](/neuron-glossary/device-software/neff) is loaded, and stored in
  HBM.
- **Software DGE.** Generated at runtime by custom kernels on the
  [GpSimd Engine](/neuron-glossary/device-hardware/gpsimd-engine), using
  SBUF for storage.
- **Hardware DGE.** From
  [NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3), a
  dedicated [Descriptor Generation Engine](/neuron-glossary/device-hardware/dge)
  generates them on demand without using the GpSimd Engine or reserving
  descriptor space in HBM or SBUF.

## Ordering

[Trainium](/neuron-glossary/device-hardware/trainium) used
write-after-write DMA barriers.
[Trainium2](/neuron-glossary/device-hardware/trainium2) uses
strong-order-write, which is generally faster, by an amount that depends on
transfer size.

Separately, each of the eight processors in a
[NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3) GpSimd
Engine has its **own** integrated DMA engine — 307 GB/s across all eight —
running in parallel with both GpSimd compute and the main DMA engines.
