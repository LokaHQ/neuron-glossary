---
title: What is tiling?
short: Tiling
---

**Tiling** is splitting a tensor operation into
[tile](/neuron-glossary/device-software/tile)-sized pieces that fit the
hardware's shape limits and on-chip memory. In an NKI kernel, split any
axis that would otherwise need more than 128 on-chip partitions.

## Matmul tile limits

These limits apply to ordinary `nc_matmul` with hardware tiling mode off:

1. **Partition axis ≤ 128.** [SBUF](/neuron-glossary/device-hardware/sbuf)
   has 128 partitions, wired to the 128 rows of the
   [systolic array](/neuron-glossary/device-hardware/systolic-array).
2. **`stationary` free axis ≤ 128**, the number of array columns.
3. **`moving` free axis.** On v2 and v3, the limit is 512 elements for an
   FP32 destination in one [PSUM](/neuron-glossary/device-hardware/psum)
   bank. On v4, the limit is 4,096 for FP32 output or 8,192 for BF16
   output across eight banks.
   [NKI `nc_matmul` reference](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/api/generated/nki.isa.nc_matmul.html),
   [Trainium and Inferentia2 NKI architecture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium_inferentia2_arch.html#tensor-engine)

> **In an unpacked matmul, the contraction dimension maps to the partition
> dimension of both operands.**

That is the axis the array sums over. If a tile arrives with `K` on its free
axis, move `K` to the partition axis before the matmul. You can arrange that
layout in the operation that produces the tile or use a
[transpose](/neuron-glossary/device-software/dma-transpose).

![NeuronCore-v3 matmul tile limits and the wider moving free axis on v4.](themed-image://tiling.svg)

## Tiling a matmul

For `A[M, K] @ B[K, N]`, splitting an output axis and splitting the
contraction axis do different things.

- **`M` and `N`** split into independent tiles with disjoint outputs.
- **`K`** splits into pieces whose results must be summed. Run the first
  `nc_matmul` with `accumulate=False`, then use `accumulate=True` to add
  later products to the same PSUM destination.

For example, unpacked `K = 4096` can use 32 matmuls that accumulate into
one [PSUM](/neuron-glossary/device-hardware/psum) tile, without a separate reduction.

## Choosing sizes

Larger matmul tiles can reuse inputs for more multiply-adds per byte of
[HBM](/neuron-glossary/device-hardware/hbm) traffic, increasing
[arithmetic intensity](/neuron-glossary/perf/arithmetic-intensity). A
128×128 stationary tile uses the full
[Tensor Engine](/neuron-glossary/device-hardware/tensor-engine) array. On
v4 a wider moving tile uses more PSUM banks, leaving less space for other
live outputs.

Budget [SBUF](/neuron-glossary/device-hardware/sbuf) for all live tiles.
Double-buffering needs room for the current tile and the next one so
computation and data transfer can overlap. If the live tiles exceed
capacity, the compiler may [spill](/neuron-glossary/perf/spilling) to HBM.

## Layout decisions

The free axis of the stationary tile becomes the partition axis of the
result. The moving tile supplies the result's free axis. Choose
[stationary and moving](/neuron-glossary/device-software/stationary-and-moving)
roles that put the result in the layout the next operation needs.

Double-rate [FP8](/neuron-glossary/device-software/cfp8) matmul requires
the second axis of both inputs to have length 2. Zero-pad an odd
contraction length before packing.
[MX matmul](/neuron-glossary/device-software/mxfp8) on v4 packs four
contraction elements into each input element and requires a partition
axis of size 32, 64, or 128.
[NKI `nc_matmul_mx` reference](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/api/generated/nki.isa.nc_matmul_mx.html)
