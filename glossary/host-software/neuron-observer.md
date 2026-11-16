---
title: What is Neuron Observer?
short: Neuron Observer
---

**Neuron Observer** is a service that monitors the health and performance
of Trn2 and Trn3 nodes on Amazon EKS. It entered public beta in Neuron
2.33.0. It identifies the node and device affected by a hardware fault
and collects utilization, latency, and network metrics. You can query
node health with the `nobs` command or HTTP API, collect metrics with
Prometheus, or export them through OpenTelemetry.
[AWS Neuron Observer overview](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/tools/neuron-observer/index.html) · [AWS Neuron Observer release notes](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/release-notes/components/observer.html)

With device health monitoring enabled,
[Neuron DRA](/neuron-glossary/host-software/neuron-dra) can use Observer
fault events to mark a faulty device on a standalone Trainium instance
or a node-level allocation on an UltraServer. Kubernetes uses that
mark, called a taint, when deciding where to place workloads.
[`neuron-monitor`](/neuron-glossary/host-software/neuron-monitor) remains
supported for JSON metrics, and
[Neuron Explorer](/neuron-glossary/host-software/neuron-explorer) captures
traces for workload profiling.
[AWS device taints guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/deploy/eks/neuron-device-taints-guide.html)
