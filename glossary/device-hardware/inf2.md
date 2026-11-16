---
title: What is an Inf2 instance?
short: Inf2
---

**Inf2** is the EC2 instance family powered by
[Inferentia2](/neuron-glossary/device-hardware/inferentia2) chips. It is
AWS's inference-optimized family for the
[NeuronCore-v2](/neuron-glossary/device-hardware/neuroncore-v2) generation.

| Size | Chips | vCPUs | Host memory | FP8/FP16/BF16/TF32 TFLOPS | FP32 TFLOPS | Device memory | Device bandwidth | [NeuronLink-v2](/neuron-glossary/device-hardware/neuronlink) |
|---|---|---|---|---|---|---|---|---|
| `inf2.xlarge` | 1 | 4 | 16 GiB | 190 | 47.5 | 32 GiB | 820 GiB/s | — |
| `inf2.8xlarge` | 1 | 32 | 128 GiB | 190 | 47.5 | 32 GiB | 820 GiB/s | — |
| `inf2.24xlarge` | 6 | 96 | 384 GiB | 1,140 | 285 | 192 GiB | 4,920 GiB/s | 192 GiB/s |
| `inf2.48xlarge` | 12 | 192 | 768 GiB | 2,280 | 570 | 384 GiB | 9,840 GiB/s | 192 GiB/s |

Each chip carries two
[NeuronCore-v2](/neuron-glossary/device-hardware/neuroncore-v2) cores, so
`inf2.48xlarge` exposes 24 NeuronCores and 384 GiB of device memory.

Both single-chip sizes have the same accelerator. `inf2.8xlarge` provides
more host CPU and RAM, which can help when
[compiling models](/neuron-glossary/host-software/neuronx-cc) on the instance.
[AWS Neuron Inf2 architecture](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/inf2-arch.html)

![Chip counts across both Inferentia instance families.](themed-image://inf-instances.svg)

## Inf2 versus Trn1

Both families use NeuronCore-v2, with different instance configurations.

| | Inf2 | [Trn1](/neuron-glossary/device-hardware/trn1) |
|---|---|---|
| Max chips | 12 | 16 |
| NeuronLink-v2 links per chip | 2 | 4 |
| [EFA](/neuron-glossary/device-hardware/efa) | Unsupported | 32xlarge sizes only |

Inf2 uses NeuronLink for multi-chip inference within one instance.

## Serving models

Inf2 serves models that fit within one instance. On a 48xlarge,
[tensor parallelism](/neuron-glossary/perf/tensor-parallelism) can use up to
384 GiB of total device memory across 12 chips. The model must support
splitting its tensors across the participating cores, and weights, KV cache
and other working data must fit on each chip.

The PyTorch/XLA serving path for Inf2 is in maintenance mode as of Neuron
2.31, based on PyTorch 2.9. The current
[vLLM Neuron plugin](/neuron-glossary/host-software/vllm-neuron) targets
[Trn2](/neuron-glossary/device-hardware/trn2) and
[Trn3](/neuron-glossary/device-hardware/trn3-ultraserver).
[AWS inference maintenance announcement](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/announcements/neuron2.x/announce-maintenance-pytorch-xla-inference.html),
[vLLM Neuron documentation](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/vllm-neuron/index.html)
