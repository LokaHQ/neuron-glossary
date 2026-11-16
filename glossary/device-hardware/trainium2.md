---
title: What is Trainium2?
short: Trainium2
---

**Trainium2** is AWS's third-generation ML chip. It powers
[Trn2 instances](/neuron-glossary/device-hardware/trn2) and the
[Trn2 UltraServer](/neuron-glossary/device-hardware/trn2-ultraserver).

Each Trainium2 chip has the following hardware.

- **Eight [NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3)
  cores**, together delivering 1,299 FP8 TFLOPS, 667 BF16/FP16/TF32 TFLOPS,
  up to 2,563 sparse TFLOPS (FP8/FP16/BF16/TF32), and 181 FP32 TFLOPS.
- **96 GiB of [HBM](/neuron-glossary/device-hardware/hbm) at 2.9 TB/s**,
  across four stacks.
- **3.5 TB/s of [DMA](/neuron-glossary/device-hardware/dma-engine)
  bandwidth** from 128 DMA engines, with inline compression and decompression.
- **[NeuronLink-v3](/neuron-glossary/device-hardware/neuronlink)**, four
  links giving 1.28 TB/s per chip, and memory pooling across up to 64 chips.
- **[CC-Cores](/neuron-glossary/device-hardware/collective-communication-engine)**
  dedicated to collective communication.

![A Trainium2 device: eight NeuronCore-v3 cores over four HBM stacks, with DMA engines, CC-Cores, and NeuronLink-v3.](themed-image://trainium2-device.svg)

## Comparison with Trainium

| | [Trainium](/neuron-glossary/device-hardware/trainium) | Trainium2 | Factor |
|---|---|---|---|
| FP8 TFLOPS | 190 | 1,299 | about 6.8× |
| BF16/FP16/TF32 TFLOPS | 190 | 667 | about 3.5× |
| FP32 TFLOPS | 47.5 | 181 | about 3.8× |
| Sparse TFLOPS | — | 2,563 | new |
| HBM capacity | 32 GiB | 96 GiB | 3× |
| HBM bandwidth | 820 GiB/s | 2.9 TB/s | |
| [SBUF](/neuron-glossary/device-hardware/sbuf) | 48 MiB | 224 MiB | 4.7× |
| Interconnect per chip | 384 GB/s | 1,280 GB/s | 3.3× |
| [Memory pool](/neuron-glossary/device-hardware/neuronlink) | 16 chips | 64 chips | 4× |

Trainium2 has four times as many cores as Trainium, and its
[NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3) Tensor Engine
can multiply matrices in select FP8 formats at twice the BF16 rate.
The extra SBUF can keep more [tiles](/neuron-glossary/device-software/tile)
on the chip for reuse. Across a
[Trn2 UltraServer](/neuron-glossary/device-hardware/trn2-ultraserver), each
chip can address HBM on all 64 chips, for a combined 6,144 GiB.

Trainium2 also changed DMA ordering guarantees from write-after-write barriers
to strong-order-write, and added column-major SBUF layouts (`Col-major-2B` and
`Col-major-4B`) alongside row-major.

## New capabilities

Trainium2 is the first chip with
[Logical NeuronCore configuration](/neuron-glossary/device-software/logical-neuroncore),
which controls how many physical cores software treats as one logical core.
The Trn2 default, `LNC=2`, groups the eight physical cores into four logical
ones per chip.

It also brings [structured sparsity](/neuron-glossary/device-software/structured-sparsity),
hardware [DMA descriptor generation](/neuron-glossary/device-hardware/dge),
[DMA transpose](/neuron-glossary/device-software/dma-transpose), and a
bit-accurate Tensor Engine transpose mode.

AWS's chip architecture lists 16 CC-Cores, and the NKI architecture guide
lists 20. The NKI guide gives 3 TB/s for HBM bandwidth. The
table uses the chip architecture's 2.9 TB/s.
[Trainium2 architecture](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trainium2.html),
[Trainium2 NKI architecture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium2_arch.html)
