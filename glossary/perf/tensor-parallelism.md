---
title: What is tensor parallelism on Neuron?
short: Tensor parallelism
abbr: TP
---

**Tensor parallelism** (TP) splits computations within a layer across several
[logical NeuronCores](/neuron-glossary/device-software/logical-neuroncore).
Each rank (worker process) computes on its slice of the weights. A
[collective](/neuron-glossary/device-software/collectives) combines or redistributes
the results.

For example, a feed-forward block's first linear layer can be **column-parallel**, giving each
rank a slice of the output features. A **row-parallel** second layer consumes the
sharded features and produces partial outputs. An all-reduce combines them
when every rank needs the full result. With sequence parallelism, a
reduce-scatter can leave the result sharded. Attention commonly shards by head.

## What TP buys

TP can fit a model whose weights and KV cache exceed the memory of one chip.
Spreading weight shards across chips also lets those chips read their local
[HBM](/neuron-glossary/device-hardware/hbm) in parallel. The bandwidth gain
depends on the **physical chips** used, the balance of the shards, and the cost
of the collectives between ranks.

On a [Trn2](/neuron-glossary/device-hardware/trn2) instance with `LNC=2`,
each chip has four logical cores. A TP group of 16 ranks can occupy four
chips if placement uses four ranks per chip. Check the device map to see
which chips supply bandwidth.

## Choosing the degree and placing ranks

1. Count the available **logical cores** with
   [Logical NeuronCore configuration](/neuron-glossary/device-software/logical-neuroncore)
   and the device allocation in mind. A full `trn2.48xlarge` exposes 64 logical
   cores at `LNC=2`.
2. Check model and backend constraints. The number of attention heads, KV
   heads, and intermediate dimensions can constrain valid sharding. Some
   implementations replicate KV heads at higher TP degrees.
3. Benchmark valid degrees that fit the model and KV cache. More ranks give
   each rank less work and add communication. In
   [vLLM Neuron](/neuron-glossary/host-software/vllm-neuron), TP trades off with
   other strategies such as [data parallelism](/neuron-glossary/perf/data-parallelism).
4. Keep frequently communicating ranks in a fast
   [NeuronLink](/neuron-glossary/device-hardware/neuronlink) domain where
   possible. A [Trn2 UltraServer](/neuron-glossary/device-hardware/trn2-ultraserver)
   links instance members over NeuronLink, and a
   [Trn3 UltraServer](/neuron-glossary/device-hardware/trn3-ultraserver) uses
   NeuronSwitch and direct links inside its scale-up domain.
   [Neuron DRA](/neuron-glossary/host-software/neuron-dra) can allocate
   topology-aware groups on eligible EKS clusters.

![Typical Trn2 training placement by communication pattern. Tensor and context parallelism prefer a fast NeuronLink domain. Pipeline and data parallelism can span instances over EFA.](themed-image://parallelism.svg)

See AWS's [vLLM Neuron tensor parallelism design](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/vllm-neuron/docs/design/parallelism/tensor_parallelism.html)
for worked examples of attention, MLP sharding, and KV-head replication.
