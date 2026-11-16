---
title: What is neuron-top?
short: neuron-top
---

**`neuron-top`** is a terminal dashboard for live
[NeuronCore](/neuron-glossary/device-hardware/neuroncore) utilization,
host and [device memory](/neuron-glossary/device-hardware/hbm) usage,
and models loaded by each process.

```
neuron-top
```

Open it to see which cores a process is using and how much memory it has
allocated. For scripts, dashboards, and alerts, use the JSON output from
[`neuron-monitor`](/neuron-glossary/host-software/neuron-monitor).
[AWS neuron-top user guide](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/tools/neuron-sys-tools/neuron-top-user-guide.html)

## The limits of a utilization number

A core can look busy when the
[Scalar Engine](/neuron-glossary/device-hardware/scalar-engine) is working
and the [Tensor Engine](/neuron-glossary/device-hardware/tensor-engine)
is idle. To see what each engine spent time doing, capture a trace with
[Neuron Explorer](/neuron-glossary/host-software/neuron-explorer). Device
memory usage gives you a starting point for checking whether a larger
batch or longer context will fit.
