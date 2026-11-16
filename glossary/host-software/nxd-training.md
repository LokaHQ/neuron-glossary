---
title: What is NxD Training?
short: NxD Training
abbr: NxDT
---

**NxD Training** (NeuronX Distributed Training, or **NxDT**) is the legacy
PyTorch/XLA library for distributed pretraining and fine-tuning on Trainium.
It builds on [NxD Core](/neuron-glossary/host-software/nxd-core). Older recipes
use YAML to describe how to divide a model or dataset across workers with
[tensor](/neuron-glossary/perf/tensor-parallelism),
[pipeline](/neuron-glossary/perf/pipeline-parallelism), and
[data parallelism](/neuron-glossary/perf/data-parallelism). NxDT also supports
splitting optimizer state with ZeRO-1 and converting checkpoints. The package is
`neuronx-distributed-training`.

## Support and migration

AWS put NxDT and NxD Core training APIs in maintenance in Neuron 2.30 for
critical security fixes. The last SDK release to support the NxDT package
was Neuron 2.31.0, with `neuronx-distributed-training` pinned to `1.7.0`.
Starting in 2.31.0, AWS stopped including NxDT in Neuron AMIs. For an AMI
with NxDT preinstalled, use a 2.30.0 or earlier image.
[Maintenance announcement](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/announcements/neuron2.x/announce-maintenance-nxdt-nxd-core-training.html) · [NxDT release notes](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.32.0/release-notes/components/nxd-training.html) · [Neuron 2.31 changes](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.31.0/about-neuron/whats-new.html)

On Trn2 and Trn3, use [TorchNeuron](/neuron-glossary/host-software/torchneuron)
with standard PyTorch distributed APIs for new PyTorch training. For
pretraining recipes, start with
[TorchTitan Neuron](/neuron-glossary/host-software/torchtitan-neuron).
