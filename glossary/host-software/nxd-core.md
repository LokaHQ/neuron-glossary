---
title: What is NxD Core?
short: NxD Core
---

**NxD Core** (NeuronX Distributed Core) supplies the distributed building blocks for
[NxD Inference](/neuron-glossary/host-software/nxd-inference) and
[NxD Training](/neuron-glossary/host-software/nxd-training). Install it as
`neuronx-distributed` and import it as `neuronx_distributed`. For example, a
sharded linear layer splits its weights across chips for
[tensor parallelism](/neuron-glossary/perf/tensor-parallelism). NxD Core also
creates the process groups for those chips and provides tools for saving
and loading sharded checkpoints.
[Archived release notes](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/release-notes/archive/index.html)

## Support and replacement APIs

AWS put the training APIs in maintenance in Neuron 2.30 for critical
security fixes. For new Trn2 and Trn3 training, use PyTorch's distributed APIs via
[TorchNeuron](/neuron-glossary/host-software/torchneuron) or
[TorchTitan Neuron](/neuron-glossary/host-software/torchtitan-neuron) for
large-scale pretraining.
[AWS training maintenance announcement](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/announcements/neuron2.x/announce-maintenance-nxdt-nxd-core-training.html)

The inference APIs have a separate lifecycle. On Inf2 and Trn1 they stay
in maintenance at Neuron 2.31 for critical bug and security fixes. For Trn2
and Trn3, AWS announced an end to support in Neuron 2.34. Native
`torch.compile(backend="neuron")` replaces model-building and tracing APIs
such as `ModelBuilderV2` and `parallel_model_trace` in the
`neuronx_distributed.trace` module.
For LLM serving on Trn2 and Trn3, use
[vLLM Neuron](/neuron-glossary/host-software/vllm-neuron).
[AWS inference support announcement](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/announcements/neuron2.x/announce-eos-nxdi-nxd-core-inference.html)
