---
title: What is nccom-test?
short: nccom-test
---

**`nccom-test`** measures how fast Trainium workers exchange data through
[collectives](/neuron-glossary/device-software/collectives) such as
all-reduce, all-gather, reduce-scatter, and all-to-all. The example measures
all-reduce across two workers (ranks) at several message sizes.

```sh
nccom-test -r 2 --minbytes 1024 --maxbytes 1073741824 --stepfactor 4 --datatype fp32 allr
```

## Reading the results

- **`time(us)`** is the measured collective latency in microseconds.
- **`algbw`** divides the message size by the measured time. It is the
  application's effective throughput for that operation and those ranks.
- **`busbw`** scales `algbw` by a factor based on the collective and rank
  count. For an all-reduce across `r` ranks the factor is
  `2 × (r − 1) / r`. It estimates communication bandwidth per rank
  from the amount of data the algorithm exchanges.

The columns labeled `GB/s` use GiB/s, according to the AWS guide. Compare
runs with the same operation, message size, dtype and rank placement.
`--show-algorithm` helps explain a change across configurations.
[AWS NCCOM-TEST user guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/tools/neuron-sys-tools/nccom-test.html)

## Topology and placement

Use [`neuron-ls --topology`](/neuron-glossary/host-software/neuron-ls) to
inspect device connectivity. Trainium can use
[NeuronLink](/neuron-glossary/device-hardware/neuronlink) between chips on
a single instance and across hosts within a supported UltraServer.
Cross-instance collectives outside that NeuronLink domain use
[EFA](/neuron-glossary/device-hardware/efa). Match the rank placement to
your workload when measuring bandwidth. Chip specifications describe the
link hardware, while `nccom-test` reports the throughput of an operation.
[AWS inter-node collectives guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/neuron-runtime/explore/internode-collective-comm.html)

For an application-level check, use
[Neuron Explorer](/neuron-glossary/host-software/neuron-explorer) to see
when the [CC-Cores](/neuron-glossary/device-hardware/collective-communication-engine)
run and whether the app overlaps communication with compute.
