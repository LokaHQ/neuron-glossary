---
title: What is operator fusion?
short: Fusion
---

**Fusion** combines several operators into one so that intermediate results
stay in on-chip memory instead of round-tripping to
[HBM](/neuron-glossary/device-hardware/hbm).

Fusion can speed up [memory-bound](/neuron-glossary/perf/memory-bound)
work by eliminating reads and writes at the boundary between operators.

Consider `y = gelu(x @ w + b)`, unfused:

```
1. matmul:  read x and w from HBM  → write matmul result to HBM
2. bias:    read matmul result, b  → write biased result to HBM
3. gelu:    read biased result    → write y to HBM
```

The matmul and bias results each make a round trip through HBM. A fused
version can keep both results on the chip:

```
1. read x, w, b from HBM into SBUF
2. matmul on the Tensor Engine     → PSUM
3. bias + gelu on Scalar/Vector    → SBUF
4. write y to HBM
```

The fused version does the same math with fewer HBM transfers, so its
HBM [arithmetic intensity](/neuron-glossary/perf/arithmetic-intensity)
is higher. Neuron's scratchpads are
[software-managed](/neuron-glossary/device-software/software-managed-memory).
The kernel or compiler must plan to reuse an intermediate on chip.

Fusion also maps naturally onto the hardware, because a
[NeuronCore](/neuron-glossary/device-hardware/neuroncore)'s engines are
specialized and independent. A fused matmul-plus-activation puts the matmul on
the [Tensor Engine](/neuron-glossary/device-hardware/tensor-engine) and the
activation on the [Scalar Engine](/neuron-glossary/device-hardware/scalar-engine),
where the Scalar Engine can process one
[tile](/neuron-glossary/device-software/tile) while the Tensor Engine
works on the next. That overlap is an example of
[engine parallelism](/neuron-glossary/perf/engine-parallelism).

## Who does it

[`neuronx-cc`](/neuron-glossary/host-software/neuronx-cc) can fuse common
patterns when the operators appear in the same compiled graph. You can also
fuse them explicitly in an [NKI](/neuron-glossary/device-software/nki) kernel.
FlashAttention, for example, computes attention in tiles and keeps intermediate
scores on chip, avoiding a full attention matrix in HBM.
[NKI performance guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/deep-dives/nki_perf_guide.html#opt-2-fuse-operations-to-minimize-intermediate-data-spilling)

## The limit

Fusion changes which buffers have to be live at the same time. If they
exceed [SBUF](/neuron-glossary/device-hardware/sbuf) capacity, the compiled
kernel may [spill](/neuron-glossary/perf/spilling) data back to HBM. Smaller
[tiles](/neuron-glossary/device-software/tiling) can help fit a fused
operation, though they can also reduce reuse. Compare HBM traffic and execution
time in [Neuron Explorer](/neuron-glossary/host-software/neuron-explorer).
