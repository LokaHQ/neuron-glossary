---
title: What is TorchTitan Neuron?
short: TorchTitan Neuron
---

**TorchTitan Neuron** is the beta Neuron port of PyTorch TorchTitan for
pretraining language models on [Trn2](/neuron-glossary/device-hardware/trn2) and
[Trn3](/neuron-glossary/device-hardware/trainium3). It runs on native
[TorchNeuron](/neuron-glossary/host-software/torchneuron). Its recipes show how
to split model state across workers with Fully Sharded Data Parallel (FSDP)
and combine it with tensor, context, expert, or pipeline parallelism.
Neuron 2.33.1 ships `torchtitan` `0.2.2+neuron.1` for native PyTorch 2.14.
[TorchTitan Neuron release notes](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/release-notes/components/torchtitan-neuron.html)

## Why SimpleFSDP matters

TorchTitan can run in eager mode or with `torch.compile` using the `neuron`
backend. A standard FSDP2 recipe can compile each transformer block on its
own and do parameter and gradient transfers between those blocks.
SimpleFSDP puts those
[collectives](/neuron-glossary/device-software/collectives) inside the graph
so the compiler can schedule communication alongside computation. Capturing
a larger graph can increase compile time.
[AWS SimpleFSDP tutorial](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/training/torchtitan/tutorials/tutorial-simple-fsdp-training.html)

For a documented starting point, AWS validates Llama 3 8B pretraining with
TP4 × FSDP16 on a `trn2.48xlarge`. That configuration combines four-way
tensor parallelism with sixteen-way FSDP. Older
[NxD Training](/neuron-glossary/host-software/nxd-training) recipes use
PyTorch/XLA and their own sharding APIs.
[AWS validated TorchTitan configurations](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/training/torchtitan/about-torchtitan-neuron.html)
