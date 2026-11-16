---
title: What is the Scalar Engine?
short: Scalar Engine
---

The **Scalar Engine** (ScalarE) handles operations where **each output element
depends on one input element**. Examples include GELU, ReLU, sigmoid,
exponential, reciprocal, and square root.

In `y[i] = gelu(x[i])`, each output uses one input value. The Scalar Engine
evaluates many of these independent operations in parallel. In layer
normalization, an output needs a mean and variance computed across many
inputs. The [Vector Engine](/neuron-glossary/device-hardware/vector-engine)
handles reductions such as those sums.

Throughput by generation:

| | [v1](/neuron-glossary/device-hardware/neuroncore-v1) | [v2](/neuron-glossary/device-hardware/neuroncore-v2) | [v3](/neuron-glossary/device-hardware/neuroncore-v3) | [v4](/neuron-glossary/device-hardware/neuroncore-v4) |
|---|---|---|---|---|
| FP32 | 512 FLOP/cycle | 2.9 TFLOPS | 1.2 TFLOPS | 1.2 TFLOPS |

The Trainium3 NKI guide lists FP8, FP16, BF16, TF32, FP32, INT8, INT16 and
INT32 for v4 Scalar Engine inputs and outputs. Individual instructions have
their own data type requirements.
[Trainium3 NKI architecture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium3_arch.html#scalar-engine)

Like the Vector Engine, it can read and write both
[SBUF](/neuron-glossary/device-hardware/sbuf) and
[PSUM](/neuron-glossary/device-hardware/psum), so it can also be used to
drain [PSUM](/neuron-glossary/device-hardware/psum) after a matmul. On
[NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3) the Vector
and Scalar engines can access PSUM **in parallel** at full bandwidth, provided
they target different PSUM banks. On
[v2](/neuron-glossary/device-hardware/neuroncore-v2), those accesses serialize.

v3 also added bit-accurate tensor copies without an intermediate cast through
FP32.

## Exponential in attention

In a fused attention kernel, the next matrix multiplication can wait on the
softmax exponential. On [Trainium2](/neuron-glossary/device-hardware/trainium2),
the Scalar Engine can be the bottleneck for that step.
[NeuronCore-v4](/neuron-glossary/device-hardware/neuroncore-v4) adds a Vector
Engine exponential instruction with 4× the Scalar Engine's exponential
throughput.
