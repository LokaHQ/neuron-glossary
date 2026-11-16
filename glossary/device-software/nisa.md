---
title: What is NISA?
short: Neuron Instruction Set
abbr: NISA
---

**NISA** stands for Neuron Instruction Set Architecture, the instructions
a [NeuronCore](/neuron-glossary/device-hardware/neuroncore) executes.
[NKI](/neuron-glossary/device-software/nki) exposes low-level operations
through `nki.isa`, usually imported as `nisa`.

In [`nki.language`](/neuron-glossary/device-software/nki-language) you
describe the operation, and the compiler selects the instructions. With
`nki.isa` you choose the operation closer to the hardware. Some calls
emit more than one instruction or let you pick the engine. These calls use
tiles already allocated in suitable buffers.

```python
import nki.isa as nisa
import nki.language as nl

nisa.nc_matmul(dst=matmul_psum, stationary=stationary_sbuf, moving=moving_sbuf)
nisa.nc_transpose(dst=transpose_psum, data=input_sbuf, engine=nisa.engine.tensor)
nisa.dma_transpose(dst=transpose_sbuf, src=input_hbm)
nisa.activation(dst=activation_sbuf, op=nl.gelu, data=input_sbuf)
```

Each instruction specifies [tile size limits](/neuron-glossary/device-software/tiling),
operand types and permitted buffers. For example, Tensor Engine matmul
reads SBUF and writes PSUM. [AWS nki.isa API](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/api/nki.isa.html) · [AWS activation API](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/api/generated/nki.isa.activation.html)

## Instruction families

| Family | Examples | Engine |
|---|---|---|
| Matmul | `nc_matmul`, `nc_matmul_mx` | [Tensor](/neuron-glossary/device-hardware/tensor-engine) |
| Transpose | `nc_transpose` | Tensor / Vector |
| Element-wise ops | `tensor_tensor`, `tensor_scalar` | [Vector](/neuron-glossary/device-hardware/vector-engine), with GpSimd and Scalar support depending on the operation |
| Reductions and statistics | `tensor_reduce`, `bn_stats`, `bn_aggr` | Vector |
| On-chip copies | `tensor_copy` | Vector, Scalar or GpSimd, depending on buffers, types and generation |
| Activations | `activation`, `activation_reduce` | [Scalar](/neuron-glossary/device-hardware/scalar-engine), with some `activation` modes on GpSimd on v4 |
| Fast exponential | `exponential` | Vector on v4 |
| Transfers | `dma_copy`, `dma_transpose`, `dma_compute` | [DMA](/neuron-glossary/device-hardware/dma-engine) |
| Selection | `affine_select`, `range_select`, `iota`, `memset` | Vector / GpSimd |
| Quantization | `quantize_mx` | Vector on v4 |

[NKI `tensor_tensor` reference](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/api/generated/nki.isa.tensor_tensor.html) · [NKI `tensor_scalar` reference](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/api/generated/nki.isa.tensor_scalar.html) · [NKI `tensor_copy` reference](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/api/generated/nki.isa.tensor_copy.html) · [NKI `exponential` reference](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/api/generated/nki.isa.exponential.html)

[Collectives](/neuron-glossary/device-software/collectives) have their own
`nki.collectives` namespace.

## Versioning

Instruction modes vary with the target NeuronCore generation.

- `nisa.matmul_perf_mode.double_row` — the double-rate
  [FP8](/neuron-glossary/device-software/cfp8) matmul, from
  [NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3).
- `nisa.nc_matmul(..., is_transpose=True)` — bit-accurate transpose mode, v3.
- `nisa.dge_mode.hwdge` — hardware
  [descriptor generation](/neuron-glossary/device-hardware/dge), v3.
- `nisa.quantize_mx` — [MXFP8](/neuron-glossary/device-software/mxfp8)
  quantization, [v4](/neuron-glossary/device-hardware/neuroncore-v4).

A kernel written against v3 instructions will not necessarily run on
[NeuronCore-v2](/neuron-glossary/device-hardware/neuroncore-v2). To branch
at compile time, query the target:

```python
if nisa.get_nc_version() >= nisa.nc_version.gen3:
    ...
```

This branch resolves during NKI specialization. The resulting kernel uses
the instruction sequence for its target generation.
[AWS get_nc_version API](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/api/generated/nki.isa.get_nc_version.html)
