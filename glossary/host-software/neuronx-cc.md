---
title: What is neuronx-cc?
short: Neuron compiler
abbr: neuronx-cc
---

**`neuronx-cc`** is the Neuron Graph Compiler for
[Inf2](/neuron-glossary/device-hardware/inf2),
[Trn1](/neuron-glossary/device-hardware/trn1),
[Trn2](/neuron-glossary/device-hardware/trn2) and
[Trn3](/neuron-glossary/device-hardware/trainium3). It translates a graph of
tensor operations into a [NEFF](/neuron-glossary/device-software/neff) built
for the chosen accelerator,
which the [Neuron Runtime](/neuron-glossary/host-software/neuron-runtime)
loads and executes. `neuron-cc` is the separate legacy compiler for
[Inf1](/neuron-glossary/device-hardware/inf1).

Your framework usually invokes the compiler for you. If you have exported
a graph as an [XLA HLO](/neuron-glossary/host-software/xla) protobuf, you can
compile it directly.

```sh
neuronx-cc compile model.hlo.pb --framework XLA --target trn2 --output model.neff
```

[AWS compiler CLI reference](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/compiler/neuronx-cc/api-reference-guide/index.html)

## What the compiler decides

Neuron's device memory is
[software-managed](/neuron-glossary/device-software/software-managed-memory).
The compiler schedules compute, tiling, [DMA](/neuron-glossary/device-hardware/dma-engine)
transfers, buffer lifetimes, and synchronization. When the compiler sees
several operations together, it can sometimes fuse them and keep intermediate
results in on-chip memory. With native
[TorchNeuron](/neuron-glossary/host-software/torchneuron), the compilation
unit may be an operator in eager mode or a captured graph under `torch.compile`.
The caller's graph and cache determine when a fresh compilation is needed.

## Options worth knowing

- **Precision.** `--auto-cast=none` is the compiler default starting in
  Neuron SDK 2.27. Older versions defaulted to casting FP32 matrix operations
  to BF16. Use `--auto-cast=matmult --auto-cast-type=bf16` to opt into that
  behavior. The framework's own mixed-precision policy is a separate
  setting.
  [Neuron 2.27 compiler release notes](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/release-notes/components/compiler.html#neuron-compiler-2-22-12471-0-neuron-2-27-0-release)
- **Model type and optimization level.** `--model-type` can target
  `transformer` or `unet-inference`. `-O` controls the optimization level.
- **Integer behavior.** `--native-int64=enabled` requests native 64-bit
  execution on Trn2 and later where supported. `--implicit-integer-downcast`
  controls whether operations without a suitable integer datapath can use a
  lossy conversion. Check [data types](/neuron-glossary/device-software/data-types)
  and the CLI reference before relying on defaults.

When graph compilation fails, the framework decides how to handle the
error. [TorchNeuron](/neuron-glossary/host-software/torchneuron) has
different fallback rules for eager operators and compiled graphs.
The [compilation caches](/neuron-glossary/host-software/neuron-persistent-cache)
can reuse a previously compiled executable.
