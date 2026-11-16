---
title: What is the Neuron driver?
short: Neuron driver
---

The **Neuron driver**, packaged as `aws-neuronx-dkms` for Inf2 and Trainium,
is the Linux kernel module that gives the host access to
[Neuron devices](/neuron-glossary/device-hardware/neuron-device). The
[Neuron Runtime](/neuron-glossary/host-software/neuron-runtime) uses it to
communicate with the hardware.

The package uses Dynamic Kernel Module Support (DKMS) to build the module
for the host kernel. After a kernel upgrade, it needs matching headers
and a successful build for the new kernel. These commands check whether
Linux has loaded the module and whether Neuron can see the devices.

```sh
lsmod | grep neuron
neuron-ls
```

[AWS Neuron Runtime and Driver compatibility reference](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/neuron-runtime/compatibility.html)

## OS and kernel compatibility

The compatibility reference lists tested configurations by instance family,
OS, kernel, and glibc version. Neuron Driver 2.31 added support for Linux
7.0, the default kernel in Ubuntu 26.04. Neuron 2.33.0 dropped Amazon Linux
2 support. Driver 2.31 also reorganized the Neuron sysfs tree, so scripts
that read device attributes directly may need new paths.
[AWS Neuron Driver release notes](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/release-notes/components/runtime.html) · [AWS Amazon Linux 2 announcement](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/announcements/neuron2.x/announce-no-support-al2-driver.html) · [AWS sysfs migration guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/tools/neuron-sys-tools/neuron-sysfs-user-guide.html#migrating-from-neuron-driver-2-30-and-earlier)

The driver comes installed on a
[Neuron DLAMI](/neuron-glossary/host-software/neuron-dlami). In a container
deployment, the driver stays on the host and the workload uses exposed
device files. On EKS, the
[Neuron device plugin](/neuron-glossary/host-software/neuron-device-plugin)
or [Neuron DRA](/neuron-glossary/host-software/neuron-dra) handles allocation.
