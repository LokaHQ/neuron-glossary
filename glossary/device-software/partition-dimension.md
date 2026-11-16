---
title: What is the partition dimension?
short: Partition dimension
---

The **partition dimension** is the first axis of any
[tile](/neuron-glossary/device-software/tile) in
[SBUF](/neuron-glossary/device-hardware/sbuf) or
[PSUM](/neuron-glossary/device-hardware/psum). These memories have 128 physical
partitions, so the first axis can hold at most 128 entries. In a 2-D tile,
each row occupies one partition.

```python
tile = nl.ndarray((128, 512), dtype=nl.bfloat16, buffer=nl.sbuf)
#                  ^^^ partition dimension, maximum 128
#                       ^^^ free dimension
```

## Why 128

For matrix multiplication, each of the 128 SBUF partitions feeds one row of
processing elements in the
[systolic array](/neuron-glossary/device-hardware/systolic-array). The limit
comes from that physical layout.

## Which axis goes first in a matmul

> In an ordinary, unpacked matmul, put the **contraction dimension** on the
> partition axis of both inputs.

The contraction dimension is the axis you sum over, `K` in
`A[M, K] @ B[K, N]`. To compute this with `nc_matmul`, pass `A`
in `[K, M]` layout and `B`
in `[K, N]` layout. [Double-rate FP8](/neuron-glossary/device-software/cfp8)
and [MX matmul](/neuron-glossary/device-software/mxfp8) pack more than one
contraction element into each partition.
[NKI `nc_matmul` reference](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/api/generated/nki.isa.nc_matmul.html)

For example, an attention kernel can store keys in HBM as `[seqlen, d_head]`.
Computing `Q @ K.T` contracts over `d_head`. A
[DMA transpose](/neuron-glossary/device-software/dma-transpose) can move the
keys to SBUF as `[d_head, seqlen]` in the same transfer.

## Working with it

In current [NKI](/neuron-glossary/device-software/nki), the first axis of the
shape passed to `nl.ndarray` is the partition axis for SBUF and PSUM.
For a leading axis of 300 elements, [tile](/neuron-glossary/device-software/tiling)
it into 128, 128, and 44 elements. A loop over `range(0, 300, 128)` covers
all three, including the final partial tile.
[AWS data representation guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/get-started/about/data-representation-overview.html)

On [NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3), an SBUF
partition holds 224 KiB and a PSUM partition holds 16 KiB. Move completed
matmul results out of PSUM to make room for the next output tiles.
