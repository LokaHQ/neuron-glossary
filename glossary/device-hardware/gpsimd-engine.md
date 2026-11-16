---
title: What is the GpSimd Engine?
short: GpSimd Engine
---

The **GpSimd Engine** (GpSimdE) is a group of **eight programmable 512-bit
vector processors** in each
[NeuronCore](/neuron-glossary/device-hardware/neuroncore) starting with v2.
They can run C/C++ programs and read and write
[SBUF](/neuron-glossary/device-hardware/sbuf) directly.

Where the [Tensor](/neuron-glossary/device-hardware/tensor-engine),
[Vector](/neuron-glossary/device-hardware/vector-engine), and
[Scalar](/neuron-glossary/device-hardware/scalar-engine) engines are
specialized for particular operations, GpSimd can run general-purpose code.
For example, a kernel can use it to apply a triangle-shaped mask to a tensor
without sending the tensor back to the host CPU.

## Custom operators

The legacy Neuron Custom C++ Operators library exposes GpSimd for
[custom operators](/neuron-glossary/device-software/custom-operators) on
[NeuronCore-v2](/neuron-glossary/device-hardware/neuroncore-v2). AWS
directs developers writing new operators to
[NKI](/neuron-glossary/device-software/nki), which can use the specialized
engines directly.

## Generation notes

On [NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3), each
of the eight processors gains its **own integrated DMA engine**. These run in
parallel with GpSimd computation *and* in parallel with the device's main
[DMA engines](/neuron-glossary/device-hardware/dma-engine), and they can
reach SBUF or HBM on chips in the same Trn2 instance. All eight together
provide 307 GB/s, split as 153 GB/s per direction.

Also on v3, the Vector and GpSimd engines can access SBUF **in parallel**,
which was disallowed on v2. The two share a memory bus that the
[Vector Engine's performance mode](/neuron-glossary/device-hardware/vector-engine)
also uses, with the hardware arbitrating between them.

GpSimd can also generate DMA descriptors at runtime. On v3 and later, the
dedicated [Descriptor Generation Engine](/neuron-glossary/device-hardware/dge)
can handle supported transfers and leave GpSimd available for other work.

[NeuronCore-v4](/neuron-glossary/device-hardware/neuroncore-v4) keeps the
same eight-processor structure and programmable C/C++ hardware. The legacy
`aws-neuronx-gpsimd-customop-lib` package is documented for v2 (Trn1 and Inf2)
and entered maintenance in Neuron 2.33.0. The v4 architecture guide
describes the programmable hardware.
[NeuronCore-v4 architecture](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/neuron-core-v4.html#gpsimd-engine),
[Custom C++ library release notes](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/release-notes/archive/customcxxps/gpsimd-customop-lib.html),
[Maintenance announcement](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/announcements/neuron2.x/announce-maintenance-gpsimd-customop-lib.html)

In AWS's abbreviations this appears as **GpSimdE**.
