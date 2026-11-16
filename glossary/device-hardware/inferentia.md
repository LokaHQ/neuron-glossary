---
title: What is Inferentia?
short: Inferentia
---

**Inferentia** is AWS's first machine learning chip, announced in 2018 and
shipped in 2019. The chip powers the inference-only
[Inf1](/neuron-glossary/device-hardware/inf1) instance family.

Each Inferentia chip holds:

- Four [NeuronCore-v1](/neuron-glossary/device-hardware/neuroncore-v1)
  cores, together delivering 128 INT8 TOPS and 64 FP16/BF16 TFLOPS.
- 8 GiB of DDR device memory at 50 GiB/s. AWS switched to
  [HBM](/neuron-glossary/device-hardware/hbm) in the second generation.
- [NeuronLink-v1](/neuron-glossary/device-hardware/neuronlink), used for
  [NeuronCore Pipeline](/neuron-glossary/perf/neuroncore-pipeline).

![An Inferentia chip with four NeuronCore-v1 cores and DDR device memory.](themed-image://inferentia-device.svg)

Inferentia introduced the Neuron software stack. The first compiler,
`neuron-cc`, compiled the model ahead of time, and the
[Neuron runtime](/neuron-glossary/host-software/neuron-runtime) loaded and ran
it on the chip. Later chips use
[`neuronx-cc`](/neuron-glossary/host-software/neuronx-cc).

AWS's Inf1 examples include convolutional models such as ResNet-50 and
encoders such as BERT-base. A dense 7-billion-parameter model needs about
14 GB for BF16 weights alone, more than a single Inferentia chip's 8 GiB.

The later [Inferentia2](/neuron-glossary/device-hardware/inferentia2) shares
its [NeuronCore-v2](/neuron-glossary/device-hardware/neuroncore-v2) design
with [Trainium](/neuron-glossary/device-hardware/trainium). That generation
added programmable processors for custom operators, device-side control flow,
dynamic shapes and FP8.
[AWS Inferentia architecture](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/inferentia.html)
