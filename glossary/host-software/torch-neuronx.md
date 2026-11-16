---
title: What is torch-neuronx?
short: torch-neuronx
---

**`torch-neuronx`** is the package name shared by native TorchNeuron and the
older PyTorch NeuronX integration. The version tells you which programming
model a recipe expects.

| Build | What it provides in Neuron 2.33.1 |
|---|---|
| `2.13.*` or `2.14.*` | [TorchNeuron](/neuron-glossary/host-software/torchneuron), the native `neuron` device backend in public beta on [Trn2](/neuron-glossary/device-hardware/trn2) and [Trn3](/neuron-glossary/device-hardware/trainium3). Use eager mode or `torch.compile(backend="neuron")`. |
| `2.9.*` | The deprecated PyTorch NeuronX build based on [PyTorch/XLA](/neuron-glossary/host-software/xla). PyTorch 2.9 is the last PyTorch release family for this integration. Neuron 2.33.1 still ships the wheel for existing inference workloads. |

The 2.33.1 package inventory labels the 2.9 wheel as native PyTorch. AWS's
component release notes identify that wheel as PyTorch/XLA and list the
native builds under TorchNeuron.
[Package inventory](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/release-notes/releasecontent.html) · [PyTorch NeuronX release notes](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/release-notes/components/pytorch.html) · [TorchNeuron release notes](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/release-notes/components/torchneuron.html)

`torch-neuron` is the separate legacy package for
[Inf1](/neuron-glossary/device-hardware/inf1).

## Reading older PyTorch/XLA code

In legacy inference code, `torch_neuronx.trace(model, example)` creates a
TorchScript module that embeds a compiled
[NEFF](/neuron-glossary/device-software/neff). It can be saved and reloaded with
`torch.jit.load` and is specialized to the traced input shapes and types. See
[AWS's trace API reference](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.32.0/frameworks/torch/torch-neuronx/api-reference-guide/inference/api-torch-neuronx-trace.html).

In legacy training code, `xm.xla_device()` selects an XLA device. PyTorch/XLA
records operations into a graph until it reaches a boundary such as
`xm.mark_step()` or a read of a tensor value on the host. The graph at that
boundary is the unit of compilation and the input to the
[legacy persistent cache](/neuron-glossary/host-software/neuron-persistent-cache).
AWS directs new PyTorch training on Trn2 and Trn3 to
[TorchNeuron](/neuron-glossary/host-software/torchneuron) and
[TorchTitan Neuron](/neuron-glossary/host-software/torchtitan-neuron).

AWS [announced that XLA inference support on Trn2 and Trn3 ends in Neuron 2.34](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/announcements/neuron2.x/announce-eos-torch-xla-inference-trn.html).
[Inf2](/neuron-glossary/device-hardware/inf2) and
[Trn1](/neuron-glossary/device-hardware/trn1) XLA inference entered
maintenance in Neuron 2.31 and receives critical bug and security fixes.
A move to native TorchNeuron involves updating device placement and
replacing the XLA-specific tracing or training calls.
[AWS Inf2 and Trn1 maintenance announcement](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/announcements/neuron2.x/announce-maintenance-pytorch-xla-inference.html)
