---
title: What is the Tensor Engine?
short: Tensor Engine
---

The **Tensor Engine** (TensorE) is the matrix multiplication unit in a
[NeuronCore](/neuron-glossary/device-hardware/neuroncore). Its peak rate
depends on the input format. On
[NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3), for example,
it can reach 79 TFLOPS for BF16 matrix multiplication if data arrives fast
enough to keep the array busy.

It uses a [systolic array](/neuron-glossary/device-hardware/systolic-array),
a grid of **128 × 128 processing elements** on NeuronCore-v2 through v4.
It handles general matrix multiplication
(GEMM), convolution, and transpose. It plays a role similar to NVIDIA's
[Tensor Cores](https://modal.com/gpu-glossary/device-hardware/tensor-core).

## Where inputs and outputs go

**The Tensor Engine reads only from
[SBUF](/neuron-glossary/device-hardware/sbuf) and writes only to
[PSUM](/neuron-glossary/device-hardware/psum).** A typical matmul kernel loads
a tile from [HBM](/neuron-glossary/device-hardware/hbm) into SBUF, computes
into PSUM, then uses the
[Vector](/neuron-glossary/device-hardware/vector-engine) or
[Scalar](/neuron-glossary/device-hardware/scalar-engine) engine to copy the
finished result back to SBUF and make room for the next output.

Floating-point matmul accumulates in FP32 inside the Tensor Engine. The ordinary matmul
destination is FP32 on [NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3). [NeuronCore-v4](/neuron-glossary/device-hardware/neuroncore-v4)
also supports a BF16 destination, rounding on each write to PSUM. The v3
transpose mode supports 16-bit destinations.
[Trainium3 NKI architecture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium3_arch.html)

## Stationary and moving

One NKI matmul call typically appears as two hardware instructions.

1. **`LoadStationary`** loads one matrix from SBUF and caches it inside the
   array.
2. **`MultiplyMoving`** streams the second matrix across it, producing output
   into PSUM.

So `nki.isa.nc_matmul(dst, stationary, moving)` computes `stationary.T @ moving`.
The free axis of `stationary` becomes the output's *partition* axis, while
the free axis of `moving` becomes the output's free axis. Choosing the order
that the next operation expects can save a
[transpose](/neuron-glossary/device-software/dma-transpose). See
[stationary and moving](/neuron-glossary/device-software/stationary-and-moving).

## Tile size limits

For a standard `nc_matmul` tile with hardware tiling mode off, the limits are:

| Constraint | Limit | Why |
|---|---|---|
| `stationary` free axis | 128 | columns of processing elements |
| Partition axis, both inputs | 128 | rows of PEs, and SBUF partitions |
| `moving` free axis, v2 and v3 | 512 | one FP32 PSUM bank per partition |
| `moving` free axis, v4 | 4,096 (FP32 output) or 8,192 (BF16 output) | up to eight PSUM banks per partition |

Anything larger must be [tiled](/neuron-glossary/device-software/tiling)
into multiple `nc_matmul` calls. Splitting either output axis gives
independent output tiles. Splitting the contraction dimension `K`, the
axis that gets summed over, yields partial results that accumulate in the
same PSUM location.

Large tiles generally make better use of the array. Choosing the widest
moving tile trades PSUM capacity for work per call.
[NKI `nc_matmul` reference](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/api/generated/nki.isa.nc_matmul.html)

## Using it for data movement

Because the array multiplies by whatever you load, you can construct
matrices of zeros and ones to rearrange or combine data.

- **Transpose.** On v2, multiplying by an identity matrix transposes the
  input but can propagate `NaN` or `Inf` to other positions. Starting with
  [v3](/neuron-glossary/device-hardware/neuroncore-v3), Tensor Engine
  transpose preserves the input bits.
- **Broadcast.** Multiplying by a vector of ones repeats values across
  partitions.
- **Cross-partition sum.** A single column of the array can sum values
  along the partition axis.

These operations occupy the Tensor Engine. A
[DMA transpose](/neuron-glossary/device-software/dma-transpose) can move
data and transpose it at the same time, leaving the Tensor Engine available
for matrix multiplication.
[NKI `nc_transpose` reference](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/api/generated/nki.isa.nc_transpose.html)

## Per-generation throughput

| | [v1](/neuron-glossary/device-hardware/neuroncore-v1) | [v2](/neuron-glossary/device-hardware/neuroncore-v2) | [v3](/neuron-glossary/device-hardware/neuroncore-v3) | [v4](/neuron-glossary/device-hardware/neuroncore-v4) |
|---|---|---|---|---|
| BF16/FP16 | 16 TFLOPS | 92 | 79 | 79 |
| FP8-class support | — | cFP8 | 158 TFLOPS FP8 | 315 TFLOPS MXFP8/MXFP4 |
| FP32 | — | 23 | 20 | 20 |
| Structured sparsity | — | — | up to 316 TFLOPS (FP8/FP16/BF16/TF32) | up to 315 TFLOPS (FP16/BF16/TF32) |

[Trainium2 NKI architecture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium2_arch.html#tensor-engine),
[NeuronCore-v4 architecture](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/neuron-core-v4.html#tensor-engine)

Several instruction pairs can be in flight at once. For a stream of matmuls,
throughput depends on the **initiation interval**, the time between issuing
successive instructions.
