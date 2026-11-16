---
title: What is NeuronLink?
short: NeuronLink
---

**NeuronLink** is AWS's high-speed connection between Neuron chips. It carries
[collective communication](/neuron-glossary/device-hardware/collective-communication-engine)
and, starting with NeuronLink-v2, makes other chips'
[device memory](/neuron-glossary/device-hardware/hbm) directly addressable
on systems that support memory pooling. The chips connected this way form a
**scale-up domain**.

| Version | Chip | Published bandwidth per chip |
|---|---|---|
| v1 | [Inferentia](/neuron-glossary/device-hardware/inferentia) | 32 GiB/s |
| v2 | [Trainium](/neuron-glossary/device-hardware/trainium), [Inferentia2](/neuron-glossary/device-hardware/inferentia2) | 384 GB/s for Trainium in the chip comparison, 192 GiB/s for multi-chip Inf2 in the instance guide |
| v3 | [Trainium2](/neuron-glossary/device-hardware/trainium2) | 1,280 GB/s in the chip specification |
| v4 | [Trainium3](/neuron-glossary/device-hardware/trainium3) | 2,560 GB/s total across links, both directions |

## Memory pooling and chip connections

| Platform | Scale-up domain | Topology | Directly addressable HBM |
|---|---|---|---|
| [Trn1](/neuron-glossary/device-hardware/trn1) | 16 chips | 2D torus | 512 GiB |
| [Trn2](/neuron-glossary/device-hardware/trn2) | 16 chips | 4×4 2D torus | 1,536 GiB |
| [Trn2 UltraServer](/neuron-glossary/device-hardware/trn2-ultraserver) | 64 chips | Four tori with matching chip positions linked in rings | 6,144 GiB |
| [Trn3 UltraServer](/neuron-glossary/device-hardware/trn3-ultraserver), Gen1 | 64 chips | NeuronSwitch-v1 and direct links | 9,216 GiB |
| Trn3 UltraServer, Gen2 | 144 chips | NeuronSwitch-v1 and direct links | 20,736 GiB |

The connection layout affects where it makes sense to split a model. For a
Trn2 UltraServer, the instance architecture guide labels the rates in GiB/s
and lists four times as much NeuronLink-v3 bandwidth per chip within an
instance as between its instances. On Trn3,
[NeuronSwitch-v1](/neuron-glossary/device-hardware/neuronswitch) routes
DMA traffic within the UltraServer. Within-server, within-rack and cross-rack
paths have different bandwidths.
[Trainium2 chip comparison](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trainium2.html#interconnect),
[Inf2 architecture](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/inf2-arch.html),
[Trn2 architecture](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trn2-arch.html),
[Trn3 architecture](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trn3-arch.html)

![Trn2 bandwidth by scope, with NeuronLink rates per chip and EFAv3 per 48xlarge instance.](themed-image://interconnect.svg)

[EFA](/neuron-glossary/device-hardware/efa) carries traffic beyond the
NeuronLink domain, including between UltraServers and between standalone
instances. See [tensor parallelism](/neuron-glossary/perf/tensor-parallelism)
for the implications of placing a group across those boundaries.
