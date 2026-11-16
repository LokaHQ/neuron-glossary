---
title: What is SGLang-Neuron?
short: SGLang-Neuron
---

**SGLang-Neuron** is a plugin that lets the SGLang serving engine run models
on Trainium through [TorchNeuron](/neuron-glossary/host-software/torchneuron).
Version 0.1.0 launched as a public preview on November 12, 2026, with its own
container. On [Trn3](/neuron-glossary/device-hardware/trainium3), the preview
can run the prompt and token generation phases of language models on
separate workers (prefill/decode disaggregation). On
[Trn2](/neuron-glossary/device-hardware/trn2), it runs supported models using
SGLang Diffusion.

The preview covers models such as GPT-OSS-120B for text generation and
FLUX.1-dev and Wan2.2 A14B for diffusion. See the supported configurations
and container tag in the release notes for this preview.
[SGLang-Neuron release notes](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/release-notes/components/sglang-plugin.html)
