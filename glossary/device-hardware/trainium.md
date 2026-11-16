---
title: What is Trainium?
short: Trainium
---

**Trainium**, also called Trainium1, is AWS's first purpose-built chip for
model training. It is the second Neuron hardware generation and powers the
[Trn1 and Trn1n](/neuron-glossary/device-hardware/trn1) instances.

Each Trainium chip has the following hardware.

- Two [NeuronCore-v2](/neuron-glossary/device-hardware/neuroncore-v2)
  cores, together delivering 380 INT8 TOPS, 190 FP16/BF16/cFP8/TF32 TFLOPS,
  and 47.5 FP32 TFLOPS.
- 32 GiB of [HBM](/neuron-glossary/device-hardware/hbm) at 820 GiB/s.
- 1 TB/s of [DMA](/neuron-glossary/device-hardware/dma-engine) bandwidth,
  with inline memory compression and decompression.
- [NeuronLink-v2](/neuron-glossary/device-hardware/neuronlink), four links
  per chip, for collectives and memory pooling across chips.

Trainium and [Inferentia2](/neuron-glossary/device-hardware/inferentia2)
both use NeuronCore-v2. A full Trn1 instance has 16 chips, four NeuronLink-v2
links per chip, and [EFA](/neuron-glossary/device-hardware/efa) for scaling
across instances.

![A Trainium chip: two NeuronCore-v2 cores, each with four engines, over two HBM stacks.](themed-image://trainium-device.svg)

## What made it a training chip

Three additions in [NeuronCore-v2](/neuron-glossary/device-hardware/neuroncore-v2)
help with training.

- **Stochastic [rounding](/neuron-glossary/device-software/rounding-mode).**
  Round-to-nearest can repeatedly lose small updates to BF16 weights.
  Stochastic rounding chooses between nearby representable values so the update
  is preserved on average. This can enable BF16 training without keeping a
  separate FP32 copy of the weights.
- **Control flow and dynamic shapes**, so a training loop's data-dependent
  branches stay on device.
- **The [GpSimd Engine](/neuron-glossary/device-hardware/gpsimd-engine)**,
  so a novel loss or optimizer can be written as a
  [custom operator](/neuron-glossary/device-software/custom-operators)
  rather than falling back to the host.

On a 16-chip Trn1 instance, NeuronLink-v2 lets any chip directly address
another chip's HBM. EFA lets Trn1 instances communicate across an
[UltraCluster](/neuron-glossary/device-hardware/ultracluster), which AWS
describes as designed to scale to over 100,000 chips.

## Software and newer chips

[Trainium2](/neuron-glossary/device-hardware/trainium2) has three times the
HBM capacity and about 3.5× the BF16 throughput per chip. Current
[TorchNeuron](/neuron-glossary/host-software/torchneuron) and
[vLLM Neuron](/neuron-glossary/host-software/vllm-neuron) target
Trainium2 and [Trainium3](/neuron-glossary/device-hardware/trainium3).
See [Trn1](/neuron-glossary/device-hardware/trn1) for the older serving path.
[AWS Trainium architecture](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trainium.html),
[AWS Trn1 architecture](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trn1-arch.html)
