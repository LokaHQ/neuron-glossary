---
title: What is spilling on Neuron?
short: Spilling
---

**Spilling** moves a value out of fast memory to make room for other
work. A **reload** brings it back when the kernel needs it. The
[Neuron compiler](/neuron-glossary/host-software/neuronx-cc) can insert
these transfers, such as saving an intermediate from
[SBUF](/neuron-glossary/device-hardware/sbuf) to
[HBM](/neuron-glossary/device-hardware/hbm) and reading it back.

The program still computes the same result, but the extra transfers may
show up as unexpected DMA activity. In
[Neuron Explorer](/neuron-glossary/host-software/neuron-explorer), compare
`Spill Save Bytes` and `Spill Reload Bytes` with overall SBUF traffic.
[NKI guide to spill metrics](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/deep-dives/nki_perf_guide.html#opt-2-fuse-operations-to-minimize-intermediate-data-spilling)

## The budgets

| Memory | Capacity | Per partition |
|---|---|---|
| [SBUF](/neuron-glossary/device-hardware/sbuf), [v2](/neuron-glossary/device-hardware/neuroncore-v2) | 24 MiB | 192 KiB |
| SBUF, [v3](/neuron-glossary/device-hardware/neuroncore-v3) | 28 MiB | 224 KiB |
| SBUF, [v4](/neuron-glossary/device-hardware/neuroncore-v4) | 32 MiB | 256 KiB |
| [PSUM](/neuron-glossary/device-hardware/psum), v2–v4 | 2 MiB | 16 KiB |

The [Tensor Engine](/neuron-glossary/device-hardware/tensor-engine)
writes its results to PSUM. Copy completed results to SBUF so the next
matmul has space to accumulate.

## Reducing spills

Count all buffers that must fit at once. If you double-buffer inputs to
[overlap loads and compute](/neuron-glossary/perf/latency-hiding), each
input needs two buffers. [Fusion](/neuron-glossary/perf/fusion) can avoid
HBM traffic between operators, but the fused operation may also need
space for more live intermediates. Adjust the
[tile size](/neuron-glossary/device-software/tiling) and compare the
profile again.
