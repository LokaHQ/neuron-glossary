---
title: What is transformers-neuronx?
short: transformers-neuronx
abbr: TNx
---

**`transformers-neuronx`** (TNx) was AWS's earlier library for running
transformer decoders across [NeuronCores](/neuron-glossary/device-hardware/neuroncore).
It provided tensor-parallel implementations for common model families and
appears in older deployment recipes for Inf2, Trn1 and Trn2.

AWS put TNx in maintenance in Neuron 2.24 and ended support in 2.26.
Its successor was [NxD Inference](/neuron-glossary/host-software/nxd-inference).
The migration guide covers the changes to Python model APIs, compiled
artifacts, and serving settings.
[AWS support announcement](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.30.0/about-neuron/announcements/neuron2.x/announce-intent-eos-tnx.html) · [TNx-to-NxDI migration guide](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/inference-legacy/nxd-inference/developer_guides/migrate-from-tnx-to-nxdi.html)

On Trn2 and Trn3, the standalone
[vLLM Neuron](/neuron-glossary/host-software/vllm-neuron) plugin serves text
and vision-language models. To run upstream Hugging Face Transformers for
inference or fine-tuning from Python, use the native `neuron` device in
[TorchNeuron](/neuron-glossary/host-software/torchneuron).
