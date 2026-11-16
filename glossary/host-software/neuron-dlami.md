---
title: What are Neuron DLAMIs and DLCs?
short: Neuron DLAMI & containers
abbr: DLC
---

**Neuron DLAMIs** (Deep Learning Amazon Machine Images) set up the EC2 host.
Base images include the
[Neuron driver](/neuron-glossary/host-software/neuron-driver),
[EFA](/neuron-glossary/device-hardware/efa) software, and Neuron tools.
Framework images add one or more Python environments with preinstalled
training or inference packages.
[AWS Neuron DLAMI guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/deploy/environments/dlami.html)

**Neuron DLCs** (Deep Learning Containers) package the application
environment, including the [runtime](/neuron-glossary/host-software/neuron-runtime)
and framework packages. They use the driver installed on the host.
On Kubernetes,
the [Neuron device plugin](/neuron-glossary/host-software/neuron-device-plugin)
or [Neuron DRA](/neuron-glossary/host-software/neuron-dra) allocates devices
and exposes them to pods.
[AWS EKS device management guide](https://docs.aws.amazon.com/eks/latest/userguide/device-management-neuron.html)

## Image and host compatibility

AWS publishes Neuron SDK 2.33 DLCs on Ubuntu 26.04. The host image has its
own version matrix. For example, AWS publishes the multi-framework DLAMI
for Ubuntu 24.04 and 26.04 and a base DLAMI for Amazon Linux 2023.
For a manual host installation, the runtime and driver compatibility
tables list tested operating systems, kernels, and glibc versions by
instance family.
[AWS container release notes](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/release-notes/components/containers.html) · [AWS DLAMI release notes](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/release-notes/components/dlamis.html)
[AWS runtime and driver compatibility](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/neuron-runtime/compatibility.html)
