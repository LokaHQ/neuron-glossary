---
title: What are MXFP8 and MXFP4?
short: MXFP8 / MXFP4
---

**MXFP8** and **MXFP4** are Open Compute Project floating-point formats
that store a scale for each small group of values. This is called
**microscaling**. Each group can represent a different range of magnitudes,
which helps when one part of a tensor has much larger values than another.
MXFP4 uses four data bits per value and MXFP8 uses eight, plus the scale
shared by the group.

## On Trainium3

The [NeuronCore-v4 Tensor Engine](/neuron-glossary/device-hardware/neuroncore-v4)
reads one 8-bit scale per 32 elements along the axis the matmul sums over.
It can multiply an MXFP8 matrix by an MXFP4 matrix and apply their scales
in the same instruction. It converts MXFP4 data to MXFP8 before doing the
math. Trainium3 peaks at 2,517 TFLOPS per chip for either format, about four
times its BF16 rate.
[AWS Trainium3 chip specifications](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trainium3.html),
[Trainium3 NKI architecture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium3_arch.html#quad-mxfp8-mxfp4-matmul-performance),
[NeuronCore-v4 architecture](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/neuron-core-v4.html#tensor-engine)

## In NKI

`nki.isa.nc_matmul_mx` reads the stationary and moving tiles from SBUF,
along with one scale tensor for each. Each packed element contains four values
along the contraction axis. At 128 partitions, one matmul therefore
covers 512 contraction elements. The Tensor Engine accumulates in FP32.
The [PSUM](/neuron-glossary/device-hardware/psum) destination can be FP32 with a
moving free dimension of up to 4,096, or BF16 with up to 8,192. Both limits
use all eight PSUM banks.
[NKI `nc_matmul_mx` reference](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/api/generated/nki.isa.nc_matmul_mx.html)

The v4 [Vector Engine](/neuron-glossary/device-hardware/vector-engine) can use
`nki.isa.quantize_mx` to produce MXFP8 data and scales from BF16 or FP16 in
[SBUF](/neuron-glossary/device-hardware/sbuf). This lets a kernel quantize
intermediate activations before the next matmul without moving them through
HBM. Ordinary [FP8](/neuron-glossary/device-software/cfp8) inputs are available
through `nki.isa.nc_matmul`.
[Trainium3 NKI architecture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium3_arch.html#mx-data-type-quantization)
