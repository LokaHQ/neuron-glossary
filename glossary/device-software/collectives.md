---
title: What are collectives on Neuron?
short: Collectives
---

**Collective operations** move or combine data across a group of workers,
each identified by its rank. Neuron runs them on dedicated
[CC-Cores](/neuron-glossary/device-hardware/collective-communication-engine),
which allows communication to overlap with compute when dependencies and
scheduling permit. [AWS compute-communication overlap guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/neuron-runtime/explore/compute-comm-overlap.html)

| Operation | What it does |
|---|---|
| **All-reduce** | Combine corresponding values, for example by summing, and return the result to every rank |
| **All-gather** | Concatenate all ranks' data and return the result to every rank |
| **Reduce-scatter** | Reduce values across ranks and give each rank a slice |
| **All-to-all** | Redistribute one piece from each source rank to each destination rank |
| **Collective-permute** | Send each rank's data to a specified destination rank |

[Tensor parallelism](/neuron-glossary/perf/tensor-parallelism) often reduces
partial activations across shards.
[Data parallelism](/neuron-glossary/perf/data-parallelism) synchronizes
gradients. Mixture-of-experts routing can use all-to-all.

## Where they run

[NeuronLink](/neuron-glossary/device-hardware/neuronlink) carries traffic
within a connected set of chips. The 16 chips of a
[`trn2.48xlarge`](/neuron-glossary/device-hardware/trn2) form a 4×4 grid
with links that wrap around its edges. A
[Trn2 UltraServer](/neuron-glossary/device-hardware/trn2-ultraserver) adds
NeuronLink rings connecting matching positions across four hosts.
[EFA](/neuron-glossary/device-hardware/efa) carries traffic between
NeuronLink domains. The cost depends on the SKU, rank placement, message size
and collective algorithm. Use
[`nccom-test`](/neuron-glossary/host-software/nccom-test) to measure the
paths and group sizes your workload uses.
[AWS Trn2 architecture](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trn2-arch.html) · [AWS inter-node collectives guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/neuron-runtime/explore/internode-collective-comm.html) · [AWS intra-node collectives guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/neuron-runtime/explore/intranode-collective-comm.html)

## Issuing collectives

Frameworks and libraries such as
[TorchTitan Neuron](/neuron-glossary/host-software/torchtitan-neuron) and
[vLLM Neuron](/neuron-glossary/host-software/vllm-neuron) use collectives
to implement sharding. The
[Neuron Runtime](/neuron-glossary/host-software/neuron-runtime) executes
them on hardware.

Hand-written [NKI](/neuron-glossary/device-software/nki) kernels can use
`nki.collectives` directly. A `ReplicaGroup` identifies which ranks act
together. This fragment sums one tensor per rank and writes the same
sum to every rank. Inside the kernel, `world_size` is the total number
of ranks, supplied as a Python integer at specialization. Allocate
matching tensors `src` and `dst` in private HBM before calling it.

```python
import nki.collectives as ncc
import nki.language as nl

replica_group = ncc.ReplicaGroup.from_partition_op(
    world_size, ncc.rg_partition_op.bitwise_and, 0
)
ncc.all_reduce(srcs=[src], dsts=[dst], replica_group=replica_group, op=nl.add)
```

The source and destination are lists so one call can reduce several
HBM tensors together. The allowed buffers and layouts vary by
operation and [LNC setting](/neuron-glossary/device-software/logical-neuroncore).
[AWS all-reduce API](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/api/generated/nki.collectives.all_reduce.html) · [AWS ReplicaGroup API](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/api/generated/nki.collectives.ReplicaGroup.html)
