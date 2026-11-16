---
title: What is the Neuron device plugin?
short: Neuron device plugin (K8s)
---

The **Neuron device plugin** tells Kubernetes how many
[Neuron devices](/neuron-glossary/device-hardware/neuron-device) and
[NeuronCores](/neuron-glossary/device-hardware/neuroncore) a node can
allocate. A container can request whole devices with
`aws.amazon.com/neuron` or cores with `aws.amazon.com/neuroncore`. This
fragment requests four devices.

```yaml
resources:
  limits:
    aws.amazon.com/neuron: 4
```

If a pod needs a group of chips connected by
[NeuronLink](/neuron-glossary/device-hardware/neuronlink), the Neuron
scheduler extension can select that group.
[Neuron DRA](/neuron-glossary/host-software/neuron-dra) lets pods request
devices by attributes and topology through Kubernetes resource claims.
EKS Auto Mode includes the device plugin for Neuron hardware.
[AWS EKS device management guide](https://docs.aws.amazon.com/eks/latest/userguide/device-management-neuron.html)

The [Neuron driver](/neuron-glossary/host-software/neuron-driver) runs on
the host. The pod uses the exposed devices through the
[Neuron Runtime](/neuron-glossary/host-software/neuron-runtime) and its
framework packages, typically from a
[Neuron DLC](/neuron-glossary/host-software/neuron-dlami).

The Neuron Node Problem Detector reports health problems at the node
level. Automatic node recovery is opt-in. For isolation of a single
faulty device on a standalone Trainium instance, see DRA device taints
and [Neuron Observer](/neuron-glossary/host-software/neuron-observer).
[AWS Node Problem Detector guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/deploy/infrastructure/problem-detector.html) · [AWS device taints guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/deploy/eks/neuron-device-taints-guide.html)
