---
title: What is a tile?
short: Tile
---

A **tile** is a rectangular chunk of a tensor, sized to fit in on-chip memory
and meet the shape limits of the instruction that will use it. Tensor
instructions on a [NeuronCore](/neuron-glossary/device-hardware/neuroncore)
take tiles as inputs or destinations.

A typical [NKI](/neuron-glossary/device-software/nki) kernel loads tiles,
computes on them and stores the results.

A tile in [SBUF](/neuron-glossary/device-hardware/sbuf) or
[PSUM](/neuron-glossary/device-hardware/psum) has one
[partition dimension](/neuron-glossary/device-software/partition-dimension)
and one or more [free dimensions](/neuron-glossary/device-software/free-dimension).
The first axis can use up to 128 physical partitions. The other axes describe
the values within each partition.

```python
# A BF16 moving tile for a matmul on NeuronCore-v3.
tile = nl.ndarray((128, 512), dtype=nl.bfloat16, buffer=nl.sbuf)
```

In a standard matmul, each input has a different role and a different
limit on its free dimension.

| Constraint | Limit | Source |
|---|---|---|
| Partition axis | 128 | SBUF partitions, [systolic array](/neuron-glossary/device-hardware/systolic-array) rows |
| `stationary` free axis | 128 | systolic array columns |
| `moving` free axis, v2 and v3 | 512 | one FP32 PSUM bank per partition |
| `moving` free axis, v4 | 4,096 (FP32 output) or 8,192 (BF16 output) | up to eight PSUM banks per partition |
| Total live SBUF data, v2–v4 | 24–32 MiB per core | [SBUF](/neuron-glossary/device-hardware/sbuf) capacity |

Matmul tiles must meet the size limits for the target instruction. If live
intermediates exceed available SBUF, the compiler may
[spill](/neuron-glossary/perf/spilling) them to HBM.
[NKI `nc_matmul` reference](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/api/generated/nki.isa.nc_matmul.html)

## Pipelining tiles

A GPU can hide memory latency by running another warp while one waits for
data. On Neuron, the kernel or compiler can overlap explicit
[DMA](/neuron-glossary/device-hardware/dma-engine) transfers with
computation. With enough buffer space and independent work, a pipeline
can look like this.

```
load tile n+1   (DMA, in background)
compute tile n  (Tensor Engine)
store tile n-1  (DMA, in background)
```

See [latency hiding](/neuron-glossary/perf/latency-hiding) for how these
transfers can overlap.

Tile size is also the main lever on
[arithmetic intensity](/neuron-glossary/perf/arithmetic-intensity) in matmul.
A larger tile can reuse its inputs for more operations per byte fetched from
[HBM](/neuron-glossary/device-hardware/hbm).

For how to choose tile shapes, see
[tiling](/neuron-glossary/device-software/tiling).
