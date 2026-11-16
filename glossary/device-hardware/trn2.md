---
title: What is a Trn2 instance?
short: Trn2
---

**Trn2** is the EC2 instance family powered by
[Trainium2](/neuron-glossary/device-hardware/trainium2). It supports training,
inference and [NKI](/neuron-glossary/device-software/nki) kernel development.

| Specification | `trn2.3xlarge` | `trn2.48xlarge` / `trn2u.48xlarge` | [Trn2 UltraServer](/neuron-glossary/device-hardware/trn2-ultraserver) |
|---|---|---|---|
| Trainium2 chips | 1 | 16 | 64 |
| vCPUs | 12 | 192 | 768 |
| Host memory | 128 GiB | 2,048 GiB | 8,192 GiB |
| Device memory | 96 GiB | 1,536 GiB | 6,144 GiB |
| Device memory bandwidth | 2.9 TB/s | 46.4 TB/s | 185.6 TB/s |
| FP8 PFLOPS | 1.3 | 20.8 | 83.2 |
| FP16/BF16/TF32 PFLOPS | 0.67 | 10.7 | 42.8 |
| Sparse PFLOPS | 2.6 | 41 | 164 |
| FP32 PFLOPS | 0.18 | 2.9 | 11.6 |
| Intra-instance NeuronLink-v3 per chip | — | 1,024 GiB/s | 1,024 GiB/s |
| NeuronLink-v3 between members of one UltraServer, per chip | — | — | 256 GiB/s |

The single-chip size has 96 GiB for development, inference or fine-tuning
that fits on one chip. The 16-chip sizes link chips in a 4×4 grid with
wrap-around connections. This is a **torus**. Each chip can address all
1,536 GiB of [HBM](/neuron-glossary/device-hardware/hbm) through
[NeuronLink-v3](/neuron-glossary/device-hardware/neuronlink).
A `trn2.48xlarge` runs on its own. Four `trn2u.48xlarge` instances join
over NeuronLink-v3 to make a 64-chip UltraServer.
[Source: AWS Neuron Trn2 architecture](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trn2-arch.html)

![Trn2 NeuronLink-v3 topology. A 4×4 torus within each 16-chip instance and rings joining matching chip positions across four UltraServer instances.](themed-image://trn2-topology.svg)

## Physical and logical cores

A 48xlarge has **128 physical cores** (16 chips × 8
[NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3) cores).
The default [Logical NeuronCore configuration](/neuron-glossary/device-software/logical-neuroncore)
for model workloads is `LNC=2`, so software sees **64 logical cores**,
four per chip. Use the logical count and the model's sharding constraints when
choosing a [tensor-parallel](/neuron-glossary/perf/tensor-parallelism) degree.

## Differences between AWS specifications

The EC2 instance-type table lists 512 GiB per Trainium2 chip. The Neuron
architecture gives 96 GiB per chip and 1,536 GiB per 16-chip instance,
which the table above uses. The EC2 Trn2 product page likewise shows 96 GB
for the one-chip size and 1.5 TB for the 16-chip sizes, using different units.

For `trn2.3xlarge`, the Neuron architecture says EFA is unavailable. The
EC2 network specification and EFA support list both show EFA support, and
the EC2 network table gives 200 Gbps of network bandwidth. EC2 lists
3,200 Gbps of EFAv3 per 48xlarge instance. The Neuron architecture table
labels that value in GB/s, while the EC2 product page gives 3.2 Tbps.
[AWS Neuron Trn2 architecture](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trn2-arch.html),
[EC2 instance-type specifications](https://docs.aws.amazon.com/ec2/latest/instancetypes/ac.html),
[EC2 EFA support](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/efa.html),
[EC2 Trn2 product details](https://aws.amazon.com/ec2/instance-types/trn2/)
