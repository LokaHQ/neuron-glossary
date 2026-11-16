---
title: What is a Trn1 instance?
short: Trn1
---

**Trn1** is the EC2 family powered by first-generation
[Trainium](/neuron-glossary/device-hardware/trainium) chips. It supports
model training and inference.

| Size | Chips | NeuronCores | NeuronLink-v2 | EFAv2 |
|---|---|---|---|---|
| `trn1.2xlarge` | 1 | 2 | — | — |
| `trn1.32xlarge` | 16 | 32 | 2D torus | 800 Gbps |
| `trn1n.32xlarge` | 16 | 32 | 2D torus | 1,600 Gbps |

The 2xlarge has one chip for workloads that fit within 32 GiB of device
memory. Each 32xlarge has 512 GiB across 16 chips. The chips can address
each other's HBM through
[NeuronLink-v2](/neuron-glossary/device-hardware/neuronlink).
[EFA](/neuron-glossary/device-hardware/efa) carries traffic between instances.
The `trn1n` variant doubles EFA bandwidth for jobs with high inter-node
communication.
[Trn1 architecture](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trn1-arch.html),
[EC2 Trn1 specifications](https://aws.amazon.com/ec2/instance-types/trn1/)

![The 4×4 NeuronLink-v2 torus inside a Trn1 32xlarge. Wrap-around links give every chip four neighbours.](themed-image://torus-topology.svg)

## Software and serving

Trn1 uses [NeuronCore-v2](/neuron-glossary/device-hardware/neuroncore-v2).
Each physical core is individually addressable.
[Logical NeuronCore configuration](/neuron-glossary/device-software/logical-neuroncore)
starts with [Trainium2](/neuron-glossary/device-hardware/trainium2).

For inference, Trn1 supports the PyTorch/XLA-based
[PyTorch NeuronX](/neuron-glossary/host-software/torch-neuronx) inference
path. AWS has kept it on PyTorch 2.9 in maintenance mode for critical fixes
since Neuron 2.31. Native
[TorchNeuron](/neuron-glossary/host-software/torchneuron) or the current
[vLLM Neuron plugin](/neuron-glossary/host-software/vllm-neuron) target
[Trn2](/neuron-glossary/device-hardware/trn2) and
[Trn3](/neuron-glossary/device-hardware/trn3-ultraserver).
[AWS inference maintenance announcement](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/announcements/neuron2.x/announce-maintenance-pytorch-xla-inference.html),
[Neuron 2.33.1 documentation](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/)
