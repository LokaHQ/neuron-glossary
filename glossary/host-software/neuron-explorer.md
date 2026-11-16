---
title: What is Neuron Explorer?
short: Neuron Explorer
---

**Neuron Explorer** is a profiler that records when a Neuron workload
runs each operation. Its timelines let you see whether compute overlaps
with [DMA transfers](/neuron-glossary/device-hardware/dma-engine) and which
dependencies leave an engine idle. For ongoing utilization and memory
metrics, see [`neuron-monitor`](/neuron-glossary/host-software/neuron-monitor).

## What it shows

- **Per-engine timelines** for the
  [Tensor](/neuron-glossary/device-hardware/tensor-engine),
  [Vector](/neuron-glossary/device-hardware/vector-engine),
  [Scalar](/neuron-glossary/device-hardware/scalar-engine), and
  [GpSimd](/neuron-glossary/device-hardware/gpsimd-engine) engines, plus
  DMA queues.
- **A hierarchy view**, from the whole model down to individual instructions.
- **A memory viewer** for [SBUF](/neuron-glossary/device-hardware/sbuf),
  [PSUM](/neuron-glossary/device-hardware/psum), and
  [HBM](/neuron-glossary/device-hardware/hbm) allocation.
- **A tensor viewer** for inspecting actual values.
- **Source linking**, mapping instructions back to your
  [NKI](/neuron-glossary/device-software/nki) or framework code.
- **Device and system profiles** cover on-device execution or a wider trace
  that includes host activity and
  [collectives](/neuron-glossary/device-software/collectives).
- **AI recommendations**, automated suggestions from the profile.

You can also open traces in Perfetto.
[AWS Perfetto guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/tools/neuron-explorer/view-perfetto.html)

## What to look for

**Gaps on the Tensor Engine timeline.** Follow the dependency arrows to
see what the next matrix multiply needs. A late DMA transfer can leave
it waiting for input. It can also wait for another engine to consume the
previous result in [PSUM](/neuron-glossary/device-hardware/psum).
See [latency hiding](/neuron-glossary/perf/latency-hiding).

**Softmax in an attention trace.** Check which engine evaluates the
exponentials before looking for a bottleneck. A kernel can use
`nki.isa.activation` on the
[Scalar Engine](/neuron-glossary/device-hardware/scalar-engine). On
NeuronCore-v4 it can also use `nki.isa.exponential` on
the [Vector Engine](/neuron-glossary/device-hardware/vector-engine).
[AWS Trainium3 NKI architecture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/nki/guides/architecture/trainium3_arch.html#fast-exponential-evaluation)

**Unexpected DMA traffic.** Compare against the expected transfers to spot
extra HBM round trips from [spilling](/neuron-glossary/perf/spilling).

## Capturing and exporting profiles

Use `neuron-explorer capture` with a compiled
[NKI kernel](/neuron-glossary/device-software/nki). To profile a live
[vLLM Neuron](/neuron-glossary/host-software/vllm-neuron) server, use its
profiling endpoints for capture and open the output in Explorer.
[Native TorchNeuron](/neuron-glossary/host-software/torchneuron) also
integrates with `torch.profiler.profile`. Pass
`ProfilerActivity.CPU`, `ProfilerActivity.PrivateUse1`, and a
`NeuronConfig` to correlate the framework trace with runtime and device
activity.
[AWS capture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/tools/neuron-explorer/how-to-profile-workload.html) · [AWS vLLM Neuron profiling guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/vllm-neuron/docs/guides/how-to-profile-workloads.html) · [AWS PyTorch profiling guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/tools/neuron-explorer/how-to-profile-pytorch.html)

For programmatic analysis, `neuron-explorer view --output-format parquet`
exports the full profile as Parquet tables. AWS plans to retire the
full-profile JSON export in the next SDK release, identified as 2.34 in
the 2.33.1 export guide. PyTorch's `trace.json` is a separate input that adds
framework events to an Explorer profile.
[AWS full-profile JSON announcement](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/announcements/neuron2.x/announce-intent-eos-explorer-json.html) · [AWS profile export guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/tools/neuron-explorer/get-started.html) · [AWS profile files reference](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/tools/neuron-explorer/profile-artifacts.html)

Neuron Explorer replaces Neuron Profiler and Neuron Profiler 2.0, and can
open existing NEFF and NTFF captures from those tools.
[AWS migration guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/tools/neuron-explorer/migration-faq.html)
