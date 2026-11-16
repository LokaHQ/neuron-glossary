---
title: What is JAX NeuronX?
short: JAX NeuronX
---

**JAX NeuronX** is the beta plugin that lets JAX train and run models on
Inf2, Trn1, Trn2, and Trn3. The `libneuronxla` package makes Neuron devices
available through PJRT, JAX's plugin interface for accelerator backends.
The `jax-neuronx` package brings in a tested set of dependencies and adds
support for calling [NKI kernels](/neuron-glossary/device-software/nki).
[JAX NeuronX overview](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/jax/index.html) · [Installation matrix](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/setup/jax/index.html)

When you call a function wrapped in `jax.jit`, JAX records the computation
and passes it through the [XLA stack](/neuron-glossary/host-software/xla).
The Neuron backend compiles it for the device. Changing shapes, dtypes, or
how arrays are split across devices can trigger a new compilation.
After setup, run `jax.devices()` to confirm JAX sees your Neuron devices.
[AWS installation check](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/setup/jax/manual.html)
