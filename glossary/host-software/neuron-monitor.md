---
title: What is neuron-monitor?
short: neuron-monitor
---

**`neuron-monitor`** collects periodic metrics from the
[Neuron Runtime](/neuron-glossary/host-software/neuron-runtime) and the
host. It writes each sample as JSON to standard output, where a script
can read it. Companion scripts can expose the metrics to Prometheus or
publish them to CloudWatch.

```sh
neuron-monitor | neuron-monitor-prometheus.py --port 8008
```

The exporter in this example requires the Prometheus Python client.
[AWS neuron-monitor user guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/tools/neuron-sys-tools/neuron-monitor-user-guide.html)

## What it reports

- Per-[NeuronCore](/neuron-glossary/device-hardware/neuroncore) utilization.
- [Device memory](/neuron-glossary/device-hardware/hbm) usage, with
  categories such as model code, constants, tensors and runtime allocations.
- Application execution counts, latency statistics and errors.
- System CPU and memory usage and hardware counters such as ECC events.

The JSON configuration selects which applications and metrics to include
and how often to sample them. Core utilization tells you how long a core
was busy. To see what each engine or DMA queue was doing, use
[Neuron Explorer](/neuron-glossary/host-software/neuron-explorer).
[AWS monitoring configuration and metric groups](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/tools/neuron-sys-tools/neuron-monitor-user-guide.html)

For interactive use, [`neuron-top`](/neuron-glossary/host-software/neuron-top)
shows live utilization and memory.
[Neuron Observer](/neuron-glossary/host-software/neuron-observer) adds
per-device health events and cluster telemetry for Trn2 and Trn3 on Amazon
EKS. Both tools are supported in Neuron 2.33.1.
[AWS Neuron Observer overview](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/tools/neuron-observer/index.html)
