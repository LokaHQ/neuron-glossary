---
title: What is the free dimension?
short: Free dimension
---

The **free dimensions** of a [tile](/neuron-glossary/device-software/tile)
are the axes after the first. The
[partition dimension](/neuron-glossary/device-software/partition-dimension)
maps the first axis across physical partitions. The free dimensions
describe the elements within each partition.

```python
tile = nl.ndarray((128, 512), dtype=nl.bfloat16, buffer=nl.sbuf)
#                       ^^^ free dimension
```

The free dimensions can be wider than 128. A tile of shape `(128, 4, 512)`
has two free axes and puts `4 × 512` elements in each partition.

## Capacity and matmul limits

- **Partition capacity.** 192 KiB per SBUF partition on
  [NeuronCore-v2](/neuron-glossary/device-hardware/neuroncore-v2), 224 KiB
  on [v3](/neuron-glossary/device-hardware/neuroncore-v3), and 256 KiB
  on [v4](/neuron-glossary/device-hardware/neuroncore-v4). All free
  dimensions together must fit.
- The **`moving` free axis of a matmul** is at most 512 elements on v2 and
  v3, fitting one [PSUM](/neuron-glossary/device-hardware/psum) bank for FP32
  output. On v4 it can use eight banks for up to 4,096 elements with FP32
  output or 8,192 with BF16.
  [NKI `nc_matmul` reference](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/api/generated/nki.isa.nc_matmul.html),
  [Trainium and Inferentia2 NKI architecture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium_inferentia2_arch.html#tensor-engine)
- The **`stationary` free axis** can hold 128 elements, one for each of the
  [systolic array](/neuron-glossary/device-hardware/systolic-array)
  columns.

## Why the ordering matters

The innermost free axis is the fastest-varying one in a packed tile. On
Trainium2, [Vector Engine](/neuron-glossary/device-hardware/vector-engine)
`tensor_copy` and `tensor_scalar` on BF16 or FP16 SBUF tiles can run at
4× v2 throughput when that axis is contiguous in both operands. With the
same types and buffers but a strided axis, the documented gain is 2×.
Contiguous runs also give the
[DMA engines](/neuron-glossary/device-hardware/dma-engine) larger chunks
to transfer.
[Trainium2 NKI architecture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium2_arch.html#vector-engine-performance-mode)

## In matmul output

The free axis of the `moving` tensor becomes the free axis of the output, while
the free axis of the `stationary` tensor becomes the output's **partition**
axis. You can [choose the roles](/neuron-glossary/device-software/stationary-and-moving)
to put the output in the layout the next operation expects.
