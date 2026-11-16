---
title: What is arithmetic intensity?
short: Arithmetic intensity
---

**Arithmetic intensity** measures how much math an operation does for each
byte it moves. Choose the memory level you want to analyze, such as
[HBM](/neuron-glossary/device-hardware/hbm), and count bytes crossing that
boundary.

```
arithmetic intensity = FLOPs performed / bytes moved
```

Compare that number with the **machine balance**, the ratio of peak compute
throughput to peak bandwidth for the same hardware scope. A
[Trainium2](/neuron-glossary/device-hardware/trainium2) chip has a published
BF16 peak of 667 TFLOPS and HBM bandwidth of 2.9 TB/s, for a balance of about
**230 FLOPs per byte**. Use per-chip throughput with per-chip bandwidth.
Several [NeuronCores](/neuron-glossary/device-hardware/neuroncore) share a
chip's HBM, so the bandwidth one core sustains depends on the workload and
placement.
[Trainium2 specifications](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trainium2.html)

In the [roofline model](/neuron-glossary/perf/roofline-model), below the
balance point bandwidth sets the upper bound. Above it, compute sets the
upper bound. A real kernel can fall below both because of launch overhead,
poor overlap, or limits on an individual engine.

| Operation | FLOPs | Ideal BF16 bytes moved | FLOPs per byte |
|---|---|---|---|
| Element-wise add, `n` elements | `n` | `6n` (two reads, one write) | 0.17 |
| Layer norm, `n` elements | `~5n` | `4n` (one read, one write) | ~1.3 |
| Matmul, `M×K` by `K×N` | `2MKN` | `2(MK + KN + MN)` | grows with operand reuse |
| Decode attention, one query per head, head width `d`, context length `L` | `~4dL` (two matrix-vector products) | `~4dL` (keys and values) | ~1 |

These are simplified examples. They omit bias and scale reads for layer
norm, and omit softmax, queries and outputs for decode attention. Sharing
keys and values across query heads also changes the decode estimate.

For a square matmul of size `N` that reads each input once and writes its
output once, intensity is `N/3`. If the kernel rereads tiles from HBM,
the real intensity is lower. [Tiling](/neuron-glossary/device-software/tiling)
increases reuse, and [fusion](/neuron-glossary/perf/fusion) can keep
intermediate results in [SBUF](/neuron-glossary/device-hardware/sbuf). In both
cases, the same math requires fewer HBM transfers.
