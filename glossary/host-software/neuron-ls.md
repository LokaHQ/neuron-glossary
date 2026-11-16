---
title: What is neuron-ls?
short: neuron-ls
---

**`neuron-ls`** lists the
[Neuron devices](/neuron-glossary/device-hardware/neuron-device) on an
instance or exposed to a container. It shows which cores belong to each
device, how the devices connect, and which processes are using them.

Excerpt from AWS's example of a 16-chip Trn2 system with LNC set to 2.

```
$ neuron-ls
logical-neuroncore-config: 2
+--------+--------+----------+--------+---------------+--------------+---------------+------+
| NEURON | NEURON | NEURON   | NEURON | CONNECTED     | PCI          | CPU           | NUMA |
| DEVICE | CORES  | CORE IDS | MEMORY | DEVICES       | BDF          | AFFINITY      | NODE |
+--------+--------+----------+--------+---------------+--------------+---------------+------+
| 0      | 4      | 0-3      | 96 GB  | 12, 3, 4, 1   | 0000:cc:00.0 | 48-95,144-191 | 1    |
| 1      | 4      | 4-7      | 96 GB  | 13, 0, 5, 2   | 0000:b5:00.0 | 48-95,144-191 | 1    |
...
| 15     | 4      | 60-63    | 96 GB  | 11, 14, 3, 12 | 0000:f7:00.0 | 48-95,144-191 | 1    |
```

## Reading the inventory

**`logical-neuroncore-config: 2`.** This is
[LNC](/neuron-glossary/device-software/logical-neuroncore), and it is why
the NEURON CORES column reports four logical cores per device. Each
[Trainium2](/neuron-glossary/device-hardware/trainium2) chip physically
has eight [NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3)
cores. The whole instance exposes 64 logical cores. A
[tensor-parallel group](/neuron-glossary/perf/tensor-parallelism) can use
a subset if the model and topology support it.

**CONNECTED DEVICES.** The
[NeuronLink](/neuron-glossary/device-hardware/neuronlink) neighbors of
each device. Four neighbors per device match the 4×4 2D torus on
16-chip [Trn2](/neuron-glossary/device-hardware/trn2) instances. `--topology`
displays the system topology.

**NUMA NODE and CPU AFFINITY.** These columns show which host CPU and memory
domain is closest to a device. Placement matters when the host moves data
to the accelerator frequently. The table's `96 GB` memory label corresponds
to the 96 GiB per chip listed in the
[Trainium2 specifications](/neuron-glossary/device-hardware/trainium2).

## Options

| Flag | Effect |
|---|---|
| `-w`, `--wide` | Wider table |
| `-a`, `--show-all-procs` | Include processes not using Neuron Runtime 2.x, such as `neuron-monitor` |
| `-t`, `--topology` | Show device topology |
| `-j`, `--json-output` | Emit the Neuron 2.33.1 JSON format |

It works on all Neuron instance types — [Inf1](/neuron-glossary/device-hardware/inf1),
[Inf2](/neuron-glossary/device-hardware/inf2),
[Trn1](/neuron-glossary/device-hardware/trn1), [Trn2](/neuron-glossary/device-hardware/trn2), and
[Trainium3 instances](/neuron-glossary/device-hardware/trainium3).
[AWS neuron-ls user guide](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/tools/neuron-sys-tools/neuron-ls.html)

AWS announced that Neuron 2.34 will replace `--json-output` and `-j` with
`--output-format json`. The updated schema adds top-level instance and
UltraServer fields, so scripts that consume the 2.33 output need to update
both the flag and their parser.
[AWS neuron-ls JSON announcement](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/announcements/neuron2.x/announce-intent-eos-neuron-ls-json.html)

## Diagnosing device access

If the list is empty on a Neuron instance, check host
[driver](/neuron-glossary/host-software/neuron-driver) installation and
whether the driver built for the current kernel. From a container, also
check the device mappings. Use the process columns or `--show-all-procs`
when a process may still be holding devices.
