---
title: What are Neuron custom C++ operators?
short: Custom C++ operators
---

The legacy **Custom C++ operators** feature runs PyTorch operators written in
C++ on a Neuron [GpSimd Engine](/neuron-glossary/device-hardware/gpsimd-engine).
It applies to the [PyTorch/XLA](/neuron-glossary/host-software/torch-neuronx) path on
[Inf2](/neuron-glossary/device-hardware/inf2) and
[Trn1](/neuron-glossary/device-hardware/trn1).
[AWS archived feature overview](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/archive/neuron-features/custom-c%2B%2B-operators.html) · [AWS archive index](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/archive/index.html)

Starting with Neuron 2.33.0, AWS maintains `aws-neuronx-gpsimd-customop-lib`
with critical security and bug fixes only. AWS recommends
[NKI](/neuron-glossary/device-software/nki) for new custom kernels.
NKI can target specialized engines such as the
[Tensor Engine](/neuron-glossary/device-hardware/tensor-engine). The
[native TorchNeuron](/neuron-glossary/host-software/torchneuron) integration
can register an NKI kernel as a PyTorch operator with `torch_neuronx.nki_op`.
[AWS maintenance announcement](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/announcements/neuron2.x/announce-maintenance-gpsimd-customop-lib-2-33.html) · [AWS TorchNeuron NKI guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/torch/guides/how-to-work-with-nki.html)
