---
title: What is the Descriptor Generation Engine?
short: Descriptor Generation Engine
abbr: DGE
---

The **Descriptor Generation Engine** (DGE) is dedicated hardware, introduced in
[NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3), that
generates [DMA](/neuron-glossary/device-hardware/dma-engine) descriptors
on demand. Each NeuronCore-v3 has **two** DGE instances.

A DMA descriptor tells a DMA engine what to move. It records where to read,
where to write, how much data to copy, and how far to step between elements.
A kernel that processes data in tiles can need many descriptors. Before v3,
Neuron generated them in two ways.

- **Static generation.** The host computed every descriptor when loading the
  [NEFF](/neuron-glossary/device-software/neff), and stored them all in
  [HBM](/neuron-glossary/device-hardware/hbm), using space that could
  otherwise hold model parameters or activations.
- **Software DGE.** Descriptors were generated during execution by custom
  kernels running on the
  [GpSimd Engine](/neuron-glossary/device-hardware/gpsimd-engine), stored
  in a slice of [SBUF](/neuron-glossary/device-hardware/sbuf). This saved
  HBM space and kept a compute engine busy calculating addresses.

Hardware DGE generates descriptors as each transfer needs them and leaves
GpSimd free for computation. AWS recommends
using it wherever possible on
[Trainium2](/neuron-glossary/device-hardware/trainium2).

## Programming it

In an [NKI](/neuron-glossary/device-software/nki) kernel, set
`dge_mode` on the transfer instruction.

```python
import nki.isa as nisa

nisa.dma_copy(dst, src, dge_mode=nisa.dge_mode.hwdge)
nisa.dma_transpose(dst=sbuf_dst, src=hbm_src, dge_mode=nisa.dge_mode.hwdge)
```

Hardware DGE transpose has specific tile shape and data type requirements.
[NKI `dma_transpose` reference](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/api/generated/nki.isa.dma_transpose.html)

The [Sync Engine](/neuron-glossary/device-hardware/sync-engine) or
[Scalar Engine](/neuron-glossary/device-hardware/scalar-engine) issues the
command. The compiler can choose the engine, and `nisa.dma_copy` also accepts
an explicit `engine` argument for hardware DGE.
[NKI `dma_copy` reference](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/api/generated/nki.isa.dma_copy.html)

## Performance notes

A DGE-based DMA instruction takes about **600 ns** on
[NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3).

When the Scalar Engine issues it, DGE can run alongside earlier Scalar
Engine compute such as `nisa.activate()`. The descriptor hardware and
the compute pipeline can work independently.

## Limitation

On NeuronCore-v3, indirect DMA operations such as gather and scatter use
software DGE. They take an array of indices to determine which rows to read
or write.
[Trainium2 NKI architecture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium2_arch.html#descriptor-generation-engine-dge)
