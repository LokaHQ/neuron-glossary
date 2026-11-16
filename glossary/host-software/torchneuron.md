---
title: What is TorchNeuron?
short: TorchNeuron
---

**TorchNeuron** is the native PyTorch backend for
[Trn2](/neuron-glossary/device-hardware/trn2) and
[Trn3](/neuron-glossary/device-hardware/trainium3), in public beta as of
Neuron 2.33.1. It gives PyTorch a `neuron` device so you can place a model
and its tensors on Trainium with ordinary PyTorch calls. It registers the
device through PyTorch's `PrivateUse1` extension point. Match your PyTorch
2.13 or 2.14 version to the native
[`torch-neuronx`](/neuron-glossary/host-software/torch-neuronx) wheel family.
[AWS TorchNeuron overview](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/torch/about-pytorch-neuron.html) · [TorchNeuron release notes](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/release-notes/components/torchneuron.html)

## Hugging Face ecosystem

On Trn2 and Trn3, upstream **Transformers**, **Accelerate**, **PEFT**, **TRL**,
and **Diffusers** can use the native PyTorch `neuron` device for supported
workloads. Hugging Face documents these examples.

| Workload | Where to start |
|---|---|
| Transformers inference | Pass `device_map="neuron"` to `from_pretrained()`. For supported text generation, a static KV cache keeps the attention state at a fixed shape as the sequence grows and reduces recompilation. [Transformers on AWS Trainium](https://huggingface.co/docs/transformers/main/aws_trainium#run-inference) |
| Fine-tuning and post-training | Transformers `Trainer` detects Neuron through Accelerate. PEFT adds support for adapter fine-tuning. The TRL recipe fine-tunes Qwen3-8B on Trainium2 with `SFTTrainer`, fixed input shapes, tensor parallelism, and Fully Sharded Data Parallel (FSDP). [Trainer guide](https://huggingface.co/docs/transformers/main/aws_trainium#train-with-trainer) · [TRL recipe](https://huggingface.co/blog/hf-torchneuron#training) |
| Diffusion and custom kernels | Supported Diffusers pipelines run in eager and compiled mode. AWS publishes [NKI](/neuron-glossary/device-software/nki) kernels for use through Hugging Face Kernels. [Diffusers on Trainium](https://huggingface.co/docs/diffusers/optimization/neuron) · [AWS Neuron kernels on the Hub](https://huggingface.co/aws-neuron/kernels) |

Model and feature coverage depends on the workload and package versions. The
[TorchNeuron compatibility lookup](https://huggingface.co/spaces/aws-neuron/torch-neuronx-model-support)
lists tested Transformers inference configurations and their reproduction
scripts. [Optimum Neuron](https://huggingface.co/docs/optimum-neuron/index)
provides separate model wrappers and export workflows for the earlier
PyTorch/XLA stack. [`transformers-neuronx`](/neuron-glossary/host-software/transformers-neuronx)
is AWS's retired decoder library.

## Eager and compiled execution

```python
import torch

model = torch.nn.Linear(16, 8).to("neuron")
x = torch.ones(2, 16, device="neuron")
y = model(x)  # Eager
compiled = torch.compile(model, backend="neuron")
z = compiled(x)  # Compiles on the first call for this signature
```

**Eager mode** dispatches PyTorch operators as Python calls them. TorchNeuron
translates a supported operator into [StableHLO](/neuron-glossary/host-software/xla),
compiles a device executable called a
[NEFF](/neuron-glossary/device-software/neff) on a cache miss, and queues it on
the device. Opt-in Adaptive Eager Execution can fuse eligible queued
operations. By default, an unsupported eager operator can fall back to CPU
with a warning, incurring synchronization and data transfers.
[AWS eager execution guide](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/torch/about-pytorch-neuron.html)

**`torch.compile`** uses TorchDynamo to record related PyTorch operations as a
graph in PyTorch's FX format. The Neuron backend lowers each captured graph
through StableHLO and
[`neuronx-cc`](/neuron-glossary/host-software/neuronx-cc) to a NEFF. This
lets the compiler optimize across operators. Graph breaks can split capture
into separate graphs. If lowering or execution fails, the backend raises by
default. You can enable a fallback that reruns the original graph in eager
mode, where the eager operator fallback rules apply. Different input shapes
can trigger recompilation.
[AWS compilation guide](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/torch/compile/about-torch-compile.html) · [Compilation caches](/neuron-glossary/host-software/neuron-persistent-cache)

## Distributed training and custom kernels

TorchNeuron uses standard `torch.distributed` APIs, including DDP, FSDP and
DTensor tensor parallelism, with the `neuron` process group backend. For
large-model pretraining, [TorchTitan Neuron](/neuron-glossary/host-software/torchtitan-neuron)
provides tested recipes and a compiler-friendly SimpleFSDP option. Use
[NKI](/neuron-glossary/device-software/nki) for a custom device kernel inside
an otherwise standard PyTorch model. See the [distributed guide](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/torch/guides/torch-distributed.html).
