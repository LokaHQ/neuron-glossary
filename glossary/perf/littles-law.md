---
title: What is Little's Law?
short: Little's Law
abbr:
---

**Little's Law** relates how much work is in a system to how fast work
completes and how long each item spends there. In steady state:

```
average work in flight = throughput × average time in the system
```

To plan a pipeline, use the target throughput and an estimate of latency
to size the work in flight. The required concurrency can be higher once
transfers queue or compete for bandwidth. Neuron's
[compiler](/neuron-glossary/host-software/neuronx-cc) or
[NKI](/neuron-glossary/device-software/nki) kernel has to expose enough
independent work for the engines to overlap.

## DMA example

Suppose a [DMA](/neuron-glossary/device-hardware/dma-engine) transfer from
[HBM](/neuron-glossary/device-hardware/hbm) to
[SBUF](/neuron-glossary/device-hardware/sbuf) takes 2 μs on average and
the throughput target is 2 TB/s across a chip. In this example, you need about 4 MB of data in flight across the
chip. For equal transfers of 256 KiB, that is about 16 outstanding transfers.

A [Trainium2](/neuron-glossary/device-hardware/trainium2) chip provides
128 DMA engines for local and cross-device transfers. If a kernel loads
one tile, waits, computes, and then issues the next load, the transfers never
overlap even if spare DMA engines are available.
[Trainium2 NKI architecture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium2_arch.html)

## Tensor Engine example

The [Tensor Engine](/neuron-glossary/device-hardware/tensor-engine) is
deeply pipelined, so several `LoadStationary`/`MultiplyMoving` pairs are in
flight at once. This is why AWS advises reasoning about a matmul's **initiation
interval** rather than the end-to-end latency of a single instruction — the
latency is already hidden, provided you supply enough independent work.

[PSUM](/neuron-glossary/device-hardware/psum) has eight banks per
partition. On [NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3),
each `nc_matmul` output fits within one bank, leaving the other banks for
independent accumulation groups. On
[NeuronCore-v4](/neuron-glossary/device-hardware/neuroncore-v4), a wide
output can span all eight banks. The room available for interleaving
accumulation groups depends on output width and data type.

## Using it

In a profile, look for gaps between engine instructions or long periods
spent waiting for dependencies. To increase useful work in flight:

- **Double-buffer.** Use one [tile](/neuron-glossary/device-software/tile)
  buffer for compute while DMA fills the other.
- **Expose independent work.** Use separate buffers for transfers and
  computation that can overlap. In NKI 0.7, small loops with known bounds can
  use Python `range` and unroll at specialization time.
  [NKI loop guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/deep-dives/nki-loops.html)
- **Leave PSUM banks free.** A wide accumulation group can occupy all
  eight banks, leaving no bank for a second group.

This term is the Neuron counterpart of
[Little's Law in Modal's GPU Glossary](https://modal.com/gpu-glossary/perf/littles-law),
where the same law explains warp occupancy instead of pipeline depth.
