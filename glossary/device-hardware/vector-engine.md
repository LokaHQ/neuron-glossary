---
title: What is the Vector Engine?
short: Vector Engine
---

The **Vector Engine** (VectorE) handles operations that combine values,
such as summing a row for softmax or adding two tensors element by element.

Reductions in normalization and softmax do little arithmetic per byte
moved. They can limit a kernel's throughput even when the
[Tensor Engine](/neuron-glossary/device-hardware/tensor-engine) has capacity
to spare. See [arithmetic intensity](/neuron-glossary/perf/arithmetic-intensity).

It can read and write both
[SBUF](/neuron-glossary/device-hardware/sbuf) and
[PSUM](/neuron-glossary/device-hardware/psum). After the Tensor Engine
writes a matrix multiplication result to PSUM, the Vector Engine can move
it to SBUF and make room for the next result.

Throughput by generation:

| | [v1](/neuron-glossary/device-hardware/neuroncore-v1) | [v2](/neuron-glossary/device-hardware/neuroncore-v2) | [v3](/neuron-glossary/device-hardware/neuroncore-v3) | [v4](/neuron-glossary/device-hardware/neuroncore-v4) |
|---|---|---|---|---|
| FP32 | 256 FLOP/cycle | 2.3 TFLOPS | 1.0 TFLOPS | 1.2 TFLOPS |

AWS reports about 10× higher throughput from v1 to v2. The table shows
per-core figures. A v3 chip has four times as many cores as a v2 chip.

The Trainium3 NKI guide lists FP8, FP16, BF16, TF32, FP32, INT8, INT16 and
INT32 for v4 Vector Engine inputs and outputs. Individual instructions have
their own data type requirements.
[Trainium3 NKI architecture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium3_arch.html#vector-engine)

## Performance mode

On [NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3) the
Vector Engine has a BF16/FP16 performance mode that gives up to **4×** the v2
instruction throughput for selected instructions. The engine still does the
arithmetic in FP32.

The hardware selects the mode automatically based on the instruction,
where its inputs and outputs live, their types and their layout.

- **4× for `tensor_copy` and `tensor_scalar`** when both input and output are
  in SBUF, both are BF16 or FP16, and the innermost free dimension is
  physically contiguous.
- **2× for `tensor_copy` and `tensor_scalar`** when either side is in PSUM
  with the same type and layout conditions, or when both are in SBUF and
  BF16/FP16 with a noncontiguous innermost free dimension.
- **2× for `tensor_tensor`** when both inputs are in SBUF and everything is
  BF16/FP16.

This mode uses a memory bus shared by the Vector and
[GpSimd](/neuron-glossary/device-hardware/gpsimd-engine) engines, with the
hardware deciding which engine can use it.

On [NeuronCore-v4](/neuron-glossary/device-hardware/neuroncore-v4) the
Vector Engine gains two more capabilities: quantizing BF16/FP16 down to
[MXFP8](/neuron-glossary/device-software/mxfp8), useful between MLP layers,
and a **fast exponential at 4× the throughput of `exp` on the
[Scalar Engine](/neuron-glossary/device-hardware/scalar-engine)** for
operations such as attention softmax.
[Trainium2 NKI architecture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium2_arch.html#vector-engine)
