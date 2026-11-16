---
title: What is an Inf1 instance?
short: Inf1
---

**Inf1** is the EC2 instance family powered by first-generation
[Inferentia](/neuron-glossary/device-hardware/inferentia) chips. AWS
launched it in 2019 for model inference.

| Size | Chips | vCPUs | Host memory | FP16/BF16 TFLOPS | INT8 TOPS | Device memory | Device bandwidth | [NeuronLink](/neuron-glossary/device-hardware/neuronlink) | EFA |
|---|---|---|---|---|---|---|---|---|---|
| `inf1.xlarge` | 1 | 4 | 8 GiB | 64 | 128 | 8 GiB | 50 GiB/s | — | — |
| `inf1.2xlarge` | 1 | 8 | 16 GiB | 64 | 128 | 8 GiB | 50 GiB/s | — | — |
| `inf1.6xlarge` | 4 | 24 | 48 GiB | 256 | 512 | 32 GiB | 200 GiB/s | 32 GiB/s | — |
| `inf1.24xlarge` | 16 | 96 | 192 GiB | 1,024 | 2,048 | 128 GiB | 800 GiB/s | 32 GiB/s | 100 Gbps |

The smaller sizes have up to 25 Gbps of general network bandwidth. The
Neuron Inf1 table labels that column EFA, but EC2's network table and EFA
support list identify `inf1.24xlarge` as the only Inf1 size with EFA.
[AWS Neuron Inf1 architecture](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/inf1-arch.html),
[EC2 network specifications](https://docs.aws.amazon.com/ec2/latest/instancetypes/ac.html),
[EC2 EFA support](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/efa.html)

Each chip carries four
[NeuronCore-v1](/neuron-glossary/device-hardware/neuroncore-v1) cores, so
a full `inf1.24xlarge` exposes 64 NeuronCores.

Inf1 supports [NeuronCore Pipeline](/neuron-glossary/perf/neuroncore-pipeline)
over [NeuronLink-v1](/neuron-glossary/device-hardware/neuronlink): a model
is split by layer across several cores. The cores pass intermediate results
along the chain and can keep their own weights in on-chip memory when those
weights fit.

## Model fit

AWS's Inf1 examples include convolutional networks such as ResNet-50 and
encoders such as BERT-base. For large language models, each chip's 8 GiB
limits how many weights it can hold, and 50 GiB/s limits how fast it can
read them during [memory-bound](/neuron-glossary/perf/memory-bound) decoding.

The 128 GiB on `inf1.24xlarge` is the sum of 16 separate 8 GiB memories.
Directly addressable memory pooling arrived with
[NeuronLink-v2](/neuron-glossary/device-hardware/neuronlink).

## Software

Inf1 uses the legacy `neuron-cc` compiler and archived framework
integrations, including `torch-neuron` for older PyTorch and
`tensorflow-neuron` for TensorFlow. Modern
[TorchNeuron](/neuron-glossary/host-software/torchneuron),
[PyTorch NeuronX](/neuron-glossary/host-software/torch-neuronx) and
[NKI](/neuron-glossary/device-software/nki) target newer hardware. Moving
an Inf1 model to a newer accelerator requires compiling for the new target
with its supported framework.
[AWS Inf1 installation archive](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/archive/setup/legacy-inf1/index.html),
[Neuron Graph Compiler documentation](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/compiler/about-neuronx-cc.html)
