---
title: What is NeuronCore batching?
short: Batching
---

**Batching** runs several inputs through a model together. A layer can
reuse the same weights across inputs, doing more arithmetic for each
byte loaded from [HBM](/neuron-glossary/device-hardware/hbm). This raises
[arithmetic intensity](/neuron-glossary/perf/arithmetic-intensity) when
weight reads dominate.

## Batching during LLM decode

At batch size one, an LLM may read the same weights for every token it
generates. Processing more sequences in one step lets a kernel reuse
those weights across sequences. The gain slows once compute or KV-cache
traffic becomes the larger cost. The KV cache stores each sequence's
past keys and values and grows with the number and length of sequences.

A larger batch can raise aggregate tokens per second while increasing
queueing or per-step latency. A serving system chooses a batch size
based on its throughput and latency targets.

## Continuous batching

In a fixed batch, a finished request's slot can sit idle while longer
requests continue generating.

**Continuous batching** lets sequences join and leave a running batch
between decode steps, so the scheduler can use freed slots for new requests.
This is available in
[vLLM Neuron](/neuron-glossary/host-software/vllm-neuron).

## Batching and compilation

[NEFFs](/neuron-glossary/device-software/neff) can be compiled for particular
input shapes. A serving scheduler can vary which requests are in the batch
and still select a compiled **bucket** for the shape it will run. For example, vLLM Neuron
can bucket by the number of sequences and can optionally bucket by decode
context length. Warming the relevant
[caches](/neuron-glossary/host-software/neuron-persistent-cache) reduces cold
start overhead. See the
[vLLM Neuron configuration reference](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/vllm-neuron/docs/guides/reference-configuration.html).

## In training

Batching in training is a different question. There, batch size is a
**convergence** parameter as much as a performance one, and it interacts with
learning rate schedules. Batch size also changes the memory needed for activations.
