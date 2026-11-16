---
title: What is HBM on a Neuron device?
short: Device memory
abbr: HBM
---

**HBM** stands for **High Bandwidth Memory**. On Trainium and Inferentia2, it
is the main memory attached to the
[Neuron device](/neuron-glossary/device-hardware/neuron-device), similar to
a GPU's VRAM. It holds model weights, intermediate activations, optimizer
state, and the KV cache.

| Chip | Capacity | Bandwidth |
|---|---|---|
| [Inferentia](/neuron-glossary/device-hardware/inferentia) | 8 GiB (DRAM, not HBM) | 50 GiB/s |
| [Trainium](/neuron-glossary/device-hardware/trainium) / [Inferentia2](/neuron-glossary/device-hardware/inferentia2) | 32 GiB | 820 GiB/s |
| [Trainium2](/neuron-glossary/device-hardware/trainium2) | 96 GiB | 2.9 TB/s |
| [Trainium3](/neuron-glossary/device-hardware/trainium3) | 144 GiB | 4.9 TB/s in the chip architecture, 4.7 TB/s in the NKI guide |

AWS uses "device memory" for both HBM and the DDR memory on first-generation
[Inferentia](/neuron-glossary/device-hardware/inferentia). The chip architecture
documents list 820 GiB/s for Trainium and Inferentia2, where the NKI
architecture guide writes 820 GB/s.
[Trainium architecture](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trainium.html),
[Trainium/Inferentia2 NKI architecture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium_inferentia2_arch.html)

## Where it sits

On a v2 or later system, data moves through these memories.

| Level | Memory | Scope |
|---|---|---|
| Fastest | [PSUM](/neuron-glossary/device-hardware/psum) | per NeuronCore, on-chip |
| | [SBUF](/neuron-glossary/device-hardware/sbuf) | per NeuronCore, on-chip |
| | **HBM** | per device, off-core |
| Slowest | Host DRAM | per instance, over PCIe |

HBM and host memory store tensors in a linear address space. SBUF and PSUM
split data across 128 partitions. A plain DMA copy can distribute tensor
rows from HBM across SBUF partitions. A
[DMA transpose](/neuron-glossary/device-software/dma-transpose) can map a
different tensor axis to the partition dimension.

At the model boundary, a typical [NKI](/neuron-glossary/device-software/nki)
kernel takes device-memory tensors, loads tiles into SBUF, computes on them
and stores the result back to HBM. The host framework moves tensors between
host and device memory.

## How bandwidth affects token generation

In a batch-one decode step for a dense language model, each large weight
matrix is typically read from HBM and used once. That is little work per
byte moved, so decoding is often
[memory-bound](/neuron-glossary/perf/memory-bound).

A weight-only ceiling for token throughput is:

```
tokens/sec ≈ HBM bandwidth / bytes of model weights
```

A 70B model has about 140 GB of BF16 weights and needs more than one
96 GiB [Trainium2](/neuron-glossary/device-hardware/trainium2) chip. If two
chips stream a balanced share of the weights at their combined peak of
5.8 TB/s, the idealized bandwidth ceiling is about 41 tokens/s at batch one.
That estimate excludes KV-cache traffic and inter-chip communication.
[FP8](/neuron-glossary/device-software/cfp8) approximately halves the
bytes needed for the weights.

Note that the bandwidth figures above are **per chip**, shared across all of
its [NeuronCores](/neuron-glossary/device-hardware/neuroncore) — 2.9 TB/s
serves eight cores on Trainium2.

## Pooling

[NeuronLink](/neuron-glossary/device-hardware/neuronlink) makes the HBM of
multiple chips **directly addressable** from any chip in the pool: up to 16
chips on [Trn1](/neuron-glossary/device-hardware/trn1), 64 on a
[Trn2 UltraServer](/neuron-glossary/device-hardware/trn2-ultraserver) and
64 or 144 on a [Trn3 UltraServer](/neuron-glossary/device-hardware/trn3-ultraserver).
The memory is still physically distributed, so remote and local accesses use
different paths.

Data movement between HBM and SBUF is done by
[DMA engines](/neuron-glossary/device-hardware/dma-engine), which run in
parallel with computation and support inline compression and decompression.
