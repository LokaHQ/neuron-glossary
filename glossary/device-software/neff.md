---
title: What is a NEFF?
short: Neuron Executable Format
abbr: NEFF
---

A **NEFF** is a file in the Neuron Executable File Format. It holds code that runs
on a [Neuron device](/neuron-glossary/device-hardware/neuron-device). The
[Neuron Compiler](/neuron-glossary/host-software/neuronx-cc) produces it.
The [Neuron Runtime](/neuron-glossary/host-software/neuron-runtime) loads it
into device memory and executes it. It is analogous to a CUDA `cubin`.

A NEFF holds engine instructions and the compiled plan for moving data through
[SBUF](/neuron-glossary/device-hardware/sbuf),
[PSUM](/neuron-glossary/device-hardware/psum) and device memory. Weights can be
embedded or supplied separately, depending on the framework export.
[AWS NEFF generation guide](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/compiler/neuronx-cc/how-to-generate-neff.html)

![Native eager, native compiled and XLA/PJRT paths produce target-specialized NEFFs that the Neuron Runtime loads and executes.](themed-image://compile-flow.svg)

## When compilation happens

The framework chooses when to produce the NEFF and how much work to put in it.

- [TorchNeuron](/neuron-glossary/host-software/torchneuron) can compile a single
  operator in eager mode or a captured graph on first use with `torch.compile`.
- A serving stack such as [vLLM Neuron](/neuron-glossary/host-software/vllm-neuron)
  can compile graphs for shape buckets during warmup or ahead of deployment.
- Legacy `torch_neuronx.trace` produces a TorchScript artifact that embeds the
  NEFF and can be saved for later inference.

The compiled code targets specific hardware and input shapes and types. A
different shape or option can require another compilation. A matching
[compilation cache](/neuron-glossary/host-software/neuron-persistent-cache)
entry can supply the executable without running the compiler again. Compiling
a larger graph lets the compiler plan tiling, data movement and synchronization
across operators. See [software-managed memory](/neuron-glossary/device-software/software-managed-memory)
for what that plan controls.
