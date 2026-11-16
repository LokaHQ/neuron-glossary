---
title: What is vLLM Omni Neuron?
short: vLLM Omni Neuron
---

**vLLM Omni Neuron** is the beta `vllm-omni-neuron` plugin for vLLM Omni on
[Trn2](/neuron-glossary/device-hardware/trn2) and
[Trn3](/neuron-glossary/device-hardware/trainium3). It serves diffusion and
other multimodal generation models. For example, the Neuron 2.33 recipes
use Wan2.2 A14B to generate video from a text prompt or an image. Run
generation in Python with `Omni.generate` or send a request to the
`/v1/videos` endpoint.

The 2.33 release compiles model graphs through `libtorch-neuronx-lite`
and ships optimized [NKI kernels](/neuron-glossary/device-software/nki).
Depending on the model, a recipe can split attention across a long video
sequence or split the variational autoencoder (VAE) across devices.
[Plugin release notes](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/release-notes/components/vllm-omni-neuron.html) · [Native inference guide](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/inference-native-pytorch.html) · [Model recipes](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/vllm-omni-neuron/docs/index.html)

For text generation and vision understanding, see the
[vLLM Neuron](/neuron-glossary/host-software/vllm-neuron) plugin.
