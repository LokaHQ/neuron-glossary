---
title: What is a Trn2 UltraServer?
short: Trn2 UltraServer
---

A **Trn2 UltraServer** is four `trn2u.48xlarge`
[instances](/neuron-glossary/device-hardware/trn2) joined by
[NeuronLink-v3](/neuron-glossary/device-hardware/neuronlink). Each of its
**64 chips** can address the
[HBM](/neuron-glossary/device-hardware/hbm) on the other chips, giving a
combined **6,144 GiB** of device memory.

| Specification | One Trn2 48xlarge | Trn2 UltraServer |
|---|---|---|
| [Trainium2](/neuron-glossary/device-hardware/trainium2) chips | 16 | 64 |
| vCPUs | 192 | 768 |
| Host memory | 2,048 GiB | 8,192 GiB |
| Device memory | 1,536 GiB | 6,144 GiB |
| Aggregate device memory bandwidth | 46.4 TB/s | 185.6 TB/s |
| FP8 PFLOPS | 20.8 | 83.2 |
| BF16 PFLOPS | 10.7 | 42.8 |

## How the chips connect

Each instance connects its 16 chips in a **4×4 grid with wrap-around links**,
called a torus. Chips at the same position in the four grids form a
**ring** across the instances. AWS lists
1,024 GiB/s of NeuronLink bandwidth per chip within an instance and 256 GiB/s
per chip between instances of the same UltraServer. That 4× difference can
favor keeping communication-heavy
[tensor parallelism](/neuron-glossary/perf/tensor-parallelism) within each
instance and placing
[pipeline stages](/neuron-glossary/perf/pipeline-parallelism) across them.
[Source: AWS Neuron Trn2 architecture](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trn2-arch.html)

NeuronLink carries device-to-device traffic within the 64-chip UltraServer.
[EFA](/neuron-glossary/device-hardware/efa) provides network transport between
UltraServers and for workflows that use host networking.
[Trn3 UltraServers](/neuron-glossary/device-hardware/trn3-ultraserver)
use a switched fabric and have 64-chip and 144-chip configurations.
