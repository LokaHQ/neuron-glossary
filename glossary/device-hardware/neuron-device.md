---
title: What is a Neuron device?
short: Neuron device
abbr: ND
---

A **Neuron device** is one AWS-designed machine learning chip. In AWS's own
documentation the word covers both product lines:
[Inferentia](/neuron-glossary/device-hardware/inferentia) chips, which
only run inference, and [Trainium](/neuron-glossary/device-hardware/trainium)
chips, which run both training and inference.

An EC2 instance can contain one or more Neuron devices. Each device has its
own [device memory](/neuron-glossary/device-hardware/hbm) and multiple
[NeuronCores](/neuron-glossary/device-hardware/neuroncore), which perform the
computation. Use [`neuron-ls`](/neuron-glossary/host-software/neuron-ls) to see
the devices and cores available on an instance.

AWS groups the chips by NeuronCore generation.

| Generation | Chip | NeuronCore | Cores per chip | Instance |
|---|---|---|---|---|
| First | [Inferentia](/neuron-glossary/device-hardware/inferentia) | [v1](/neuron-glossary/device-hardware/neuroncore-v1) | 4 | [Inf1](/neuron-glossary/device-hardware/inf1) |
| Second | [Trainium](/neuron-glossary/device-hardware/trainium) and [Inferentia2](/neuron-glossary/device-hardware/inferentia2) | [v2](/neuron-glossary/device-hardware/neuroncore-v2) | 2 | [Trn1](/neuron-glossary/device-hardware/trn1), [Inf2](/neuron-glossary/device-hardware/inf2) |
| Third | [Trainium2](/neuron-glossary/device-hardware/trainium2) | [v3](/neuron-glossary/device-hardware/neuroncore-v3) | 8 | [Trn2](/neuron-glossary/device-hardware/trn2) |
| Fourth | [Trainium3](/neuron-glossary/device-hardware/trainium3) | [v4](/neuron-glossary/device-hardware/neuroncore-v4) | 8 | [Trn3 UltraServer](/neuron-glossary/device-hardware/trn3-ultraserver) |

Trainium and Inferentia2 share the second-generation core design. Both chips
have 32 GiB of high-bandwidth memory (HBM) and a peak BF16 rate of 190 TFLOPS.
Trainium2 is the second chip in the Trainium line and the third Neuron
hardware generation.

Core counts describe how the work is divided within a chip. For example,
first-generation Inferentia has twice as many cores as Trainium, while
Trainium has about three times the peak BF16 performance per chip. Compare
per-chip performance in the format your model uses, along with memory
capacity and bandwidth.

In the SDK and in AWS's abbreviations you will see **ND** for Neuron device and
**NC** for NeuronCore.
