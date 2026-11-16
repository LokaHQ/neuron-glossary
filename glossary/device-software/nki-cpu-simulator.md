---
title: What is the NKI CPU simulator?
short: NKI CPU simulator
---

The **NKI CPU simulator** runs a [`@nki.jit` kernel](/neuron-glossary/device-software/nki)
in Python and NumPy on a CPU. To debug a kernel, call
`nki.simulate(kernel)(a, b)` with NumPy arrays and compare the result
with a reference implementation. You can set Python breakpoints. The
experimental simulator also checks many operand constraints and fills
uninitialized buffers with recognizable values. PyTorch workflows can
opt in with `NKI_SIMULATOR=1`.
[AWS NKI CPU simulator guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/nki_simulator.html)

The simulator approximates hardware arithmetic and allocates tensors
independently, so it cannot tell you whether they all fit on-chip. It
can simulate a subset of
[collectives](/neuron-glossary/device-software/collectives), with one CPU
process per rank. Run the compiled kernel on Trainium to check how it
fits on-chip memory and use
[Neuron Explorer](/neuron-glossary/host-software/neuron-explorer) to see
instruction timing and engine overlap.
[AWS simulator limitations](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/nki_simulator.html#simulation-limitations)
