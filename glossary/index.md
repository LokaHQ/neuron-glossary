---
title: Neuron Glossary
tagline: A guide to AWS Trainium and Inferentia chips and the software that runs on them.
---

AWS builds two families of machine learning chips.
[Inferentia](/neuron-glossary/device-hardware/inferentia) and
[Inferentia2](/neuron-glossary/device-hardware/inferentia2) are designed for
inference: running a trained model. [Trainium](/neuron-glossary/device-hardware/trainium),
[Trainium2](/neuron-glossary/device-hardware/trainium2), and
[Trainium3](/neuron-glossary/device-hardware/trainium3) support both training
and inference. AWS calls each chip a [Neuron device](/neuron-glossary/device-hardware/neuron-device).
An EC2 instance such as [Trn2](/neuron-glossary/device-hardware/trn2) provides
the host CPU, host memory, and one or more of those devices.

## From PyTorch to a chip

1. **Choose a software path.** On Trn2 or Trn3,
   [TorchNeuron](/neuron-glossary/host-software/torchneuron) lets supported
   PyTorch code use the `neuron` device. The same entry links to examples for
   Hugging Face inference and fine-tuning. For serving a supported language
   model behind an API, start with
   [vLLM Neuron](/neuron-glossary/host-software/vllm-neuron). See the
   [Neuron SDK](/neuron-glossary/host-software/neuron-sdk) for other workloads
   and older instance families.
2. **Compile and run.** The [compiler](/neuron-glossary/host-software/neuronx-cc)
   turns operations into a [NEFF](/neuron-glossary/device-software/neff),
   the executable that the [runtime](/neuron-glossary/host-software/neuron-runtime)
   loads and runs on the device.
3. **Follow the data.** A modern [NeuronCore](/neuron-glossary/device-hardware/neuroncore)
   brings small blocks of data called [tiles](/neuron-glossary/device-software/tile)
   from device memory into a fast scratchpad, [SBUF](/neuron-glossary/device-hardware/sbuf).
   The [Tensor Engine](/neuron-glossary/device-hardware/tensor-engine) reads
   those tiles for matrix multiplication and accumulates results in
   [PSUM](/neuron-glossary/device-hardware/psum). The compiler handles these
   transfers for framework code. When you write a custom
   [NKI](/neuron-glossary/device-software/nki) kernel, you can control them
   directly.

## If you already know GPUs

These comparisons map familiar roles. NeuronCore-v2 and later execute
instructions on specialized engines that work on blocks of data called tiles.

| CUDA / NVIDIA | Neuron | How it maps |
|---|---|---|
| Streaming Multiprocessor | [NeuronCore](/neuron-glossary/device-hardware/neuroncore) | A core on the accelerator with separate compute engines on v2 and later |
| Tensor Core | [Tensor Engine](/neuron-glossary/device-hardware/tensor-engine) | Runs matrix multiplication using a [systolic array](/neuron-glossary/device-hardware/systolic-array) |
| CUDA Core | [Vector](/neuron-glossary/device-hardware/vector-engine) and [Scalar](/neuron-glossary/device-hardware/scalar-engine) Engines | Handle operations such as reductions and element-wise math |
| Thread, warp, thread block | — | NKI programs express work as operations on [tiles](/neuron-glossary/device-software/tile) |
| Shared memory | [SBUF](/neuron-glossary/device-hardware/sbuf) | A scratchpad that the compiler or kernel manages. The Tensor Engine writes its results to [PSUM](/neuron-glossary/device-hardware/psum) |
| VRAM | [HBM](/neuron-glossary/device-hardware/hbm) | Device memory on Inferentia2 and Trainium. First-generation Inferentia uses DDR4 |
| L2 cache | — | Neuron uses [software-managed memory](/neuron-glossary/device-software/software-managed-memory). The program schedules the transfers between device memory and on-chip scratchpads |
| CUDA C++ | [NKI](/neuron-glossary/device-software/nki) | Write custom kernels in Python |
| PTX / SASS | [NISA](/neuron-glossary/device-software/nisa) | Low-level operations exposed through NKI's `nki.isa` module |
| `cubin` | [NEFF](/neuron-glossary/device-software/neff) | Device executable, often specialized to input shapes |
| `nvcc` | [`neuronx-cc`](/neuron-glossary/host-software/neuronx-cc) | Compiles graphs and schedules device data movement |
| CUDA runtime | [Neuron Runtime](/neuron-glossary/host-software/neuron-runtime) | Loads and runs device executables |
| `nvidia.ko` | [Neuron driver](/neuron-glossary/host-software/neuron-driver) | Connects the host runtime to devices |
| `nvidia-smi` | [`neuron-ls`](/neuron-glossary/host-software/neuron-ls), [`neuron-top`](/neuron-glossary/host-software/neuron-top) | List devices and inspect live utilization |
| Nsight Systems | [Neuron Explorer](/neuron-glossary/host-software/neuron-explorer) | Profiles host and device activity, including individual engines |
| NCCL | [Neuron Collectives](/neuron-glossary/device-software/collectives) | Coordinates group communication using [dedicated cores](/neuron-glossary/device-hardware/collective-communication-engine) on supported chips |
| NVLink | [NeuronLink](/neuron-glossary/device-hardware/neuronlink) | Connects chips within an instance or an [UltraServer](/neuron-glossary/device-hardware/trn3-ultraserver) |
| Occupancy | [Latency hiding](/neuron-glossary/perf/latency-hiding) | Use independent work and [pipeline depth](/neuron-glossary/perf/littles-law) to keep engines busy |
| Shared-memory bank conflict | [PSUM bank conflict](/neuron-glossary/perf/bank-conflict) | Engines can contend for access to the same PSUM bank |
| PyTorch eager and `torch.compile` | [TorchNeuron](/neuron-glossary/host-software/torchneuron) | On-demand operator execution or compiled graphs on Trn2 and Trn3 |

For the CUDA side of the comparison, see
[Modal's GPU Glossary](https://modal.com/gpu-glossary).
