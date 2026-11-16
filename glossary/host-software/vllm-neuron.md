---
title: What is vLLM Neuron?
short: vLLM Neuron
---

**vLLM Neuron** is the beta `vllm-neuron` plugin for serving supported language
and vision-language models on [Trn2](/neuron-glossary/device-hardware/trn2) and
[Trn3](/neuron-glossary/device-hardware/trainium3). It exposes the standard
vLLM command line, OpenAI-compatible server, and offline `vllm.LLM` API.
Choose a model and serving options from the plugin's recipes.
[vLLM Neuron documentation](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/vllm-neuron/index.html)

```sh
vllm serve "$MODEL" --tensor-parallel-size "$TP_SIZE"
```

Set `MODEL` and `TP_SIZE` from a recipe and include its other serving options.
For example, the online quickstart uses eight
[tensor-parallel workers](/neuron-glossary/perf/tensor-parallelism) for
GPT-OSS 20B. The standalone plugin detects Neuron hardware automatically.
[AWS online quickstart](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/vllm-neuron/docs/getting-started/quickstart-online-serving.html) · [AWS migration guide](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/vllm-neuron/docs/getting-started/migration-nxdi-to-vllm-neuron.html)

## Compilation and serving

In Neuron 2.33 the default compilation route is `neuron_native`. It uses
`libtorch-neuronx-lite` to run compiled graphs on the device. PyTorch captures
the operations as an FX graph, the native backend translates it to
[StableHLO](/neuron-glossary/host-software/xla), and
[`neuronx-cc`](/neuron-glossary/host-software/neuronx-cc) produces
[NEFFs](/neuron-glossary/device-software/neff). Use the full
[`torch-neuronx`](/neuron-glossary/host-software/torch-neuronx) wheel for
eager execution in a PyTorch script.
[AWS compilation routes](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/vllm-neuron/docs/guides/how-to-choose-compilation-route.html) · [AWS native inference guide](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/inference-native-pytorch.html)

Continuous batching lets new requests join while other requests are
running. The plugin uses compiled graphs for a set of batch sizes and
sequence lengths, called shape buckets. A change
to the serving configuration can require compiling new buckets at warmup.
Use the [compiled artifact and trace caches](/neuron-glossary/host-software/neuron-persistent-cache)
to reuse that work across restarts. The plugin can also allocate KV cache
in blocks and reuse blocks for requests with the same prompt prefix.
[AWS feature guide](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/vllm-neuron/docs/guides/features-guide.html) · [Tensor parallelism design](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/vllm-neuron/docs/design/parallelism/tensor_parallelism.html)

Older guides may describe vLLM loading models from
[NxD Inference](/neuron-glossary/host-software/nxd-inference). The standalone
plugin supplies its own model implementations. AWS announced that the
standalone plugin's optional XLA route reaches end of support on Trn2 and
Trn3 in Neuron 2.34.
[AWS vLLM plugin support announcement](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/announcements/neuron2.x/announce-eos-vllm-neuron-torch-xla.html)
