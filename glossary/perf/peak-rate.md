---
title: What is peak rate?
short: Peak rate
abbr:
---

A **peak rate** is a theoretical throughput limit under specified
conditions. The compute peak is the flat part of a
[roofline](/neuron-glossary/perf/roofline-model) and the denominator in
[model FLOPs utilization](/neuron-glossary/perf/mfu). Published peaks
assume full use of the relevant hardware, with no stalls. A benchmark
measures the rate a particular workload sustains.

## Compute peaks by chip and engine

Per [Trainium2](/neuron-glossary/device-hardware/trainium2) chip:

| Precision | Peak |
|---|---|
| Sparse FP8/FP16/BF16/TF32 | 2,563 TFLOPS |
| Dense FP8 | 1,299 TFLOPS |
| BF16 / FP16 / TF32 | 667 TFLOPS |
| FP32 | 181 TFLOPS |

Per [NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3), by
engine:

| Engine | Peak |
|---|---|
| [Tensor](/neuron-glossary/device-hardware/tensor-engine) | 79 BF16 TFLOPS |
| [Scalar](/neuron-glossary/device-hardware/scalar-engine) | 1.2 FP32 TFLOPS |
| [Vector](/neuron-glossary/device-hardware/vector-engine) | 1.0 FP32 TFLOPS |

AWS publishes chip and engine figures separately. Use the chip figures for
a chip-level estimate. Use the Vector Engine's peak, for example, if it
does the arithmetic you are measuring.
[Trainium2 chip specifications](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trainium2.html)
and [Trainium2 engine specifications](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium2_arch.html).

## Bandwidth peaks

The Trainium2 chip overview reports **2.9 TB/s** of
[HBM](/neuron-glossary/device-hardware/hbm) bandwidth and **3.5 TB/s** of
[DMA](/neuron-glossary/device-hardware/dma-engine) bandwidth. DMA can move
data on and off the chip. A transfer that reads local HBM is also subject
to the HBM limit. Cross-chip transfers depend on which
[NeuronLink](/neuron-glossary/device-hardware/neuronlink) path they use.

When reporting a percentage of peak, state the precision, whether the
peak is dense or sparse, and the scope (engine, chip, or multiple chips).
Dividing peak compute by peak bandwidth for a matching scope gives the
[machine balance](/neuron-glossary/perf/arithmetic-intensity).
