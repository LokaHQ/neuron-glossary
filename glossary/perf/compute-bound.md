---
title: What does compute-bound mean?
short: Compute-bound
---

An operation is **compute-bound** when the rate of arithmetic sets its
runtime. For example, a well-tiled matrix multiplication can reuse its inputs
enough to keep the [Tensor Engine](/neuron-glossary/device-hardware/tensor-engine)
busy even though it only loads each input tile from device memory occasionally.

The [roofline model](/neuron-glossary/perf/roofline-model) predicts a compute
limit when [arithmetic intensity](/neuron-glossary/perf/arithmetic-intensity)
exceeds the machine balance. Use the peak for the engine doing the work and
the bandwidth for the memory being accessed. Large matrix multiplications,
convolutions, and long-prompt prefill can hit this limit when they reuse
their inputs enough.

## Prefill and decode have different reuse patterns

LLM inference often shifts from compute-bound prefill to memory-bound decode.
The actual bottleneck depends on the model, prompt length, context length, batch,
and implementation.

| | Prefill | Decode |
|---|---|---|
| Work | Process prompt tokens, sometimes in chunks | Generate one token per sequence per step |
| Weight reuse | Across the prompt tokens in a chunk | Across sequences in the batch |
| Common bottleneck | Compute on long prompts | [Memory](/neuron-glossary/perf/memory-bound) at small batches |
| Helped by | Faster matmul, [sparsity](/neuron-glossary/device-software/structured-sparsity) | Quantization, batching |

With **disaggregated inference**, separate worker pools handle prefill and
decode. The prefill worker passes the KV cache, which holds attention keys and
values for the prompt, to the decode worker. The serving system can size each
pool independently. See the [vLLM Neuron disaggregation tutorial](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/vllm-neuron/docs/tutorials/tutorial-di-1p1d-xpyd.html)
for supported configurations.

![Prefill reuses weights across prompt tokens. Decode can be bandwidth-bound at small batches. An 8B BF16 model at batch 1 on Trainium2 has a weight-only bandwidth ceiling of about 180 tokens/s.](themed-image://prefill-decode.svg)

## When arithmetic sets the limit

- **Use a supported lower-precision format.**
  [FP8](/neuron-glossary/device-software/cfp8) matmul can reach about twice
  the per-engine BF16 peak on
  [NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3).
  [MXFP8](/neuron-glossary/device-software/mxfp8) can reach about four times
  the per-engine BF16 peak on
  [NeuronCore-v4](/neuron-glossary/device-hardware/neuroncore-v4).
- **Use [structured sparsity](/neuron-glossary/device-software/structured-sparsity)**
  if your model meets a supported zero pattern and your kernel selects the
  sparse matmul path. Speedups depend on generation and data type.
- **Check [tile geometry](/neuron-glossary/device-software/tiling).** A kernel
  limited by arithmetic can still fall short of the published peak if it
  leaves part of the array idle.

Use [Neuron Explorer](/neuron-glossary/host-software/neuron-explorer) to see
which engine is busy. A normalization kernel can saturate the Vector Engine
while leaving the Tensor Engine idle. The Tensor Engine's peak is then a
poor baseline for that kernel.
