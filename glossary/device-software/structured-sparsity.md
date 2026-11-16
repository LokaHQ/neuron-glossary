---
title: What is structured sparsity?
short: Structured sparsity
---

**Structured sparsity** is a regular pattern of zeros in a matrix. On
[NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3) and
[v4](/neuron-glossary/device-hardware/neuroncore-v4), the
[Tensor Engine](/neuron-glossary/device-hardware/tensor-engine) can use that
pattern to skip multiplications by zero.

The pattern is **M:N**: within every group of `N` contiguous elements, at most
`M` are non-zero. Neuron supports 4:16, 4:12, 4:8, 2:8, 2:4, 1:4, and 1:2.

At 2:4, at least two entries in every group of four must be zero. One of the
two matmul inputs needs to follow the pattern. Model weights are a common
choice because they can be pruned ahead of time.

## Peak throughput

| Scope | Input format | Dense TFLOPS | Sparse TFLOPS |
|---|---|---|---|
| [Trainium2](/neuron-glossary/device-hardware/trainium2), per chip | FP8 | 1,299 | 2,563 |
| [NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3), per engine | cFP8 | 158 | 316 |
| [NeuronCore-v4](/neuron-glossary/device-hardware/neuroncore-v4), per engine | FP16 / BF16 / TF32 | 79 | 315 |

AWS publishes the chip and engine peaks separately. On v4, dense
[MXFP8 and MXFP4](/neuron-glossary/device-software/mxfp8) also peak at
315 TFLOPS per engine. They use a separate dense path.
[AWS Trainium2 specifications](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trainium2.html),
[AWS NeuronCore-v3 architecture](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/neuron-core-v3.html#tensor-engine),
[AWS NeuronCore-v4 architecture](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/neuron-core-v4.html#tensor-engine)

The v3 Tensor Engine has an input path of 2×128 elements per cycle for
dense BF16 and 5×128 for sparse input.
[Trainium2 NKI architecture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium2_arch.html#neuroncore-v3-compute-engine-updates)

![Filled cells are non-zero. Regularity is what lets the systolic array skip work predictably.](themed-image://sparsity.svg)

## Why the pattern has to be structured

A [systolic array](/neuron-glossary/device-hardware/systolic-array) streams
data through a fixed grid in lockstep. A dense matmul still processes
arbitrary zeros. An M:N pattern lets the sparse path reserve a fixed number
of slots per group and encode where those values belong.

To use a supported pattern, prune weights to meet the per-group limit and
measure model accuracy. Fine-tuning can help recover accuracy after pruning.
Both 1:2 and 4:8 keep at most half the weights, but a group of eight gives
pruning more choice about which weights to keep. With 4:16, each group keeps
at most a quarter of the weights.

## Restrictions

On [NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3),
sparse matmul is incompatible with double-rate
[FP8](/neuron-glossary/device-software/cfp8) mode. The dense FP8 double-row
mode and the sparse path have separate peak rates.
[Trainium2 NKI architecture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium2_arch.html#double-fp8-matmul-performance)
