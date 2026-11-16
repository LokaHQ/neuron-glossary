---
title: What is an EC2 UltraCluster?
short: UltraCluster
---

An **EC2 UltraCluster** is a group of accelerated EC2 instances connected by
a petabit-scale [EFA](/neuron-glossary/device-hardware/efa) network. For
Trainium, EFA lets jobs run
[collectives](/neuron-glossary/device-hardware/collective-communication-engine)
across multiple standalone instances or UltraServers. Inside each
multi-chip instance or UltraServer, its connected chips can use
[NeuronLink](/neuron-glossary/device-hardware/neuronlink).

| Scale | Example | Fabric |
|---|---|---|
| Within an instance | 16 chips in a [Trn2 48xlarge](/neuron-glossary/device-hardware/trn2) | NeuronLink-v3 torus |
| Within a Trn2 UltraServer | Four hosts, 64 chips | NeuronLink-v3 tori and rings |
| Within a [Trn3 UltraServer](/neuron-glossary/device-hardware/trn3-ultraserver) | Gen1 64 chips or Gen2 144 chips | NeuronLink-v4 and NeuronSwitch-v1 |
| Across scale-up domains in an UltraCluster | Multiple instances or UltraServers | EFA |

AWS describes the Trn1 UltraCluster EFA network as **non-blocking** and
documents a design that scales past 100,000 Trainium chips. Non-blocking
describes the network's ability to carry simultaneous traffic without an
oversubscribed shared link. Each job can use the resources allocated to it.
[AWS Neuron Trn1 architecture](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trn1-arch.html),
[AWS EC2 Trn3 UltraServers](https://aws.amazon.com/ec2/instance-types/trn3/)

Where you place a collective changes which fabric carries it. A group that
communicates on every layer, such as a
[tensor-parallel group](/neuron-glossary/perf/tensor-parallelism), often
benefits from staying within a NeuronLink domain.
