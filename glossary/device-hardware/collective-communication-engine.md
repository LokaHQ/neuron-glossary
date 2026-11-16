---
title: What is the Collective Communication Engine?
short: Collective Communication Engine
abbr: CCE
---

The **Collective Communication Engine** (CCE) uses dedicated **CC-Cores**
to handle [collectives](/neuron-glossary/device-software/collectives).
These are operations in which a group of NeuronCores exchange or combine data,
such as all-reduce, all-gather, reduce-scatter and all-to-all.

Dedicated hardware lets communication **overlap** with computation. For
example, each replica in data-parallel training computes gradients for its
batch. CC-Cores can combine the gradients for layers that have finished
while the
[Tensor](/neuron-glossary/device-hardware/tensor-engine),
[Vector](/neuron-glossary/device-hardware/vector-engine), and
[Scalar](/neuron-glossary/device-hardware/scalar-engine) engines work on
other layers.

If computation needs the result of a collective, it still has to wait for
communication to finish.

CC-Cores drive traffic over
[NeuronLink](/neuron-glossary/device-hardware/neuronlink) within a scale-up
domain. A domain can span multiple servers in an UltraServer. Across scale-up
domains, collectives use [EFA](/neuron-glossary/device-hardware/efa).

Counts per chip:

| Chip | CC-Cores |
|---|---|
| [Trainium](/neuron-glossary/device-hardware/trainium) / [Inferentia2](/neuron-glossary/device-hardware/inferentia2) | 6 |
| [Trainium2](/neuron-glossary/device-hardware/trainium2) | 16 in the chip architecture, 20 in the NKI guide |
| [Trainium3](/neuron-glossary/device-hardware/trainium3) | 16 in the chip architecture, 20 in the NKI guide |

You do not program CC-Cores directly in normal use. Collectives are invoked
through frameworks and libraries such as
[TorchNeuron](/neuron-glossary/host-software/torchneuron) and
[NxD Inference](/neuron-glossary/host-software/nxd-inference), and executed by the
[Neuron runtime](/neuron-glossary/host-software/neuron-runtime).
[NKI](/neuron-glossary/device-software/nki) kernels on Trn2 and Trn3 can
request collective operations through `nki.collectives`.
[NKI collectives reference](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/api/nki.collectives.html)

To measure what the hardware actually achieves, use
[`nccom-test`](/neuron-glossary/host-software/nccom-test), the Neuron
equivalent of NCCL's benchmark tools.
