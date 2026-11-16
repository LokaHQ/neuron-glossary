---
title: What is the Neuron Runtime?
short: Neuron Runtime
abbr: libnrt
---

The **Neuron Runtime** loads compiled
[NEFFs](/neuron-glossary/device-software/neff) onto
[Neuron devices](/neuron-glossary/device-hardware/neuron-device) and
executes them through the [Neuron driver](/neuron-glossary/host-software/neuron-driver).
It reserves cores for the process, allocates device memory, moves inputs
and outputs, and runs
[collectives](/neuron-glossary/device-software/collectives).

[Native TorchNeuron](/neuron-glossary/host-software/torchneuron),
[JAX NeuronX](/neuron-glossary/host-software/jax-neuronx) and the legacy
[PyTorch/XLA integration](/neuron-glossary/host-software/torch-neuronx)
use this runtime. The `aws-neuronx-runtime-lib` package supplies the
C library at `/opt/aws/neuron/lib/libnrt.so` and headers under
`/opt/aws/neuron/include`. You can also load and execute a NEFF directly
through the Python `nrtpy` API.
[AWS Runtime developer guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/neuron-runtime/guides/nrt-developer-guide.html) · [AWS nrtpy guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/neuron-runtime/nrtpy/index.html)

## Core allocation and runtime settings

| Variable | Effect |
|---|---|
| `NEURON_RT_VISIBLE_CORES` | Specify which logical NeuronCore IDs the process can use, for example `0-3` |
| `NEURON_RT_NUM_CORES` | Reserve the requested number of available cores |
| `NEURON_LOGICAL_NC_CONFIG` | Select how many physical cores make up a [logical NeuronCore](/neuron-glossary/device-software/logical-neuroncore) on supported hardware |
| `NEURON_RT_STOCHASTIC_ROUNDING_EN` | Enable [stochastic rounding](/neuron-glossary/device-software/rounding-mode) |
| `NEURON_RT_LOG_LEVEL` | Control runtime log verbosity |

`NEURON_RT_VISIBLE_CORES` takes precedence over `NEURON_RT_NUM_CORES`.
[AWS Runtime configuration guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/neuron-runtime/guides/configuration-guide.html) · [AWS Runtime environment variables](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/neuron-runtime/api/nrt-env-var-reference.html)

If device access breaks after an upgrade, check that your instance family,
host OS, kernel, and glibc match the compatibility table. Some Neuron SDK
2.33 runtime features, including asynchronous tensor I/O and host-device
transfer profiling, require Neuron Driver 2.31 or later.
[AWS compatibility reference](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/neuron-runtime/compatibility.html) · [AWS Neuron 2.33 changes](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/whats-new.html)
