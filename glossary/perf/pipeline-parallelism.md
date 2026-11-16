---
title: What is pipeline parallelism on Neuron?
short: Pipeline parallelism
abbr: PP
---

**Pipeline parallelism** (PP) assigns different groups of layers to
different devices. Each group is a **stage**. Stages send activations
forward and gradients backward during training. A stage can also use
[tensor parallelism](/neuron-glossary/perf/tensor-parallelism) to split
its layer computations across devices.

## The pipeline bubble

A stage waits for the previous stage to produce its input. Splitting
a batch into smaller **microbatches** lets stage 1 begin the next one
while stage 2 works on the current one. The **bubble** is time that
stages spend idle while the pipeline fills, drains, or waits for a
slower stage.

For one fill-and-drain pass with equally fast stages, the idle fraction
is `(stages - 1) / (microbatches + stages - 1)`. More microbatches can
reduce this overhead, though scheduling and activation memory still
matter. In autoregressive inference, each sequence's next token depends
on its last token. Serving multiple independent sequences provides
more work to pipeline.

## Combining strategies

A training job can combine several strategies. The communication pattern
helps decide where to place each group.

| Strategy | Communicates | Typical placement |
|---|---|---|
| [Tensor](/neuron-glossary/perf/tensor-parallelism) | within layers | within a fast NeuronLink domain |
| Context | within attention | within a fast NeuronLink domain |
| **Pipeline** | at stage boundaries | within or across instances |
| [Data](/neuron-glossary/perf/data-parallelism) | gradient synchronization | across instances |

On Trn2 and Trn3, [TorchNeuron](/neuron-glossary/host-software/torchneuron)
supports `torch.distributed.pipelining`. AWS's setup guide requires
[EFA](/neuron-glossary/device-hardware/efa)/RDMA for stage-to-stage
communication, including for a pipeline on a single node.
[TorchNeuron distributed training guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/torch/guides/torch-distributed.html#pipeline-parallelism-split-layers-across-stages)
