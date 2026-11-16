---
title: What is Trainium3?
short: Trainium3
---

**Trainium3** is AWS's fourth-generation ML chip. Each chip has eight
[NeuronCore-v4](/neuron-glossary/device-hardware/neuroncore-v4) cores and
144 GiB of [HBM](/neuron-glossary/device-hardware/hbm). AWS uses the same
chip in the Gen1 and Gen2 configurations of the
[Trn3 UltraServer](/neuron-glossary/device-hardware/trn3-ultraserver).

![A Trainium3 chip with eight NeuronCore-v4 cores, 144 GiB of HBM and NeuronLink-v4.](themed-image://trainium3-device.svg)

## Per-chip specifications

| Metric | [Trainium2](/neuron-glossary/device-hardware/trainium2) | Trainium3 |
|---|---|---|
| Peak 8-bit matmul | 1,299 TFLOPS (FP8) | 2,517 TFLOPS (MXFP8) |
| Peak MXFP4 matmul | — | 2,517 TFLOPS |
| Peak BF16/FP16/TF32 | 667 TFLOPS | 671 TFLOPS |
| Peak FP32 | 181 TFLOPS | 183 TFLOPS |
| HBM capacity | 96 GiB | 144 GiB |
| HBM bandwidth | 2.9 TB/s | 4.9 TB/s in the chip and UltraServer specifications |
| [SBUF](/neuron-glossary/device-hardware/sbuf) | 224 MiB | 256 MiB |
| [NeuronLink](/neuron-glossary/device-hardware/neuronlink) bandwidth | 1,280 GB/s | 2,560 GB/s |
| [DMA](/neuron-glossary/device-hardware/dma-engine) bandwidth | 3.5 TB/s | 4.9 TB/s |

AWS's chip architecture lists 4.9 TB/s of HBM bandwidth and 16
[CC-Cores](/neuron-glossary/device-hardware/collective-communication-engine).
The NKI architecture guide lists 4.7 TB/s and 20 CC-Cores for the same chip.
The aggregate bandwidths in the Trn3 UltraServer table are based on 4.9 TB/s
per chip.
[Trainium3 architecture](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trainium3.html),
[Trainium3 NKI architecture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium3_arch.html),
[Trn3 specifications](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trn3-arch.html#trn3-gen1-gen2-ultraserver-specifications)

![Per-chip Trainium generation comparison of 8-bit and BF16 throughput, HBM capacity, and HBM bandwidth.](themed-image://generations.svg)

For large-model inference, more HBM can hold more weights and KV cache, and
higher bandwidth can read them faster. The peak [MXFP8 and
MXFP4](/neuron-glossary/device-software/mxfp8) rates apply when the model and
kernels use those formats.

[NeuronCore-v4](/neuron-glossary/device-hardware/neuroncore-v4) adds DMA
accumulation into SBUF, direct BF16 matmul output in
[PSUM](/neuron-glossary/device-hardware/psum), and dedicated MXFP8 quantization
and fast exponential instructions on the
[Vector Engine](/neuron-glossary/device-hardware/vector-engine).

For models, see [TorchNeuron](/neuron-glossary/host-software/torchneuron)
for native PyTorch, [TorchTitan Neuron](/neuron-glossary/host-software/torchtitan-neuron)
for distributed training, and
[vLLM Neuron](/neuron-glossary/host-software/vllm-neuron) for serving.
