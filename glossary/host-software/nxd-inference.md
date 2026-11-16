---
title: What is NxD Inference?
short: NxD Inference
abbr: NxDI
---

**NxD Inference** (NeuronX Distributed Inference, or **NxDI**) is the legacy
`neuronx-distributed-inference` library for running inference across Neuron
cores. It implements supported models and uses
[NxD Core](/neuron-glossary/host-software/nxd-core) to split computation and
move data between cores. It also manages the KV cache and supports features
such as continuous batching, quantization, and speculative decoding for
selected models. The legacy **vLLM + NxD Inference** integration loads models
from this library.
[AWS NxDI overview](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/inference-legacy/nxd-inference/overview-index.html)

## Support and migration

NxDI and the NxD Core inference APIs are in maintenance for critical bug
and security fixes. AWS announced an end to that support on Trn2 and Trn3
in Neuron 2.34. On Inf2 and Trn1, maintenance continues on Neuron 2.31.
[AWS inference support announcement](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/announcements/neuron2.x/announce-eos-nxdi-nxd-core-inference.html)

For new text or vision-language serving on Trn2 and Trn3, use the standalone
[vLLM Neuron](/neuron-glossary/host-software/vllm-neuron) plugin. It supplies
its own model implementations and builds executables for the selected
model and serving configuration. For inference from a PyTorch script, use
[TorchNeuron](/neuron-glossary/host-software/torchneuron) with `torch.compile`.
[AWS migration guide](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/vllm-neuron/docs/getting-started/migration-nxdi-to-vllm-neuron.html)
