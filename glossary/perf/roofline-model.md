---
title: What is the roofline model?
short: Roofline model
---

The **roofline model** estimates the speed an operation could reach given
the available compute throughput and memory bandwidth. Plot
[arithmetic intensity](/neuron-glossary/perf/arithmetic-intensity)
on the x-axis and FLOPs per second on the y-axis.

```
throughput ceiling = min(peak compute throughput,
                         arithmetic intensity × peak memory bandwidth)
```

The slanted part of the chart is the bandwidth limit. The flat part
is the compute limit. The two meet at the **machine balance**.

![A schematic roofline with low-intensity operations near the bandwidth limit and high-intensity operations near the compute limit.](themed-image://roofline.svg)

## Numbers for Trainium2

For a [Trainium2](/neuron-glossary/device-hardware/trainium2) chip against
[HBM](/neuron-glossary/device-hardware/hbm) at 2.9 TB/s:

| Precision | Peak | Machine balance |
|---|---|---|
| BF16 | 667 TFLOPS | ~230 FLOPs/byte |
| FP8 | 1,299 TFLOPS | ~448 FLOPs/byte |
| FP32 | 181 TFLOPS | ~62 FLOPs/byte |

At a given precision, the lower of the two ceilings predicts the bottleneck
if the operation can reach that ceiling. Switching to FP8 raises the compute
ceiling. It can also change the operation's intensity, since it can take
fewer bytes to store the inputs.
[Trainium2 published chip peaks](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/about-neuron/arch/neuron-hardware/trainium2.html)

## Choose the relevant rates

Pick the peak for the engine doing the work. On
[NeuronCore-v3](/neuron-glossary/device-hardware/neuroncore-v3), the
[Tensor Engine](/neuron-glossary/device-hardware/tensor-engine) peaks at
79 BF16 TFLOPS. The
[Vector Engine](/neuron-glossary/device-hardware/vector-engine) peaks at
1.0 FP32 TFLOPS. A reduction running on the Vector Engine has a different
ceiling from a Tensor Engine matmul.

Pick the bandwidth for the data path you measured. A kernel that works in
[SBUF](/neuron-glossary/device-hardware/sbuf) after loading its inputs has
a different bandwidth limit from one that continually fetches from HBM.
See [peak rate](/neuron-glossary/perf/peak-rate).

## Using it

Measure the achieved throughput, estimate the intensity for the chosen
data path, and plot the point.

- **Near the slanted line:** reduce bytes moved with
  [tiling](/neuron-glossary/device-software/tiling),
  [fusion](/neuron-glossary/perf/fusion), or quantization.
- **Near the flat line:** look for ways to do less work or use a faster
  supported format.
- **Below either limit:** profile the operation in
  [Neuron Explorer](/neuron-glossary/host-software/neuron-explorer). Idle
  engine time can come from poor [overlap](/neuron-glossary/perf/latency-hiding),
  synchronization, or unexpected [spills](/neuron-glossary/perf/spilling).
