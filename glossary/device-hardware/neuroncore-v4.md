---
title: What is NeuronCore-v4?
short: NeuronCore-v4
---

**NeuronCore-v4** is the compute core in
[Trainium3](/neuron-glossary/device-hardware/trainium3), with eight physical
cores per chip. Each has 32 MiB of software-managed
[SBUF](/neuron-glossary/device-hardware/sbuf) and 2 MiB of
[PSUM](/neuron-glossary/device-hardware/psum).

| Engine | Peak throughput or configuration |
|---|---|
| [Tensor](/neuron-glossary/device-hardware/tensor-engine) | 315 MXFP8/MXFP4 TFLOPS, 79 BF16/FP16/TF32 TFLOPS, 20 FP32 TFLOPS |
| [Vector](/neuron-glossary/device-hardware/vector-engine) | 1.2 TFLOPS FP32 |
| [Scalar](/neuron-glossary/device-hardware/scalar-engine) | 1.2 TFLOPS FP32 |
| [GpSimd](/neuron-glossary/device-hardware/gpsimd-engine) | Eight 512-bit programmable processors |

## Changes from v3

- **[MXFP8 and MXFP4](/neuron-glossary/device-software/mxfp8).** The
  Tensor Engine handles both microscaling inputs at up to four times its
  BF16 throughput. FP8 without microscaling remains supported by
  `nc_matmul`, including OCP `float8_e4m3fn` on v4.
- **Wider matmul outputs.** An output tile from `nc_matmul` can span eight
  PSUM banks, with up to 4,096 elements per partition for FP32 or 8,192 for
  BF16. The Tensor Engine still adds the products in FP32 and casts the
  result before writing a BF16 output.
- **DMA accumulation into SBUF.** A DMA transfer can add to existing SBUF
  data in a single read-add-write operation. The Trainium3 architecture
  guide documents this hardware feature as having no `nki.isa` API in
  Neuron 2.33.1.
- **Vector Engine quantization and exponential.** The Vector Engine can
  quantize BF16/FP16 tensors to MXFP8 and evaluate exponential at four times the
  Scalar Engine's exponential rate.

The NKI guide identifies FP8, FP16, BF16, TF32, FP32, INT8, INT16 and INT32 as
supported input/output data types for the v4 Vector and Scalar engines. Check
the specific instruction for its supported data types.
[Trainium3 NKI architecture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium3_arch.html),
[NKI `nc_matmul` reference](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/api/generated/nki.isa.nc_matmul.html),
[NeuronCore-v4 architecture](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/neuron-core-v4.html)
