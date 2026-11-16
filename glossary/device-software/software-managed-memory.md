---
title: What is software-managed memory?
short: Software-managed memory
---

Memory on a [NeuronCore](/neuron-glossary/device-hardware/neuroncore) is
**software-managed**. The kernel or
[Neuron Compiler](/neuron-glossary/host-software/neuronx-cc) schedules the
transfers between device memories.
[AWS memory hierarchy guide](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/nki/get-started/about/memory-hierarchy-overview.html)

A CPU or GPU cache can fetch a missing line automatically. NeuronCore
has no such cache between device memories. To compute on data in
[HBM](/neuron-glossary/device-hardware/hbm), the program issues a
[DMA](/neuron-glossary/device-hardware/dma-engine) transfer to
[SBUF](/neuron-glossary/device-hardware/sbuf).

## Consequences

- Estimate
  [arithmetic intensity](/neuron-glossary/perf/arithmetic-intensity) by counting
  the operations and bytes transferred in the schedule. The compiler can insert
  extra transfers for spills, so check a profile when the numbers disagree.
- Work in [tiles](/neuron-glossary/device-software/tiling) to fit the
  available on-chip memory. Keep a tile in SBUF for reuse when possible.
  Issuing another load moves those bytes from HBM again.
- Schedule a DMA transfer for the next tile while the
  [Tensor Engine](/neuron-glossary/device-hardware/tensor-engine) uses the
  current one. See [latency hiding](/neuron-glossary/perf/latency-hiding).

[`neuronx-cc`](/neuron-glossary/host-software/neuronx-cc) encodes the
memory plan in a [NEFF](/neuron-glossary/device-software/neff). In
[TorchNeuron](/neuron-glossary/host-software/torchneuron) eager mode, the
backend compiles or reuses device code for each supported operator as
PyTorch calls it.

![The Trainium2 memory hierarchy, from per-core PSUM and SBUF to per-chip HBM and host memory.](themed-image://memory-hierarchy.svg)

## The hierarchy

| Level | Memory | Managed by | Moved with |
|---|---|---|---|
| On-chip | [PSUM](/neuron-glossary/device-hardware/psum) | program | engine instructions |
| On-chip | [SBUF](/neuron-glossary/device-hardware/sbuf) | program | [DMA](/neuron-glossary/device-hardware/dma-engine) to/from HBM |
| Device | [HBM](/neuron-glossary/device-hardware/hbm) | program | DMA |
| Host | CPU DRAM | framework | PyTorch / JAX |

Compute-engine instructions move tensors between SBUF and PSUM. The
framework transfers tensors between host and device memory before and
after [NKI](/neuron-glossary/device-software/nki) kernels run.

## When you exceed capacity

If live tiles exceed on-chip capacity, the compiler can move them to a
larger memory and reload them when needed. A **spill** from SBUF to HBM adds
a write and a read to the kernel's HBM traffic.
See [spilling](/neuron-glossary/perf/spilling).
