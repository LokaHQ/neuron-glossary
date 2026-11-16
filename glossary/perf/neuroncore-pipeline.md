---
title: What is NeuronCore Pipeline?
short: NeuronCore Pipeline
---

**NeuronCore Pipeline** is an
[Inf1](/neuron-glossary/device-hardware/inf1) inference feature. The compiler
splits a model into consecutive groups of layers. Each group runs on a
[NeuronCore](/neuron-glossary/device-hardware/neuroncore) with its weights
held in on-chip memory, and requests pass from one group to the next.

Keeping the weights on chip avoids fetching them from device DRAM for
every request. [NeuronLink-v1](/neuron-glossary/device-hardware/neuronlink)
carries activations when stages span devices. An `inf1.24xlarge` has
16 Inferentia chips and 64 NeuronCores. AWS gives BERT and ResNet-50 as
examples that can benefit without large batches.

The legacy `neuron-cc` compiler enables it with:

```
--neuroncore-pipeline-cores N
```

Benchmark core counts that fit the model and compare throughput and
latency. See the
[AWS NeuronCore Pipeline reference](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-features/neuroncore-pipeline.html).

Modern Trainium serving typically stores weights in
[HBM](/neuron-glossary/device-hardware/hbm) and stages smaller
[tiles](/neuron-glossary/device-software/tile) through
[SBUF](/neuron-glossary/device-hardware/sbuf).
[Tensor parallelism](/neuron-glossary/perf/tensor-parallelism) splits
the work inside a layer.
[Pipeline parallelism](/neuron-glossary/perf/pipeline-parallelism) also
splits by layer and can run with weights in device memory.
