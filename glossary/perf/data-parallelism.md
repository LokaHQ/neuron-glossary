---
title: What is data parallelism on Neuron?
short: Data parallelism
abbr: DP
---

**Data parallelism** (DP) trains replicas of the same model on different
examples from a batch. Each worker process (a **rank**) computes its own
gradients. In PyTorch DistributedDataParallel (DDP),
[all-reduce](/neuron-glossary/device-software/collectives) synchronizes the
gradients so every replica makes the same update.

DP can span instances in an
[UltraCluster](/neuron-glossary/device-hardware/ultracluster). With ordinary
DDP, each replica still needs room for its model, gradients, optimizer state,
and activations. A mixed-precision Adam setup with BF16 parameters and
gradients, FP32 master weights, and two FP32 moment buffers needs about
16 bytes per parameter before activations. For a 70B-parameter model that is
roughly 1.1 TB per replica, well beyond the 96 GiB of one
[Trainium2](/neuron-glossary/device-hardware/trainium2) chip.

## Sharding the replicated state

**ZeRO-1** shards the optimizer state across data-parallel ranks. It was
available in legacy [NxD Training](/neuron-glossary/host-software/nxd-training).

For native Trainium training, [TorchNeuron](/neuron-glossary/host-software/torchneuron)
supports standard PyTorch DDP and FSDP2. The FSDP2 path in
[TorchTitan Neuron](/neuron-glossary/host-software/torchtitan-neuron) shards
parameters, gradients, and optimizer state. It gathers parameters for
computation and reduce-scatters the gradients. See the
[TorchTitan support matrix](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/training/torchtitan/about-torchtitan-neuron.html#support-matrix).

## Overlapping the all-reduce

DDP groups gradients into buckets and can start reducing a bucket as soon
as its gradients are ready. Backpropagation can continue on layers whose
gradients are still being computed. Neuron's dedicated
[collective communication cores](/neuron-glossary/device-hardware/collective-communication-engine)
can run those reductions alongside compute. The tail of the final
collective still counts toward step time if backward finishes first.
See [latency hiding](/neuron-glossary/perf/latency-hiding) and
[`nccom-test`](/neuron-glossary/host-software/nccom-test).
