---
title: What is the Neuron SDK?
short: Neuron SDK
---

The **AWS Neuron SDK** is the software stack for
[Inferentia](/neuron-glossary/device-hardware/inferentia) and
[Trainium](/neuron-glossary/device-hardware/trainium). It connects your model
code or serving engine to the compiler, runtime, and device driver. A Neuron
release bundles components that each have their own version numbers.
[Neuron 2.33.1 release notes](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/release-notes/2.33.1.html)

## Which software should I use?

The table describes Neuron 2.33.1 and notes the separately released SGLang
preview. Start with the row for your workload and instance family.

![Trn2 and Trn3 paths in Neuron 2.33.1. Use TorchNeuron for native PyTorch training or custom inference, TorchTitan Neuron for distributed pretraining, vLLM Neuron for LLM serving, and vLLM Omni Neuron for diffusion and multimodal generation.](themed-image://workload-paths.svg)

| Workload | Where to start |
|---|---|
| PyTorch training or inference in your own script on Trn2 or Trn3 | [TorchNeuron](/neuron-glossary/host-software/torchneuron) runs PyTorch operators in eager mode and can optimize graphs with `torch.compile`. For large-model pretraining, see [TorchTitan Neuron](/neuron-glossary/host-software/torchtitan-neuron). |
| Hugging Face fine-tuning or inference from Python on Trn2 or Trn3 | The upstream Hugging Face libraries can use the native `neuron` device through [TorchNeuron](/neuron-glossary/host-software/torchneuron). |
| Text and vision-language serving on Trn2 and Trn3 | [vLLM Neuron](/neuron-glossary/host-software/vllm-neuron), the standalone plugin. |
| Diffusion and multimodal generation on Trn2 or Trn3 | [vLLM Omni Neuron](/neuron-glossary/host-software/vllm-omni-neuron). |
| SGLang serving on Trainium | The [SGLang-Neuron](/neuron-glossary/host-software/sglang-neuron) preview covers language models on Trn3 and diffusion models on Trn2. |
| JAX training or inference on Inf2, Trn1, Trn2 or Trn3 | [JAX NeuronX](/neuron-glossary/host-software/jax-neuronx) makes Neuron devices available to JAX. |
| Custom kernels | [NKI](/neuron-glossary/device-software/nki), called from a framework or used in model implementations. |
| Existing PyTorch inference on Inf2 or Trn1 | The legacy [PyTorch NeuronX](/neuron-glossary/host-software/torch-neuronx) integration is in maintenance. Deployments that use [NxD Inference](/neuron-glossary/host-software/nxd-inference) are maintained on SDK 2.31. |
| Existing Inf1 inference | See the legacy software listed under [Inf1](/neuron-glossary/device-hardware/inf1). |

## Compiler, runtime and tools

The compiler [`neuronx-cc`](/neuron-glossary/host-software/neuronx-cc) turns a
computation into a device executable called a
[NEFF](/neuron-glossary/device-software/neff). The
[runtime](/neuron-glossary/host-software/neuron-runtime) loads and executes them
through the [driver](/neuron-glossary/host-software/neuron-driver). The
framework decides when to compile and which
[cache](/neuron-glossary/host-software/neuron-persistent-cache) to consult. In
native PyTorch eager mode, the compiler can see one operator at a time. A
serving engine can compile a larger graph and share it across requests
that fit the same input dimensions.

[Deep Learning AMIs and containers](/neuron-glossary/host-software/neuron-dlami)
ship tested combinations. Use [neuron-ls](/neuron-glossary/host-software/neuron-ls)
for device discovery, [neuron-monitor](/neuron-glossary/host-software/neuron-monitor)
for metrics, and [Neuron Explorer](/neuron-glossary/host-software/neuron-explorer)
for profiling.
