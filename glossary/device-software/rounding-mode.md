---
title: What are Neuron rounding modes?
short: Rounding mode
---

The **rounding mode** determines which value Neuron stores when a
floating-point result falls between two representable values.

- **RNE** (round nearest, ties to even) selects the nearest representable
  value. At an exact tie, it picks the value with a zero in the last
  significand bit. This is the default.
- **SR** (stochastic rounding) chooses either neighboring representable value,
  with probability proportional to the proximity of the exact result.

RNE is available on all NeuronCore generations. Stochastic rounding is
available starting with
[NeuronCore-v2](/neuron-glossary/device-hardware/neuroncore-v2).
[AWS rounding modes](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-features/rounding-modes.html)

## Small updates in low precision

Suppose an update adds `0.5` to an FP16 value of `1024.0`. The exact result
is halfway between `1024.0` and `1025.0`. RNE chooses `1024.0` every time,
so repeatedly adding the increment to the rounded result leaves it
unchanged. Stochastic rounding picks `1025.0` half the time, preserving the
increment in expectation.

The same problem arises when a training update is small relative to a BF16
weight. Stochastic rounding can help such updates accumulate and can make
a full-precision master copy of weights unnecessary for some workloads.
That saves [HBM](/neuron-glossary/device-hardware/hbm), with convergence
depending on the training recipe.
[AWS rounding modes and accumulation example](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-features/rounding-modes.html)

## Runtime settings

Set `NEURON_RT_STOCHASTIC_ROUNDING_EN=1` to enable stochastic rounding
in the runtime.
For controlled comparisons, the
[Neuron Runtime](/neuron-glossary/host-software/neuron-runtime) also exposes
`NEURON_RT_STOCHASTIC_ROUNDING_SEED`.
[AWS runtime environment variables](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/neuron-runtime/api/nrt-env-var-reference.html)
