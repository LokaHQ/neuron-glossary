---
title: What is DMA transpose?
short: DMA transpose
---

**DMA transpose** swaps tensor axes during a transfer to
[SBUF](/neuron-glossary/device-hardware/sbuf). The
[DMA engines](/neuron-glossary/device-hardware/dma-engine) can read from
[HBM](/neuron-glossary/device-hardware/hbm) or from SBUF without occupying
a compute engine. On [Trainium2](/neuron-glossary/device-hardware/trainium2),
AWS documents bit-accurate transposes for 2-byte and 4-byte types.
[Trainium2 NKI architecture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium2_arch.html#dma-transpose)

```python
import nki.language as nl
import nki.isa as nisa

# hbm_src: [512, 128]
sbuf_dst = nl.ndarray((128, 512), dtype=hbm_src.dtype, buffer=nl.sbuf)
nisa.dma_transpose(dst=sbuf_dst, src=hbm_src)
```

## Why it is needed

In a packed, row-major HBM matrix, each row is a contiguous run of values.
A straight copy to SBUF puts each row into its own partition. A DMA
transpose puts each source column into its own partition instead.

For example, an attention kernel can store a key cache in HBM as
`[seqlen, d_head]`. The matmul `Q @ K.T` sums over `d_head`, so NKI
needs that axis in the
[partition dimension](/neuron-glossary/device-software/partition-dimension).
The transpose puts the cache tile into SBUF as `[d_head, seqlen]`.

## Trainium2 throughput

| Operation | Share of peak DMA throughput |
|---|---|
| Plain DMA copy | up to 100% |
| HBM→SBUF transpose | up to 90% |
| SBUF→SBUF transpose | up to 50% |

Reaching these rates requires suitable access patterns. On
[Trainium2](/neuron-glossary/device-hardware/trainium2) each
[NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3) is paired
with 16 DMA engines. The fastest transpose access pattern lets all 16 work
together, writing a block of `[128, 16]` at a time. Use all 128 output
partitions and make the innermost free dimension a contiguous multiple of 16
to approach the peak. Smaller tiles and other valid shapes can run at lower
throughput.

## Versus Tensor Engine transpose

The alternative is transposing on the
[Tensor Engine](/neuron-glossary/device-hardware/tensor-engine), either by
multiplying against an identity matrix or, from
[NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3), with a
real transpose mode.

| | DMA transpose | Tensor Engine transpose |
|---|---|---|
| Engine used | DMA only | [Tensor Engine](/neuron-glossary/device-hardware/tensor-engine) |
| Destination | SBUF directly | [PSUM](/neuron-glossary/device-hardware/psum), then must be evicted |
| Source | HBM or SBUF | SBUF |

On Trainium2, a Tensor Engine transpose can be faster by itself. If the next
operation needs the result in SBUF, the
[Vector](/neuron-glossary/device-hardware/vector-engine) or
[Scalar](/neuron-glossary/device-hardware/scalar-engine) engine must copy it
there from PSUM. DMA transpose can save that copy in kernels where those
engines are already busy, for example with attention softmax.

Before [NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3),
Tensor Engine transposes had a correctness hazard as well: multiplying by an
identity propagates `NaN`/`Inf` through the accumulation chain, so the result is
not a bit-accurate transpose. v3's explicit transpose mode fixed that.
