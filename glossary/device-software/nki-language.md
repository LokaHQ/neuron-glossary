---
title: What is nki.language?
short: nki.language
---

**`nki.language`**, conventionally imported as `nl`, is the high-level API
for [NKI](/neuron-glossary/device-software/nki). Use it to create tensors in
specific memories and express operations and loops. The compiler turns its
NumPy-style operations into [`nki.isa`](/neuron-glossary/device-software/nisa)
instructions.
AWS marks convenience operations such as `nl.load`, `nl.store` and
`nl.softmax` as experimental. [AWS nki.language API](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/api/nki.language.html)

This kernel computes softmax across the columns of each row. Run it with
[`LNC=1`](/neuron-glossary/device-software/logical-neuroncore). Each batch
of rows keeps the full width in [SBUF](/neuron-glossary/device-hardware/sbuf).
Leave room for the softmax intermediates.

```python
import nki
import nki.language as nl

@nki.jit
def softmax_kernel(in_tensor):
    out = nl.ndarray(in_tensor.shape, dtype=in_tensor.dtype, buffer=nl.shared_hbm)
    rows = in_tensor.shape[0]
    tile_rows = nl.tile_size.pmax
    for start in range(0, rows, tile_rows):
        stop = min(start + tile_rows, rows)
        tile = nl.load(in_tensor[start:stop, :])
        nl.store(out[start:stop, :], value=nl.softmax(tile, axis=1))
    return out
```

## Buffers are explicit

[Neuron memory is software-managed](/neuron-glossary/device-software/software-managed-memory).
A tensor's buffer determines which instructions can access it.

| Buffer | Memory |
|---|---|
| `nl.shared_hbm` | [HBM](/neuron-glossary/device-hardware/hbm), shared by the physical programs of an LNC=2 kernel |
| `nl.sbuf` | [SBUF](/neuron-glossary/device-hardware/sbuf), core-local working memory |
| `nl.psum` | [PSUM](/neuron-glossary/device-hardware/psum), core-local matmul accumulation |
| `nl.private_hbm` | HBM private to the physical core |

`nl.load` and `nl.store` use [DMA](/neuron-glossary/device-hardware/dma-engine)
to transfer tiles between HBM and SBUF. `nl.tile_size.pmax` gives the
[128-partition limit](/neuron-glossary/device-software/tiling). The
partition is the first on-chip tile dimension, which determines the row count
in this example. [AWS tile-size API](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/api/nki.language.tile_size.html)

## Specialization and device loops

The NKI 0.7 frontend unrolls Python `for` and `while` loops whose bounds
or conditions it can evaluate at compile time. It traces the body once for
each iteration. For a counted loop that runs on
the device, use `nl.fori_loop(lower, upper, body)`. For a device-side
condition, use `nl.while_loop(init, body)` and return the next condition
value from the body.

The old iterators `nl.affine_range`, `nl.sequential_range` and
`nl.static_range` are deprecated aliases for `range`. Migrate
`nl.dynamic_range` loops and Python `while` loops that test a device
register to the compiled loop APIs.
[AWS NKI loop guide](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/nki/deep-dives/nki-loops.html)
