---
title: What does memory-bound mean?
short: Memory-bound
---

An operation is **memory-bound** when the rate of data transfer sets its
runtime. Element-wise operations often fall into this category because they
read and write many values for a small amount of arithmetic.

In the [roofline model](/neuron-glossary/perf/roofline-model), this is the
region where bandwidth caps throughput. Which memory matters depends on
where the data moves. An operation can be limited by
[HBM](/neuron-glossary/device-hardware/hbm) or by a path into an on-chip
scratchpad.

## LLM decoding at batch size one

In a batch-1 dense decode step, a weight streamed from HBM typically contributes
one multiply-accumulate. BF16 stores it in two bytes, so the weight-only
arithmetic intensity is roughly **1 FLOP per byte**. KV-cache reads and other
traffic also take bandwidth.

If each step reads all the weights from HBM, this gives a weight-only
upper bound at batch size one.

```
tokens/sec ≤ HBM bandwidth / bytes of model weights
```

An 8B model in BF16 has about 16 GB of weights, which fit in a Trainium2
chip's 96 GiB of HBM. With the full chip bandwidth of 2.9 TB/s, the weight-only
ceiling is about **180 tokens/s**. That estimate excludes KV-cache traffic,
compute, and communication. See the [Trn2 architecture specifications](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trn2-arch.html#trn2-instance-specifications).

## What actually helps

**Quantize.** Storing weights in fewer bytes can raise the bandwidth ceiling.
Actual savings depend on the format, scale metadata, and which weights are
quantized. See [FP8](/neuron-glossary/device-software/cfp8) and
[MX formats](/neuron-glossary/device-software/mxfp8).

**Batch.** Reading the weights once and using them for many sequences amortizes
the traffic, raising intensity roughly linearly with batch size. This is the idea behind
[batching](/neuron-glossary/perf/neuroncore-batching).

**[Fuse](/neuron-glossary/perf/fusion).** Keep intermediates in
[SBUF](/neuron-glossary/device-hardware/sbuf) rather than round-tripping
them to HBM between operators.

**Use more chips.**
[Tensor parallelism](/neuron-glossary/perf/tensor-parallelism) can read
shards in parallel across physical chips. Effective bandwidth depends on
rank placement, shard balance, and communication overhead.

**Reuse tiles.** [Tiling](/neuron-glossary/device-software/tiling) can reduce
how often the same inputs cross the HBM boundary. Leave enough scratchpad
space for both the tile and the rest of the pipeline.

A faster [Tensor Engine](/neuron-glossary/device-hardware/tensor-engine)
helps only if arithmetic is taking time on the critical path.
Measure the relevant bytes and bandwidth before tuning matmul throughput.
