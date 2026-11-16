---
title: What is engine parallelism?
short: Engine parallelism
---

**Engine parallelism** means overlapping work on separate
[NeuronCore](/neuron-glossary/device-hardware/neuroncore) engines. Each engine
has its own instruction stream. A matmul can run while another engine
processes a result from a previous tile, provided the two operations have
independent data to work on.

Here are the compute engines on
[NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3).

| Engine | Peak or configuration | Work |
|---|---|---|
| [Tensor](/neuron-glossary/device-hardware/tensor-engine) | 79 BF16 TFLOPS | matmul, convolution |
| [Vector](/neuron-glossary/device-hardware/vector-engine) | 1.0 FP32 TFLOPS | reductions, normalization |
| [Scalar](/neuron-glossary/device-hardware/scalar-engine) | 1.2 FP32 TFLOPS | activations, `exp` |
| [GpSimd](/neuron-glossary/device-hardware/gpsimd-engine) | 8 × 512-bit | general-purpose SIMD operations |

Plus the [Sync Engine](/neuron-glossary/device-hardware/sync-engine) and
[DMA engines](/neuron-glossary/device-hardware/dma-engine), which also run
concurrently.

## Overlapping tiles

In a well-pipelined matmul chain, at any instant:

- The **Tensor Engine** computes tile `n` into
  [PSUM](/neuron-glossary/device-hardware/psum).
- The **Vector or Scalar Engine** drains tile `n-1` from PSUM to
  [SBUF](/neuron-glossary/device-hardware/sbuf), applying the activation on
  the way.
- **DMA engines** fetch tile `n+1` from
  [HBM](/neuron-glossary/device-hardware/hbm).

Keeping several tiles in flight can hide the cost of loading inputs and
copying completed results. Each stage still needs enough buffer space and
memory bandwidth to keep pace.

![In steady state the DMA engines, Tensor Engine, and Vector/Scalar engines are each working on a different tile.](themed-image://engine-pipeline.svg)

## Synchronization

The [compiler](/neuron-glossary/host-software/neuronx-cc) inserts
hardware synchronization based on the dependencies it sees. When every
step needs the full result of the previous one, the engines have to wait.
Working in tiles can let one engine process tile `n-1` as another
computes tile `n`.

## What limits it

Some engine pairs contend for memory ports, and the rules changed between
generations:

| Restriction | [v2](/neuron-glossary/device-hardware/neuroncore-v2) | [v3](/neuron-glossary/device-hardware/neuroncore-v3) |
|---|---|---|
| Vector + GpSimd on [SBUF](/neuron-glossary/device-hardware/sbuf) | serialized | can overlap |
| Vector + Scalar on [PSUM](/neuron-glossary/device-hardware/psum) | serialized | can overlap on different banks |

The Vector Engine's performance mode also shares a memory bus with
[GpSimd](/neuron-glossary/device-hardware/gpsimd-engine). Hardware arbitrates
when they both request it.
[Trainium2 NKI architecture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium2_arch.html#data-movement-updates)

[Neuron Explorer](/neuron-glossary/host-software/neuron-explorer) shows a
timeline per engine. Use it to see which work overlaps and where an engine
sits idle. A core-level utilization figure from
[`neuron-top`](/neuron-glossary/host-software/neuron-top) cannot show that.
