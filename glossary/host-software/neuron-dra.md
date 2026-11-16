---
title: What is Neuron Dynamic Resource Allocation?
short: Neuron DRA
abbr: DRA
---

The **Neuron Dynamic Resource Allocation (DRA) driver** lets Kubernetes
allocate [Neuron devices](/neuron-glossary/device-hardware/neuron-device)
based on their hardware and how they are connected. The driver publishes
available devices and attributes in `ResourceSlice` objects. A workload
uses a `ResourceClaim` or `ResourceClaimTemplate` to request devices
from the `neuron.aws.com` device class. Where supported, the claim can
select a connected group of chips or set a
[Logical NeuronCore](/neuron-glossary/device-software/logical-neuroncore)
configuration for the allocation.
[AWS Neuron DRA guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/deploy/eks/dra.html)

On EKS, Neuron DRA requires Kubernetes 1.34 or later. It runs on supported
Trainium and Inferentia2 nodes provisioned by Karpenter, EKS managed node
groups or self-managed node groups. Allocation modes vary by instance type.
For Kubernetes 1.34, the Neuron guide specifies node AMIs at 1.34.2 or
later. EKS Auto Mode uses the
[Neuron device plugin](/neuron-glossary/host-software/neuron-device-plugin)
for Neuron accelerators. Each node uses one allocator for its Neuron devices.
[AWS EKS device management guide](https://docs.aws.amazon.com/eks/latest/userguide/device-management-neuron.html) · [AWS Neuron DRA prerequisites](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/deploy/eks/dra.html#prerequisites)

The Neuron UltraServer Operator uses DRA's `ResourceSlice` objects to
manage supported Trn3 UltraServer workloads. On Trainium, DRA can also use
[Neuron Observer](/neuron-glossary/host-software/neuron-observer) fault
events to mark faulty devices with device taints. Taints can keep Kubernetes
from placing work on those devices. This beta feature is opt-in and
requires Kubernetes 1.36 or later, DRA driver 1.3.0 or later, and a Neuron
kernel driver from SDK 2.33.0 or later. A fault taints the affected device on
a standalone instance, or the node-level allocation on an UltraServer.
[AWS UltraServer Operator guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/deploy/eks/ultraserver-operator.html) · [AWS device taints guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/deploy/eks/neuron-device-taints-guide.html)
