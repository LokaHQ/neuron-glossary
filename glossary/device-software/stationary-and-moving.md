---
title: What are stationary and moving matrices?
short: Stationary & moving
---

A matrix multiplication on the
[Tensor Engine](/neuron-glossary/device-hardware/tensor-engine) has two
inputs. The **stationary** matrix stays in the
[systolic array](/neuron-glossary/device-hardware/systolic-array) while the
**moving** matrix streams through it.

- `LoadStationary` (LS) loads the stationary matrix into the array.
- The **moving** matrix is streamed by a `MultiplyMoving` (MM) instruction,
  multiplying against the held stationary matrix and writing results to
  [PSUM](/neuron-glossary/device-hardware/psum).

One `nki.isa.nc_matmul` call lowers to those two hardware instructions.

```python
# stationary: [K, M], moving: [K, N], dst: [M, N]
nki.isa.nc_matmul(dst, stationary, moving)  # stationary.T @ moving
```

In this unpacked matmul, both inputs put the contraction dimension `K` on
the [partition axis](/neuron-glossary/device-software/partition-dimension).
That is why the math reads `stationary.T @ moving`.

![NeuronCore-v3 example. The Tensor Engine holds the stationary matrix and streams the moving matrix across it, writing to PSUM.](themed-image://stationary-moving.svg)

## The layout rule

> The **free axis of `stationary`** becomes the **partition axis of the
> output**.
> The **free axis of `moving`** becomes the **free axis of the output**.

The layout follows the geometry of the array. Results emerge along the
axis perpendicular to the input partitions, so AWS's architecture diagrams
draw the PSUM partition dimension at a right angle to SBUF's.
[Trainium2 NKI architecture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium2_arch.html)

## Choosing the output layout

You can swap the roles, and you get a transposed result:

```python
nki.isa.nc_matmul(dst_mn, x, y)  # [M, N]
nki.isa.nc_matmul(dst_nm, y, x)  # [N, M]
```

If both inputs fit the chosen roles, choose the order that gives the next
operation the layout it needs. For example, if it needs `N` on the partition
axis, produce `[N, M]` directly and save a
[transpose](/neuron-glossary/device-software/dma-transpose).

## Tile size limits differ by role

The two roles have different caps, which is another reason the assignment
matters. For a standard `nc_matmul` with hardware tiling mode off:

| Role | Axis | Limit | Source |
|---|---|---|---|
| `stationary` | free | 128 | array columns |
| `stationary` | partition | 128 | array rows |
| `moving` | partition | 128 | array rows |
| `moving`, v2 and v3 | free | 512 | one [PSUM](/neuron-glossary/device-hardware/psum) bank with FP32 output |
| `moving`, v4 | free | 4,096 (FP32 output) or 8,192 (BF16 output) | up to eight PSUM banks |

The moving role can take a wider free dimension than the stationary role.
That can reduce the number of matmul calls needed to cover the output.
[NKI `nc_matmul` reference](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/api/generated/nki.isa.nc_matmul.html),
[Trainium and Inferentia2 NKI architecture guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/guides/architecture/trainium_inferentia2_arch.html)

## Double-rate FP8

On [NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3), the
double-rate [FP8](/neuron-glossary/device-software/cfp8) mode extends the
contraction dimension to 256 by giving each processing element two
multiply-accumulates per cycle. Both operands take an extra axis of size
exactly 2:

```python
# stationary: [128, 2, 128]   moving: [128, 2, 512]   dst: [128, 512]
nisa.nc_matmul(dst, stationary, moving, perf_mode=nisa.matmul_perf_mode.double_row)
```

`LoadStationary` places two values in each processing element.
`MultiplyMoving` streams in two matching values so the element can compute
both products in the same cycle. Zero-pad an odd contraction length before
packing it into the two axes.
