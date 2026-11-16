---
title: What is latency hiding on Neuron?
short: Latency hiding
---

**Latency hiding** keeps an engine busy with independent work while another
operation is in progress. For example, the Tensor Engine can compute one
[tile](/neuron-glossary/device-software/tile) while a DMA engine loads the next.

The target shape is a software pipeline:

```
DMA:      load tile n+1 ────────────►
Tensor:   compute tile n ───────────►
DMA:      store tile n-1 ───────────►
```

This pipeline keeps the
[Tensor Engine](/neuron-glossary/device-hardware/tensor-engine) busy if tile
`n+1` finishes loading into
[SBUF](/neuron-glossary/device-hardware/sbuf) before compute needs it.

A GPU can switch to another ready warp while one waits for data. On Neuron,
overlap between compute and data movement comes from the schedules produced
by the [compiler](/neuron-glossary/host-software/neuronx-cc) or from
independent work you arrange in an [NKI](/neuron-glossary/device-software/nki)
kernel.

## The hardware that helps

- **[DMA engines](/neuron-glossary/device-hardware/dma-engine) run in
  parallel with compute.** 128 of them on
  [Trainium2](/neuron-glossary/device-hardware/trainium2), about 16 per
  [NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3).
- **The [Sync Engine](/neuron-glossary/device-hardware/sync-engine)** exists
  to trigger DMAs without injecting instructions into a compute engine's
  stream.
- **The [DGE](/neuron-glossary/device-hardware/dge)** generates descriptors
  independently. This can reduce the work the issuing engine spends
  preparing a transfer.
- **[CC-Cores](/neuron-glossary/device-hardware/collective-communication-engine)**
  do the same for
  [collectives](/neuron-glossary/device-software/collectives), overlapping
  communication with computation.

## What you do

**Expose independent work.** Use Python `range()` for statically unrolled
tile loops in current NKI. Organize loads and compute so there is independent
work for the scheduler to overlap. Use `nl.fori_loop` or `nl.while_loop` for
device-side loops when the bounds depend on runtime values. See
[nki.language](/neuron-glossary/device-software/nki-language) and the
[NKI optimization guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/deep-dives/nki_perf_guide.html).

**Double-buffer.** Size [tiles](/neuron-glossary/device-software/tile) so
that two fit in [SBUF](/neuron-glossary/device-hardware/sbuf)
alongside the other live data. One buffer feeds compute while DMA fills
the other.

**Watch the profile.** Gaps on the Tensor Engine timeline in
[Neuron Explorer](/neuron-glossary/host-software/neuron-explorer), with
DMA activity in the gaps, can indicate that loads are on the critical path.

## Overlapping collectives

The same idea applies to distributed training. Gradient buckets can be
reduced as they become ready while the rest of the backward pass continues.
How much time this saves depends on when the communication starts and when
the result is needed. See
[data parallelism](/neuron-glossary/perf/data-parallelism).
