---
title: What is NeuronCore-v1?
short: NeuronCore-v1
---

**NeuronCore-v1** is the first-generation
[NeuronCore](/neuron-glossary/device-hardware/neuroncore), the core inside
the original [Inferentia](/neuron-glossary/device-hardware/inferentia)
chip. Each chip has four v1 cores, so the largest
[Inf1](/neuron-glossary/device-hardware/inf1) instance has 64 cores across
16 chips.

It has **three compute engines**.

- [Tensor Engine](/neuron-glossary/device-hardware/tensor-engine) — 16
  TFLOPS of FP16/BF16, on a
  [systolic array](/neuron-glossary/device-hardware/systolic-array).
  Mixed precision, with FP16/BF16/INT8 inputs and FP32/INT32 outputs.
- [Vector Engine](/neuron-glossary/device-hardware/vector-engine) — 256
  floating-point operations per cycle.
- [Scalar Engine](/neuron-glossary/device-hardware/scalar-engine) — 512
  floating-point operations per cycle.

The programmable [GpSimd Engine](/neuron-glossary/device-hardware/gpsimd-engine)
and its [custom operator](/neuron-glossary/device-software/custom-operators)
support arrived in [v2](/neuron-glossary/device-hardware/neuroncore-v2), along
with device-side control flow, dynamic shapes and programmable
[rounding](/neuron-glossary/device-software/rounding-mode).

Supported data types are FP16, BF16, FP32, INT8, INT16, and INT32. There is no
[FP8](/neuron-glossary/device-software/cfp8) and no
[TF32](/neuron-glossary/device-software/data-types).

The four cores share 8 GiB of DDR device memory with 50 GiB/s of bandwidth.
The later [Trainium](/neuron-glossary/device-hardware/trainium) and
[Inferentia2](/neuron-glossary/device-hardware/inferentia2) chips use HBM.

## Software

Inf1 uses the legacy `torch-neuron` integration and `neuron-cc` compiler.
[NKI](/neuron-glossary/device-software/nki) support starts with v2. For the
frameworks and migration path, see
[Inf1](/neuron-glossary/device-hardware/inf1).
[AWS NeuronCore-v1 architecture](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/neuron-core-v1.html)
