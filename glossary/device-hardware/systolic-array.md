---
title: What is a systolic array?
short: Systolic array
---

A **systolic array** is a grid of simple processing elements, each doing a
multiply-accumulate, which multiplies two numbers and adds the product to a
running sum. The elements pass data to their neighbors, reusing it as it
moves through the grid. The
[Tensor Engine](/neuron-glossary/device-hardware/tensor-engine) uses a
**128 × 128** array in the NeuronCore generations covered by NKI.

## How the array reuses data

In a systolic array, each input element is read from
[SBUF](/neuron-glossary/device-hardware/sbuf) **once**, then reused across
an entire row or column of processing elements. With a full row or column,
one read can feed up to 128 multiply-accumulates.

## Why 128 is everywhere

The shape of the array determines how standard matmul instructions lay out
their inputs.

- [SBUF](/neuron-glossary/device-hardware/sbuf) and
  [PSUM](/neuron-glossary/device-hardware/psum) have **128 partitions**,
  one per row of processing elements.
- An on-chip [tile](/neuron-glossary/device-software/tile) can use up to
  **128 partitions**.
- The contraction dimension of a matmul must map to the partition dimension,
  because that is the axis the array accumulates along.
- The `stationary` matrix's free axis is capped at **128**, the number of
  columns.

See [tiling](/neuron-glossary/device-software/tiling) for how NKI breaks larger
matrices into blocks that fit these limits.

## The tradeoffs

Tile shape and data layout affect how much of the array is useful.

- **Small matrices use less of the array.** A narrow tile can leave rows
  or columns idle. The cost also depends on which input is stationary and
  whether hardware tiling mode is enabled.
- **Sparsity does not help** unless it is
  [structured](/neuron-glossary/device-software/structured-sparsity) in a
  pattern the hardware recognizes — hence the 4:16 through 1:2 patterns on
  [v3](/neuron-glossary/device-hardware/neuroncore-v3) and later.
- **There is a pipeline fill and drain cost.** Data has to propagate across the
  grid before the first result emerges. For a long stream of matmuls, the
  rate depends on how often the engine can accept a new instruction.

The 128×128 shape is also why [FP8](/neuron-glossary/device-software/cfp8)
doubling works the way it does on
[NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3): the grid
stays 128×128 physically, but each processing element performs two FP8
multiply-accumulates per cycle, which the programmer sees as a 256×128 array.
