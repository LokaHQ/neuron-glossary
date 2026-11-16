---
title: What is XLA on Neuron?
short: XLA and HLO
abbr: XLA
---

**XLA** (Accelerated Linear Algebra) is a compiler stack for tensor programs used by
[JAX NeuronX](/neuron-glossary/host-software/jax-neuronx) and the legacy
PyTorch/XLA build of [torch-neuronx](/neuron-glossary/host-software/torch-neuronx).
**HLO** (High Level Optimizer) is how XLA represents a computation before
turning it into device code. **StableHLO** is a related format with a
compatibility contract for exchanging computations between frameworks and
compilers.
[OpenXLA architecture](https://openxla.org/xla/architecture) · [StableHLO overview](https://openxla.org/stablehlo)

| Path | How the graph reaches Neuron |
|---|---|
| Legacy PyTorch/XLA | Traced or lazily accumulated PyTorch operations lower through XLA to HLO. `xm.mark_step()` is a graph boundary in lazy execution. |
| JAX | JAX traces functions such as `jax.jit`; the Neuron PJRT plugin connects the XLA path to Neuron. |
| [Native TorchNeuron](/neuron-glossary/host-software/torchneuron) | PyTorch dispatches eager operators or captures FX graphs under `torch.compile`. The native backend translates those operators or graphs directly into StableHLO. |

All three routes can produce a [NEFF](/neuron-glossary/device-software/neff)
for the [Neuron Runtime](/neuron-glossary/host-software/neuron-runtime). You can
also invoke [`neuronx-cc`](/neuron-glossary/host-software/neuronx-cc) directly on
an exported XLA HLO protobuf; see the
[compiler CLI reference](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/compiler/neuronx-cc/api-reference-guide/index.html).

AWS's announced 2.34 cutoff applies to PyTorch/XLA inference on Trn2 and Trn3.
JAX continues to use PJRT, and native TorchNeuron uses StableHLO as its input
to the Neuron compiler in 2.33.1.
[AWS support announcement](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/announcements/neuron2.x/announce-eos-torch-xla-inference-trn.html) · [TorchNeuron compilation guide](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/torch/compile/about-torch-compile.html)
