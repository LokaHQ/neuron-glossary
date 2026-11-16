---
title: What is the NKI Library?
short: NKI Library
---

The **NKI Library** contains AWS's optimized
[NKI](/neuron-glossary/device-software/nki) kernels for Trn2 and Trn3. It
includes attention, matrix multiplication, normalization, quantization and
[collectives](/neuron-glossary/device-software/collectives). Each kernel's
reference lists the layouts, shapes, data types, and configurations it
accepts.
[AWS kernel reference](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/library/index.html)

The [Neuron compiler](/neuron-glossary/host-software/neuronx-cc) bundles a
compatible version that you can import as `nkilib`. The standalone
`nki-library` package takes precedence when installed in the same
environment, so check which library branch or release matches your
compiler. The source also shows how each kernel tiles data, manages its
buffers, and schedules work.
[AWS setup and compatibility guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/library/quickstart-nkl.html) · [NKI Library source](https://github.com/aws-neuron/nki-library)
