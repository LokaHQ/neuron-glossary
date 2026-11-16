---
title: What is NeuronCore-v3?
short: NeuronCore-v3
---

**NeuronCore-v3** is the third-generation
[NeuronCore](/neuron-glossary/device-hardware/neuroncore) and the core
inside [Trainium2](/neuron-glossary/device-hardware/trainium2). Each chip has
eight physical cores, up from two on chips with
[v2](/neuron-glossary/device-hardware/neuroncore-v2).

## Engines

| Engine | Throughput |
|---|---|
| [Tensor](/neuron-glossary/device-hardware/tensor-engine) | 158 TFLOPS FP8, 79 TFLOPS BF16/FP16/TF32, 20 TFLOPS FP32, up to 316 TFLOPS with structured sparsity |
| [Vector](/neuron-glossary/device-hardware/vector-engine) | 1.0 TFLOPS FP32 |
| [Scalar](/neuron-glossary/device-hardware/scalar-engine) | 1.2 TFLOPS FP32 |
| [GpSimd](/neuron-glossary/device-hardware/gpsimd-engine) | 8 × 512-bit processors |

The data-path width tells you how many elements an engine can accept or return
per clock cycle.

| Engine | Data path (elements/cycle) | Clock |
|---|---|---|
| Tensor | 4×128 dense FP8, 2×128 dense BF16/FP16, 5×128 sparse; 1×128 out | 2.4 GHz |
| Vector | 512 BF16/FP16, 256 other types | 0.96 GHz |
| Scalar | 128 in/out | 1.2 GHz |
| GpSimd | — | 1.2 GHz |

On-chip memory is 28 MiB of [SBUF](/neuron-glossary/device-hardware/sbuf)
(128 partitions × 224 KiB), up from 24 MiB on v2.
[PSUM](/neuron-glossary/device-hardware/psum) stays at 2 MiB.

## What v3 introduced

**Double-rate FP8 matmul.** Each element of the 128×128 array can perform
two `FP8_E4` or `FP8_E5` multiply-accumulates per cycle. A packed
[FP8](/neuron-glossary/device-software/cfp8) instruction can therefore cover
256 values along the contraction dimension, the axis the matmul sums over.
The sum stays in FP32. `FP8_E3` runs at the BF16 rate.

**[Structured sparsity](/neuron-glossary/device-software/structured-sparsity).**
Up to 316 TFLOPS for FP8, BF16, FP16 or TF32 when one input matrix has a
supported pattern of zeros. The patterns are 4:16, 4:12, 4:8, 2:8, 2:4, 1:4,
and 1:2, where M of each N values can be nonzero.

**Bit-accurate transpose.** The v2 Tensor Engine transposed by multiplying by an
identity matrix, which could propagate `NaN` or `Inf` to other positions. The
v3 transpose mode preserves the input bits, runs twice as fast for FP32,
and can write FP16 or BF16 to PSUM so the result is cheaper to copy to SBUF.

**The [Descriptor Generation Engine](/neuron-glossary/device-hardware/dge).**
Dedicated hardware, two instances per core, that generates DMA descriptors on
demand. Previously the host generated them when loading the
[NEFF](/neuron-glossary/device-software/neff) and stored them in HBM, or the
GpSimd Engine generated them while the program ran and stored them in SBUF.

**[DMA transpose](/neuron-glossary/device-software/dma-transpose).** The
DMA engines can transpose while moving, HBM→SBUF or SBUF→SBUF, without
involving a compute engine at all.

**More engine parallelism.** Two v2 restrictions are gone: Vector and GpSimd
can now access SBUF in parallel, and Vector and Scalar can access
[PSUM](/neuron-glossary/device-hardware/psum) in parallel at full
bandwidth, as long as they do not collide on the same PSUM bank.

**Per-processor DMA in GpSimd.** Each of the eight GpSimd processors gets an
integrated DMA engine, 307 GB/s in total across all eight, able to reach any
SBUF or HBM in the instance.

**Adjustable exponent bias** for the
[cFP8](/neuron-glossary/device-software/cfp8) data type.

v3 is also the first core where
[Logical NeuronCore configuration](/neuron-glossary/device-software/logical-neuroncore)
exists, letting two physical v3 cores be addressed as one.
[AWS Trainium2 NKI architecture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium2_arch.html)
