---
title: What is a NeuronCore?
short: NeuronCore
abbr: NC
---

A **NeuronCore** is the independent compute unit inside a
[Neuron device](/neuron-glossary/device-hardware/neuron-device). It is the
closest thing Neuron has to an NVIDIA
[Streaming Multiprocessor](https://modal.com/gpu-glossary/device-hardware/streaming-multiprocessor)
in the sense that both are compute units within a larger chip.

A NeuronCore combines several engines that specialize in different operations
and share on-chip memory.

- The [Tensor Engine](/neuron-glossary/device-hardware/tensor-engine) multiplies
  matrices on a [systolic array](/neuron-glossary/device-hardware/systolic-array).
- The [Vector Engine](/neuron-glossary/device-hardware/vector-engine) handles
  operations such as sums and normalization that combine multiple values.
- The [Scalar Engine](/neuron-glossary/device-hardware/scalar-engine) handles
  element-wise operations such as applying an activation to each input value.
- The [GpSimd Engine](/neuron-glossary/device-hardware/gpsimd-engine) contains
  programmable C/C++ processors for operations that do not map well to the
  specialized engines. It first appeared in [v2](/neuron-glossary/device-hardware/neuroncore-v2).
- The [Sync Engine](/neuron-glossary/device-hardware/sync-engine) can schedule
  [DMA](/neuron-glossary/device-hardware/dma-engine) transfers independently of
  the compute engines on v2 and later.

![A NeuronCore-v2 or later has four compute engines. The Tensor Engine reads from SBUF and writes to PSUM.](themed-image://neuroncore.svg)

The main working memory on the core is [SBUF](/neuron-glossary/device-hardware/sbuf).
The Tensor Engine reads its inputs from SBUF and writes its results to
[PSUM](/neuron-glossary/device-hardware/psum), a smaller buffer where it can add
successive partial results.

## How engines work together

Each engine has its own **sequencer**, the hardware that fetches, decodes and
issues instructions. That lets the engines run different operations at the
same time. In an [NKI](/neuron-glossary/device-software/nki) kernel, you
choose which engines act on each tile, or block of data.

When one engine needs another engine's result, hardware semaphores enforce
the ordering. The [Neuron compiler](/neuron-glossary/host-software/neuronx-cc)
works out those dependencies and inserts the semaphore operations, including
for hand-written NKI kernels.

For example, the Tensor Engine can multiply one pair of tiles while the Vector
Engine moves a finished result out of PSUM and the DMA engines load the next
tile. See
[engine parallelism](/neuron-glossary/perf/engine-parallelism).

![NeuronCore generations and the compute features each added.](themed-image://neuroncore-generations.svg)

## Generations

| | [v1](/neuron-glossary/device-hardware/neuroncore-v1) | [v2](/neuron-glossary/device-hardware/neuroncore-v2) | [v3](/neuron-glossary/device-hardware/neuroncore-v3) | [v4](/neuron-glossary/device-hardware/neuroncore-v4) |
|---|---|---|---|---|
| In chip | [Inferentia](/neuron-glossary/device-hardware/inferentia) | [Trainium](/neuron-glossary/device-hardware/trainium), [Inferentia2](/neuron-glossary/device-hardware/inferentia2) | [Trainium2](/neuron-glossary/device-hardware/trainium2) | [Trainium3](/neuron-glossary/device-hardware/trainium3) |
| Cores per chip | 4 | 2 | 8 | 8 |
| Compute engines | 3 | 4 | 4 | 4 |
| SBUF | — | 24 MiB | 28 MiB | 32 MiB |
| Tensor Engine BF16 | 16 TFLOPS | 92 TFLOPS | 79 TFLOPS | 79 TFLOPS |

Trainium2 has eight v3 cores per chip. Although each core's published BF16
peak is lower than v2's, the published chip peak rose from 190 TFLOPS on
Trainium to 667 TFLOPS on Trainium2. AWS reports core and chip peaks
separately. Use the figure that matches the scope of your work.

On Trainium2 and Trainium3, a
[Logical NeuronCore](/neuron-glossary/device-software/logical-neuroncore)
configuration can combine the resources of several physical cores into one
unit visible to software.

In AWS's abbreviations, **NC** means NeuronCore.
