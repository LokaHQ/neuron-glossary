---
title: What is model FLOPs utilization?
short: Model FLOPs utilization
abbr: MFU
---

**Model FLOPs utilization** (MFU) compares the rate of useful model
arithmetic with the hardware's theoretical peak rate.

```
MFU = useful model FLOPs per second / peak FLOPs per second
```

For dense transformer training, a common starting estimate of useful
work is `6 × parameter count × token count` per step. The approximation
captures the main weight-matrix operations. The exact count depends on
the architecture, sequence length, and which weights are active.
Padding and activation recomputation add hardware work without increasing
the model FLOPs in that estimate.

Compare runs using the same counting convention. Report the device count,
precision, and which portion of the run you timed. For small-batch LLM
decode, weight or KV-cache traffic can dominate. Pair MFU with tokens per
second and measured HBM bandwidth utilization to see where time goes.
[Neuron Explorer metric definitions](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/tools/neuron-explorer/glossary.html)

## Which peak to divide by

On Neuron this needs care, because "peak" depends on precision:

| [Trainium2](/neuron-glossary/device-hardware/trainium2) | Peak per chip |
|---|---|
| FP8 | 1,299 TFLOPS |
| BF16/FP16/TF32 | 667 TFLOPS |
| FP32 | 181 TFLOPS |
| Sparse FP8/FP16/BF16/TF32 | 2,563 TFLOPS |

Divide by the peak for the precision and mode used by the workload,
using the total peak of the chips included in the measurement. A dense
BF16 run should use the dense BF16 peak. Mixed-precision comparisons
should say how the denominator was chosen.

## Raising it

The levers are the ones in this section, and which applies depends on the
[roofline](/neuron-glossary/perf/roofline-model):

- **[Engine parallelism](/neuron-glossary/perf/engine-parallelism)** — overlap independent work on the engines your kernel uses.
- **[Latency hiding](/neuron-glossary/perf/latency-hiding)** — overlap DMA
  with compute.
- **[Fusion](/neuron-glossary/perf/fusion)** — remove HBM round trips.
- **[Tile geometry](/neuron-glossary/device-software/tiling)** — fill the
  Tensor Engine array while leaving enough scratchpad space to overlap work.
- **Overlapped collectives** — launch gradient reductions as buckets become ready.

A profile in
[Neuron Explorer](/neuron-glossary/host-software/neuron-explorer) can show whether the job spends time on arithmetic, transfers, or waiting for
other ranks.
