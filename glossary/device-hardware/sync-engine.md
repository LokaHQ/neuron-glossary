---
title: What is the Sync Engine?
short: Sync Engine
---

The **Sync Engine** (SyncE, sometimes SP) is a control unit in
[NeuronCore-v2 and later](/neuron-glossary/device-hardware/neuroncore). It
can start [DMA](/neuron-glossary/device-hardware/dma-engine) transfers and
synchronize operations independently of the compute engines.

A compute engine's **sequencer** directs its own stream of instructions.
It can issue two kinds of instruction.

- **Control instructions** run on the sequencer itself. They can branch,
  compute an address in private 32-bit registers, or start a DMA transfer.
- **Data path instructions** perform tensor operations using
  [SBUF](/neuron-glossary/device-hardware/sbuf) and
  [PSUM](/neuron-glossary/device-hardware/psum).

The Sync Engine is a separate sequencer that runs control instructions.
It can start loading the next tile while the
[Tensor Engine](/neuron-glossary/device-hardware/tensor-engine) works on
the current one. See
[latency hiding](/neuron-glossary/perf/latency-hiding).

## Synchronization

The compute engines run asynchronously and in parallel, so data dependencies
between them need enforcement. That is done with **atomic hardware semaphores**.

The [Neuron compiler](/neuron-glossary/host-software/neuronx-cc) analyzes the
data dependencies in your graph or
[NKI](/neuron-glossary/device-software/nki) kernel and inserts the
semaphore operations so a consumer waits until its input is ready.

On [NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3), the
Sync Engine is one of the two sequencers that can drive the
[Descriptor Generation Engine](/neuron-glossary/device-hardware/dge); the
[Scalar Engine](/neuron-glossary/device-hardware/scalar-engine) is the
other. The compiler can choose a sequencer, and `nisa.dma_copy` also allows
the caller to select it.

The Sync Engine appears in AWS's glossary as "the SP engine".
