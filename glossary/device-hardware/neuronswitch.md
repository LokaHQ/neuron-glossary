---
title: What is NeuronSwitch?
short: NeuronSwitch
---

**NeuronSwitch-v1** is the switch used in
[Trn3 UltraServers](/neuron-glossary/device-hardware/trn3-ultraserver).
[NeuronLink-v4](/neuron-glossary/device-hardware/neuronlink) carries
chip-to-chip traffic over switched and direct links. Each chip has a range
of addresses in the UltraServer's shared address space. A
[DMA engine](/neuron-glossary/device-hardware/dma-engine) can request a
transfer to another chip by using an address in that chip's range.
Switches along the path forward the request to its destination.

| Trn3 configuration | Connections inside each server | Switches linking servers in each rack |
|---|---|---|
| Gen1, 64 chips | Chips connect in direct pairs | One 32-port switch |
| Gen2, 144 chips | One four-port switch | Two 36-port switches |

Direct NeuronLink-v4 links connect corresponding chips across the two racks
within each UltraServer. Any two chips can reach each other, and the
bandwidth depends on the path between them.
[Source: AWS Neuron Trn3 connectivity](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trn3-arch.html)

NeuronSwitch serves the scale-up domain within one UltraServer. Traffic
between UltraServers uses [EFA](/neuron-glossary/device-hardware/efa).
