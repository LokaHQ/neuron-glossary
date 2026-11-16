---
title: What is overhead on Neuron?
short: Overhead
abbr:
---

**Overhead** is time and work spent preparing or dispatching computation.
On Neuron, it includes host dispatch, first-use compilation, synchronization,
and transfers. A profile separates these from time spent
[compute-bound](/neuron-glossary/perf/compute-bound) or
[memory-bound](/neuron-glossary/perf/memory-bound) on the device.

## Dispatch, compilation, and graph breaks

**Eager dispatch.** [TorchNeuron](/neuron-glossary/host-software/torchneuron)
can dispatch an ATen operator at a time. A new operator specialization can
trigger compilation before it executes. Unsupported eager operators may run on
the CPU, adding device transfers and synchronization. Experimental adaptive eager mode can fuse eligible queued operations.
It is off by default in Neuron 2.33.

**Compiled execution.** `torch.compile(backend="neuron")` lets the compiler
compile each captured graph as a
[NEFF](/neuron-glossary/device-software/neff). This gives the compiler room to fuse operators and schedule their data
transfers, with fewer host dispatches. Dynamo graph breaks split the
work into separately compiled segments. Legacy
[PyTorch NeuronX](/neuron-glossary/host-software/torch-neuronx) lazy execution
has a separate mechanism for materializing pending work.

**Cold or repeated compilation.** A new shape, dtype, compiler setting, or failed graph guard can require a
new specialization. A guard is a condition PyTorch checks before reusing a
captured graph. Check
[cache hits](/neuron-glossary/host-software/neuron-persistent-cache) and account
for warmup separately when measuring steady state. Serving stacks often use
fixed buckets for this reason.

## Transfers and synchronization

**Host-to-device movement.** Moving inputs from host DRAM to device
[HBM](/neuron-glossary/device-hardware/hbm) can stall a job whose data pipeline
cannot keep up. Use [`neuron-ls`](/neuron-glossary/host-software/neuron-ls) to
check device and NUMA placement. Printing an eager device tensor also incurs a
synchronization and host copy.

**Collectives on the critical path.** Reducing gradients after backward adds
the uncovered collective time to each step. Neuron's dedicated
[CC-Cores](/neuron-glossary/device-hardware/collective-communication-engine)
can communicate while compute engines work when dependencies allow it. See
[latency hiding](/neuron-glossary/perf/latency-hiding).

[Neuron Explorer](/neuron-glossary/host-software/neuron-explorer) correlates device
and system activity. Look at host dispatch and compilation around device idle
gaps, as well as DMA and collectives before a stalled compute engine.

See AWS's [TorchNeuron compile guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/torch/compile/about-torch-compile.html)
and [eager execution overview](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/torch/about-pytorch-neuron.html#eager-mode-execution).
