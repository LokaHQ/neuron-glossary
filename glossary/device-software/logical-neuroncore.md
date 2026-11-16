---
title: What is Logical NeuronCore configuration?
short: Logical NeuronCore
abbr: LNC
---

**Logical NeuronCore configuration** (LNC) controls how many physical
[NeuronCores](/neuron-glossary/device-hardware/neuroncore) the compiler and
runtime present as one logical core. It applies to
[Trainium2](/neuron-glossary/device-hardware/trainium2) and
[Trainium3](/neuron-glossary/device-hardware/trainium3). `LNC=1` exposes
each physical core separately. `LNC=2` groups cores in pairs, which can
reduce the number of workers and model shards.
[AWS LNC configuration guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-features/logical-neuroncore-config.html)

## Counting cores on Trn2

**Trn2 defaults to `LNC=2` in the runtime.** On a `trn2.48xlarge`,
[`neuron-ls`](/neuron-glossary/host-software/neuron-ls) reports 64 logical
cores with this configuration. Use that count when sizing worker groups and
[tensor-parallel](/neuron-glossary/perf/tensor-parallelism) degrees.

| Trn2 scope | Physical cores | Logical cores at `LNC=2` |
|---|---|---|
| One chip | 8 | 4 |
| `trn2.48xlarge` | 128 | 64 |

![At LNC=2, the Trainium2 runtime exposes each pair of physical NeuronCore-v3 cores as one logical core. Each physical core retains its own engines, SBUF, and PSUM.](themed-image://logical-neuroncore.svg)

## Writing and compiling kernels

At `LNC=2`, [NKI](/neuron-glossary/device-software/nki) compiles one
instruction stream for each physical core. Both can access shared
[HBM](/neuron-glossary/device-hardware/hbm). Call `nl.program_id()` to
get 0 or 1 and select the part of a tensor that core should process.
Each core keeps its own [SBUF](/neuron-glossary/device-hardware/sbuf),
[PSUM](/neuron-glossary/device-hardware/psum), and tile limits, including the
[128-partition limit](/neuron-glossary/device-software/tiling).
[AWS guide to LNC in NKI](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/get-started/about/lnc.html)

An unspecified NKI 0.7 kernel defaults to `LNC=1`, while the graph
compiler defaults to `LNC=2` on Trainium2 and Trainium3. Set
`NEURON_LOGICAL_NC_CONFIG` explicitly and check that the kernel, graph
compiler's `--lnc` setting, and runtime agree. A launch such as
`kernel[2](x)` takes precedence over the environment setting for the
kernel. Starting with Neuron SDK 2.33.0, the graph compiler rejects
kernel and graph LNC mismatches by default.
[AWS NKI migration guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/migration/index.html#kernel-lnc-configuration)
