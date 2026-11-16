---
title: What is Inferentia2?
short: Inferentia2
---

**Inferentia2** is AWS's second-generation inference chip, powering the
[Inf2](/neuron-glossary/device-hardware/inf2) instance family.

Inferentia2 and [Trainium](/neuron-glossary/device-hardware/trainium) share
the [NeuronCore-v2](/neuron-glossary/device-hardware/neuroncore-v2) design
and have the same published compute and memory specifications. Inferentia2
has two chip-to-chip links, and Trainium has four.

Each Inferentia2 chip holds:

- Two [NeuronCore-v2](/neuron-glossary/device-hardware/neuroncore-v2)
  cores, together delivering 380 INT8 TOPS, 190 FP16/BF16/cFP8/TF32 TFLOPS,
  and 47.5 FP32 TFLOPS.
- 32 GiB of [HBM](/neuron-glossary/device-hardware/hbm) at 820 GiB/s.
- 1 TB/s of [DMA](/neuron-glossary/device-hardware/dma-engine) bandwidth,
  with inline memory compression and decompression.
- [NeuronLink-v2](/neuron-glossary/device-hardware/neuronlink) for
  chip-to-chip collectives.

Compared with the first
[Inferentia](/neuron-glossary/device-hardware/inferentia): 4× the device
memory, 16× the memory bandwidth, and roughly 3× the FP16 throughput. The
faster memory helps during token generation, when the chip repeatedly reads
the model weights.

Because it is a v2 core, it inherits the whole v2 feature set: dynamic shapes,
control flow, programmable
[rounding](/neuron-glossary/device-software/rounding-mode),
[cFP8](/neuron-glossary/device-software/cfp8), and
[custom operators](/neuron-glossary/device-software/custom-operators) on
the [GpSimd Engine](/neuron-glossary/device-hardware/gpsimd-engine).

![Trainium chip for comparison. Inferentia2 shares the two NeuronCore-v2 cores and HBM capacity but has two NeuronLink-v2 links.](themed-image://trainium-device.svg)

## Inf2 and Trn1 instances

| | [Inf2](/neuron-glossary/device-hardware/inf2) | [Trn1](/neuron-glossary/device-hardware/trn1) |
|---|---|---|
| Max chips | 12 | 16 |
| [NeuronLink-v2](/neuron-glossary/device-hardware/neuronlink) per chip | 2 | 4 |
| [EFA](/neuron-glossary/device-hardware/efa) networking | no | yes |
| Smallest size | 1 chip | 1 chip |

Inf2 uses NeuronLink for collectives within one instance. The larger Trn1 sizes
also use [EFA](/neuron-glossary/device-hardware/efa) to carry collectives between
instances. [Trainium2](/neuron-glossary/device-hardware/trainium2) and
[Trainium3](/neuron-glossary/device-hardware/trainium3) support both training
and inference.
[AWS Inferentia2 architecture](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/inferentia2.html),
[AWS Trainium/Inferentia2 NKI architecture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium_inferentia2_arch.html)
