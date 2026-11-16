---
title: What is cFP8?
short: cFP8
---

**cFP8** stands for configurable FP8, a family of 8-bit floating-point formats
introduced on [NeuronCore-v2](/neuron-glossary/device-hardware/neuroncore-v2).
Each format makes a different tradeoff between exponent bits (range) and
mantissa bits (precision).

| Format | Sign | Exponent | Mantissa | Character |
|---|---|---|---|---|
| `FP8_e5m2` | 1 | 5 | 2 | Widest range, least precision |
| `FP8_e4m3` | 1 | 4 | 3 | Middle ground |
| `FP8_e3m4` | 1 | 3 | 4 | Narrowest range, most precision |

A common training recipe uses `e4m3` for weights and activations and `e5m2`
for gradients, where the wider range can help.

[NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3) adds
**adjustable exponent biasing**, which lets software shift the range toward
the magnitudes in a tensor.
[AWS NeuronCore-v3 architecture](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/neuron-core-v3.html#tensor-engine)

## Trainium2 throughput

On [Trainium2](/neuron-glossary/device-hardware/trainium2), the Tensor Engine
can do twice as much dense matmul work per cycle with E4M3 or E5M2 as with
BF16. AWS publishes these chip and engine peaks separately.

| Scope | BF16 TFLOPS | FP8 TFLOPS |
|---|---|---|
| Per chip | 667 | 1,299 |
| Per [Tensor Engine](/neuron-glossary/device-hardware/tensor-engine) | 79 | 158 |

An FP8 tensor also takes half as many bytes as a BF16 tensor of the same
shape. Keeping weights in FP8 in [HBM](/neuron-glossary/device-hardware/hbm)
can therefore help [memory-bound](/neuron-glossary/perf/memory-bound) decoding.
The end-to-end gain depends on how much time the model spends reading those
weights and what it costs to convert them.
[AWS Trainium2 chip specifications](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trainium2.html)

## How the doubling works

[NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3) doubles the
maximum contraction length of a matmul from 128 to 256 in this mode. Each
processing element in the 128×128
[systolic array](/neuron-glossary/device-hardware/systolic-array) multiplies
two pairs of FP8 values per cycle and adds both products in FP32.

The NKI `nc_matmul` API lists E4M3 and E5M2 as its FP8 inputs on v3.
The Trainium2 architecture guide also documents E3M4 hardware support at the
BF16 rate, but the API's supported input list omits it.
[Trainium2 NKI architecture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium2_arch.html),
[NKI `nc_matmul` reference](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/api/generated/nki.isa.nc_matmul.html)

Invoking it from [NKI](/neuron-glossary/device-software/nki):

```python
# stationary: [128, 2, 128]   moving: [128, 2, 512]
nisa.nc_matmul(dst, stationary, moving, perf_mode=nisa.matmul_perf_mode.double_row)
```

Both operands need a middle axis of exactly 2. Zero-pad an odd contraction
length before packing the operands. On v3, this mode is incompatible with
column tiling,
[sparse matmul](/neuron-glossary/device-software/structured-sparsity), or
transpose mode. See
[stationary and moving](/neuron-glossary/device-software/stationary-and-moving).

## FP8 on Trainium3

[NeuronCore-v4](/neuron-glossary/device-hardware/neuroncore-v4) adds the
Open Compute Project format `float8_e4m3fn` to `nc_matmul`. Both inputs
can use it, or one can pair it with `float8_e5m2`. Legacy `float8_e4m3`
and `float8_e4m3fn` are incompatible in the same call.
[MXFP8 and MXFP4](/neuron-glossary/device-software/mxfp8) use block scales
and a different matmul instruction.
[NKI `nc_matmul` reference](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/api/generated/nki.isa.nc_matmul.html)
