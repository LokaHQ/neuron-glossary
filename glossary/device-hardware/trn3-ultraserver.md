---
title: What is a Trn3 UltraServer?
short: Trn3 UltraServer
---

A **Trn3 UltraServer** joins [Trainium3](/neuron-glossary/device-hardware/trainium3)
chips across servers so they can work together. Gen1 connects **64 chips**
and Gen2 connects **144 chips**, all using the same Trainium3 chip. Both use
[NeuronLink-v4](/neuron-glossary/device-hardware/neuronlink) and
[NeuronSwitch-v1](/neuron-glossary/device-hardware/neuronswitch) to give
each chip access to every other chip's
[HBM](/neuron-glossary/device-hardware/hbm) through device DMA.

| Specification | Gen1 | Gen2 |
|---|---|---|
| Servers × chips per server | 4 × 16 | 36 × 4 |
| Chips per UltraServer | 64 | 144 |
| Host vCPUs | 768 | 3,456 |
| Host memory | 8,192 GiB | 27,648 GiB |
| Device memory | 9,216 GiB | 20,736 GiB |
| Aggregate device memory bandwidth | 313.6 TB/s | 705.6 TB/s |
| Peak MXFP8/MXFP4 | 161.1 PFLOPS | 362.4 PFLOPS |
| Peak FP16/BF16/TF32 | 42.9 PFLOPS | 96.6 PFLOPS |
| Peak FP32 | 11.7 PFLOPS | 26.4 PFLOPS |
| NeuronLink-v4 total per chip, both directions | 2,560 GB/s | 2,560 GB/s |
| Aggregate EFA | 12,800 Gbps | 57,600 Gbps |

[Source: AWS Neuron Trn3 architecture and specifications](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trn3-arch.html#trn3-gen1-gen2-ultraserver-specifications)

## How the chips connect

![Trn3 Gen1 and Gen2 use NeuronLink-v4, NeuronSwitch-v1 and direct links within each UltraServer.](themed-image://trn3-topology.svg)

- **Gen1** has two racks of two servers. Within a server, chips are paired by
  direct links. One 32-port NeuronSwitch-v1 in each rack connects all chips
  from both servers. Direct links connect corresponding chips across racks.
- **Gen2** has two racks of 18 servers. A four-port NeuronSwitch-v1 connects
  the chips inside each server. Two 36-port switches per rack connect the
  servers in that rack. Direct links connect corresponding chips across racks.

The bandwidth depends on which path the data takes. AWS reports the
following totals per chip, summed over both directions.

| NeuronLink-v4 path | Gen1 | Gen2 |
|---|---|---|
| Within a server | 1,024 GB/s | 1,024 GB/s |
| To a rack switch | 1,024 GB/s | 1,280 GB/s |
| Direct cross-rack link | 512 GB/s | 256 GB/s |

[Source: AWS Neuron Trn3 connectivity](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trn3-arch.html)

Traffic **between UltraServers** uses [EFA](/neuron-glossary/device-hardware/efa).
The switched links help with workloads that exchange a lot of data.
In expert parallelism, chips send tokens to the chips running the selected
experts through
[all-to-all collectives](/neuron-glossary/device-software/collectives).
The previous [Trn2 UltraServer](/neuron-glossary/device-hardware/trn2-ultraserver)
connects 64 chips using NeuronLink-v3 tori and rings.
