---
title: What is NeuronCore-v2?
short: NeuronCore-v2
---

**NeuronCore-v2** is the second-generation
[NeuronCore](/neuron-glossary/device-hardware/neuroncore). It powers both
[Trainium](/neuron-glossary/device-hardware/trainium) and
[Inferentia2](/neuron-glossary/device-hardware/inferentia2), with two cores
per chip in both cases.

## Compute engines

| Engine | Throughput | Purpose |
|---|---|---|
| [Tensor](/neuron-glossary/device-hardware/tensor-engine) | 92 TFLOPS BF16/FP16, 23 TFLOPS FP32 | Matrix multiplication, convolution, transpose |
| [Vector](/neuron-glossary/device-hardware/vector-engine) | 2.3 TFLOPS FP32 | Layer norm, pooling, reductions |
| [Scalar](/neuron-glossary/device-hardware/scalar-engine) | 2.9 TFLOPS FP32 | GELU, sigmoid, exp, reciprocal |
| [GpSimd](/neuron-glossary/device-hardware/gpsimd-engine) | 8 × 512-bit processors | Arbitrary C/C++ |

Relative to [v1](/neuron-glossary/device-hardware/neuroncore-v1), the
Tensor Engine has about 6× the throughput, the Scalar Engine 3×, and the
Vector Engine 10× in AWS's comparison.

The data-path width is how many elements an engine can accept or return per
clock cycle. These figures matter when tuning an
[NKI](/neuron-glossary/device-software/nki) kernel.

| Engine | Data path (elements/cycle) | Clock |
|---|---|---|
| Tensor | 2×128 in, 1×128 out | 2.8 GHz |
| Vector | 128 in/out | 1.12 GHz |
| Scalar | 128 in/out | 1.4 GHz |
| GpSimd | — | 1.4 GHz |

## Memory

Each core has two software-managed memories, both organized into
**128 partitions**.

- [SBUF](/neuron-glossary/device-hardware/sbuf): 24 MiB, so 192 KiB per partition.
- [PSUM](/neuron-glossary/device-hardware/psum): 2 MiB, so 16 KiB per partition.

The two cores on the chip share 32 GiB of
[HBM](/neuron-glossary/device-hardware/hbm) at 820 GiB/s in the chip
architecture specifications.

The [systolic array](/neuron-glossary/device-hardware/systolic-array) is
128×128, which is where the 128-partition figure comes from and why
[tile shapes](/neuron-glossary/device-software/tiling) are capped at 128 in
the partition dimension.

## What v2 introduced

- **The [GpSimd Engine](/neuron-glossary/device-hardware/gpsimd-engine)**,
  and with it [custom operators](/neuron-glossary/device-software/custom-operators).
- **Control flow and dynamic shapes**, via ISA extensions. A model with a
  data-dependent branch no longer has to round-trip to the host.
- **Programmable [rounding](/neuron-glossary/device-software/rounding-mode).**
  You can select round-to-nearest-even or stochastic rounding. Stochastic
  rounding can help preserve small updates in BF16 training.
- **[cFP8](/neuron-glossary/device-software/cfp8) and TF32** data types.

On Trn1 and Inf2, software sees each physical core individually.
[Logical NeuronCore](/neuron-glossary/device-software/logical-neuroncore)
configuration starts with [v3](/neuron-glossary/device-hardware/neuroncore-v3).

Two engine-parallelism restrictions also apply on v2 and were lifted in v3: the
Vector and GpSimd engines cannot access
[SBUF](/neuron-glossary/device-hardware/sbuf) at the same time, and the
Vector and Scalar engines cannot access
[PSUM](/neuron-glossary/device-hardware/psum) at the same time.
[AWS Trainium/Inferentia2 NKI architecture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium_inferentia2_arch.html),
[NeuronCore-v2 architecture](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/neuron-core-v2.html)
