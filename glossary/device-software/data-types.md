---
title: What data types does Neuron support?
short: Data types
---

**Data types** determine how Neuron stores and computes with numbers. The
formats in this table depend on the
[NeuronCore](/neuron-glossary/device-hardware/neuroncore) generation. For a
particular operation, check what its engine, instruction, and framework
accept.
[AWS data type guide](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/about-neuron/arch/neuron-features/data-types.html)

## By generation

| Type | Sign bits | Exponent bits | Mantissa bits | [v1](/neuron-glossary/device-hardware/neuroncore-v1) | [v2](/neuron-glossary/device-hardware/neuroncore-v2) | [v3](/neuron-glossary/device-hardware/neuroncore-v3) | [v4](/neuron-glossary/device-hardware/neuroncore-v4) |
|---|---|---|---|---|---|---|---|
| FP32 | 1 | 8 | 23 | yes | yes | yes | yes |
| TF32 | 1 | 8 | 10 | — | yes | yes | yes |
| BF16 | 1 | 8 | 7 | yes | yes | yes | yes |
| FP16 | 1 | 5 | 10 | yes | yes | yes | yes |
| FP8_e5m2 | 1 | 5 | 2 | — | yes | yes | yes |
| FP8_e4m3 | 1 | 4 | 3 | — | yes | yes | yes |
| FP8_e3m4 | 1 | 3 | 4 | — | yes | yes | yes |
| UINT8 | — | — | — | — | yes | yes | yes |
| INT32 / UINT32 | 1 / 0 | — | — | — | yes | yes | yes |
| INT64 / UINT64 | 1 / 0 | — | — | — | — | yes | yes |
| `float8_e4m3fn` (OCP FP8) | 1 | 4 | 3 | — | — | — | yes |
| [MXFP8 / MXFP4](/neuron-glossary/device-software/mxfp8) | | | | — | — | — | yes |

The first three FP8 rows are [cFP8](/neuron-glossary/device-software/cfp8),
or configurable FP8. The v4 Tensor Engine also accepts the OCP format
`float8_e4m3fn`, which has a different encoding from legacy E4M3 despite
having the same bit counts.
[NKI `nc_matmul` reference](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/api/generated/nki.isa.nc_matmul.html)

![Bit layouts for selected numeric formats. In the floating-point formats shown, exponent bits provide range and mantissa bits provide precision.](themed-image://data-type-bits.svg)

## Automatic casting

Since **Neuron SDK 2.27**, `neuronx-cc` keeps the input type of matrix
multiplications by default (`--auto-cast=none`). Older releases cast FP32
matrix multiplications to BF16 by default. To request that behavior, pass
`--auto-cast=matmult --auto-cast-type=bf16` and check model accuracy.
[AWS compiler guide](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/compiler/index.html)

This compiler default is distinct from the dtype chosen by the model and
from framework mixed precision, such as `torch.autocast(device_type="neuron")`
in [TorchNeuron](/neuron-glossary/host-software/torchneuron). The legacy Inf1
compiler has its own precision defaults.

## Integer conversions

Matrix multiplication, scatter that accumulates into its destination,
all-reduce and reduce-scatter lack a native integer datapath. When the compiler
permits downcasting, these can run in FP32 and lose precision; integer power
can narrow `int64` to `int32`.

In Neuron 2.33.1 the compiler still defaults to narrowing `int64` for
execution. On [Trn2](/neuron-glossary/device-hardware/trn2) and later,
`--native-int64=enabled` preserves 64-bit integers where supported. Earlier
targets narrow them. Use `--implicit-integer-downcast=none` to reject lossy
conversions for operations without the required integer datapath. Check the
[CLI reference](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/compiler/neuronx-cc/api-reference-guide/index.html)
and [compiler release notes](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/release-notes/components/compiler.html)
for the exact rules and the planned default change.

## Which to use

For **inference**, lower precision can reduce weight and KV traffic when
serving is [memory-bound](/neuron-glossary/perf/memory-bound). It can also
raise peak compute throughput on a supported engine. Check the model recipe
and measure the accuracy and throughput of the complete workload.

For **training**, BF16 is a common starting point. Accumulation precision,
optimizer state, and [stochastic rounding](/neuron-glossary/device-software/rounding-mode)
are separate decisions. Keep higher precision where the workload requires it.
