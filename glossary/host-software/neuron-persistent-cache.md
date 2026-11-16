---
title: What is the Neuron persistent cache?
short: Neuron persistent cache
---

The **Neuron Persistent Cache** saves compiled
[NEFFs](/neuron-glossary/device-software/neff) from the legacy PyTorch/XLA
and Transformers NeuronX stacks. When a later run needs the same executable,
it can load the file and skip compilation. Native TorchNeuron and vLLM
Neuron have their own caches with different settings.

## Which cache applies?

| Stack | What it saves and how to configure it |
|---|---|
| Legacy PyTorch/XLA lazy execution and `transformers-neuronx` | The [Neuron Persistent Cache](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/about-neuron/arch/neuron-features/neuron-caching.html) stores compiler results in `/var/tmp/neuron-compile-cache` by default. Select a local directory or S3 URI with `NEURON_COMPILE_CACHE_URL` or the wrapper's `NEURON_CC_FLAGS=--cache_dir=...`. The lazy path also has a per-process JIT cache. The persistent cache excludes graphs created with `torch_neuronx.trace` when weights are frozen. |
| Native [TorchNeuron](/neuron-glossary/host-software/torchneuron) | The [native backend](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/torch/compile/reference-torch-compile.html#caching-configuration) has a content-addressed NEFF cache (`TORCH_NEURONX_NEFF_CACHE_DIR`, default `/tmp/neff_cache`) and an HLO cache shared by eager and compiled execution (`TORCH_NEURONX_HLO_CACHE_DIR`). An optional Dynamo precompile cache (`TORCH_CACHING_PRECOMPILE`) can reuse work from graph capture. Use a shared NEFF cache across instances and keep `TORCH_NEURONX_NEFF_LOCAL_CACHE_DIR` for local locks and scratch. |
| Standalone [vLLM Neuron](/neuron-glossary/host-software/vllm-neuron) | The plugin's [compilation cache](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/vllm-neuron/docs/design/compilation/compilation_cache.html) stores compiled graphs locally by default under `$VLLM_CACHE_ROOT/neuron/compile_cache` and supports an optional shared NFS or FSx tier (`NEURON_LIBTORCH_REMOTE_CACHE`). The native route also saves graph traces in its [Precompile Cache](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/vllm-neuron/docs/guides/how-to-precompile-cache.html) to speed up startup. |
| Legacy [NxD Inference](/neuron-glossary/host-software/nxd-inference) | `NEURON_COMPILED_ARTIFACTS` selects a directory with a precompiled model export. [Legacy integration guide](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/inference-legacy/nxd-inference/developer_guides/migrate-from-tnx-to-nxdi.html#compiling-and-loading-the-model) |

For [JAX NeuronX](/neuron-glossary/host-software/jax-neuronx), use the cache
settings for your installed JAX and PJRT versions.

## Preparing a deployment

Warm up the exact model and serving configuration you intend to deploy, then
verify a restart can find the artifacts. Shapes, dtypes, compiler options,
compiler versions, or the target can change the graph or cache key. A warm
startup can reuse compiled code and still has to load weights and initialize
the server. A serving KV cache stores attention state for requests.
