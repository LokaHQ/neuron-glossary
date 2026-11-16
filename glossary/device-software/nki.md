---
title: What is NKI?
short: Neuron Kernel Interface
abbr: NKI
---

**NKI**, the Neuron Kernel Interface, is a Python API and compiler for
writing kernels that run on the engines inside a
[NeuronCore](/neuron-glossary/device-hardware/neuroncore). A kernel can
implement a single operation or combine several operations so they can
reuse data in on-chip memory.

This NKI 0.7 kernel adds two tensors with the same shape and data type.
It loads each input as a single tile, so the first axis can have at
most 128 entries and the inputs and result must fit in SBUF. Run it with
[`LNC=1`](/neuron-glossary/device-software/logical-neuroncore).

```python
import nki
import nki.language as nl

@nki.jit
def add_kernel(a_tensor, b_tensor):
    out = nl.ndarray(a_tensor.shape, dtype=a_tensor.dtype, buffer=nl.shared_hbm)
    a = nl.load(a_tensor)
    b = nl.load(b_tensor)
    nl.store(out, value=nl.add(a, b))
    return out
```

The inputs and output live in [HBM](/neuron-glossary/device-hardware/hbm).
`nl.load` brings each input into [SBUF](/neuron-glossary/device-hardware/sbuf)
before the add. The result goes back to HBM through `nl.store`. These
transfers are explicit because
[Neuron memory is software-managed](/neuron-glossary/device-software/software-managed-memory).

## How a kernel runs

- [`nki.language`](/neuron-glossary/device-software/nki-language) provides
  buffers, data types, loops and high-level operations. A convenience
  operation can lower to one or more hardware instructions.
- [`nki.isa`](/neuron-glossary/device-software/nisa) exposes low-level
  operations and their operands. Use it when
  tuning engine use, memory layout or instruction scheduling.

`@nki.jit` marks the kernel entry point. In NKI 0.7, Python runs at compile
time to decide which operations to emit. A branch on input shape, for
example, emits only the operations for the shape seen at compilation.
The compiler turns those operations into device instructions on
[tiles](/neuron-glossary/device-software/tile) and tells engines when to
wait for one another's results. Use the `nki.*` modules for current kernels.
The previous `neuronxcc.nki.*` namespace has a different API.
[AWS NKI language guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/get-started/nki-language-guide.html) · [AWS NKI migration guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/migration/index.html)

## Using kernels in models

[Native TorchNeuron](/neuron-glossary/host-software/torchneuron) can call a
`@nki.jit` kernel directly on Neuron tensors in eager mode or inside
`torch.compile(backend="neuron")`. For a named PyTorch custom operator,
decorate a typed wrapper with `torch_neuronx.nki_op` and declare any
mutated arguments in `mutates_args`. To train through the operator, register
its backward function with `.register_autograd`. JAX integration is also
available. [AWS guide to NKI in TorchNeuron](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/torch/guides/how-to-work-with-nki.html) · [AWS framework integration guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/framework_custom_op.html)

The [NKI Library](/neuron-glossary/device-software/nki-library) offers tuned
kernels for common operations. The
[NKI CPU simulator](/neuron-glossary/device-software/nki-cpu-simulator) runs
kernels locally for debugging and correctness checks.
