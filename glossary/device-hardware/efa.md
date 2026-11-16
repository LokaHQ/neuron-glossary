---
title: What is EFA?
short: Elastic Fabric Adapter
abbr: EFA
---

**EFA**, the **Elastic Fabric Adapter**, is AWS's high-performance EC2 network
interface. On supported Neuron instances it carries
[collective communication](/neuron-glossary/device-hardware/collective-communication-engine)
across [NeuronLink](/neuron-glossary/device-hardware/neuronlink) domains,
including between standalone instances or between UltraServers. With EFA's
OS bypass, a userspace application can send and receive data through the
Libfabric networking library without going through the operating system's
network stack.
[AWS EC2 EFA documentation](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/efa.html)

| Platform | EFA bandwidth and scope |
|---|---|
| [Inf1](/neuron-glossary/device-hardware/inf1) | 100 Gbps on `inf1.24xlarge` only |
| [Inf2](/neuron-glossary/device-hardware/inf2) | Unsupported |
| [Trn1](/neuron-glossary/device-hardware/trn1) | EFAv2, 800 Gbps on `trn1.32xlarge` and 1,600 Gbps on `trn1n.32xlarge` |
| [Trn2](/neuron-glossary/device-hardware/trn2) | EFAv3, 3,200 Gbps per 48xlarge instance |
| [Trn3 UltraServer](/neuron-glossary/device-hardware/trn3-ultraserver) | 12,800 Gbps aggregate on Gen1 and 57,600 Gbps aggregate on Gen2 |

[EC2 network specifications](https://docs.aws.amazon.com/ec2/latest/instancetypes/ac.html),
[EC2 Trn1 product details](https://aws.amazon.com/ec2/instance-types/trn1/),
[EC2 Trn2 product details](https://aws.amazon.com/ec2/instance-types/trn2/),
[AWS Neuron Trn3 specifications](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trn3-arch.html#trn3-gen1-gen2-ultraserver-specifications)

For the one-chip `trn2.3xlarge`, EC2 lists EFA support and 200 Gbps of network
bandwidth. The [Trn2 architecture entry](/neuron-glossary/device-hardware/trn2)
explains where the Neuron guide differs.

## Bandwidth in perspective

On a standalone Trn2 48xlarge, 3,200 Gbps is 400 GB/s for the instance.
If all 16 chips split the bandwidth evenly, that would be 25 GB/s per chip.
Within the instance, NeuronLink-v3 is rated at 1,024 GiB/s per chip. The
figures describe different paths and scopes, but illustrate why frequent
[tensor-parallel](/neuron-glossary/perf/tensor-parallelism) collectives often
stay on NeuronLink. The rate you measure depends on the collective and where
its participants run.

EFA is the scale-out fabric of an
[UltraCluster](/neuron-glossary/device-hardware/ultracluster). To measure
collective bandwidth, use
[`nccom-test`](/neuron-glossary/host-software/nccom-test).
