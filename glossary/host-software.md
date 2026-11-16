---
title: Host Software
---

The software on the host CPU connects your application to the Neuron
accelerator. A framework or serving engine asks the
[compiler](/neuron-glossary/host-software/neuronx-cc) to build an executable.
The [runtime](/neuron-glossary/host-software/neuron-runtime) loads it and
works with the [driver](/neuron-glossary/host-software/neuron-driver) to run
it on the accelerator.

Start with the [Neuron SDK](/neuron-glossary/host-software/neuron-sdk) to
find the framework for your workload. Use
[`neuron-ls`](/neuron-glossary/host-software/neuron-ls) to see which
devices your instance exposes and
[Neuron Explorer](/neuron-glossary/host-software/neuron-explorer) to see
where a workload spends its time.
