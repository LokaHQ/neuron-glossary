#!/usr/bin/env python3
"""Generate the glossary's themed SVG diagrams.

Each diagram is defined once and emitted twice, as `<name>-light.svg` and
`<name>-dark.svg`, using the Loka palette. `build.py` inlines both and CSS shows
whichever matches the active theme.

Usage:
    python3 utils/diagrams.py
"""

import html
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "diagrams")

THEMES = {
    "light": {
        "bg": "none",
        "surface": "#f4f5f7",
        "surface2": "#eaf2fe",
        "text": "#16181f",
        "muted": "#61636d",
        "line": "#cfd0d7",
        "blue": "#1877f2",
        "teal": "#0c6f71",
        "yellow": "#f7d043",
        "on_accent": "#ffffff",
        "yellow_text": "#16181f",
    },
    "dark": {
        "bg": "none",
        "surface": "#161922",
        "surface2": "#16223a",
        "text": "#e9ebf1",
        "muted": "#969cab",
        "line": "#393f4f",
        "blue": "#4d97ff",
        "teal": "#3aa8aa",
        "yellow": "#f7d043",
        "on_accent": "#0e1016",
        "yellow_text": "#0e1016",
    },
}

FONT = "Archivo, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"


class _Palette(dict):
    """Palette lookup that refuses unknown roles.

    A typo'd role name used to fall through to the literal string and emit an
    invalid SVG colour, which renders as black with no error.
    """

    def get(self, key, default=None):
        if key in self:
            return self[key]
        if isinstance(key, str) and (key.startswith("#") or key == "none"):
            return key
        raise KeyError(f"unknown palette role: {key!r}")


class Canvas:
    """Collects SVG primitives, resolving palette roles against one theme."""

    def __init__(self, width, height, theme):
        self.w = width
        self.h = height
        self.c = _Palette(THEMES[theme])
        self.parts = []

    def box(self, x, y, w, h, fill="surface", stroke="line", rx=8, width=1.5, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.parts.append(
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" '
            f'fill="{self.c.get(fill, fill)}" stroke="{self.c.get(stroke, stroke)}" '
            f'stroke-width="{width}"{d}/>'
        )

    def text(self, x, y, s, size=13, fill="text", anchor="middle", weight="500", mono=False, italic=False):
        fam = MONO if mono else FONT
        it = ' font-style="italic"' if italic else ""
        self.parts.append(
            f'<text x="{x}" y="{y}" font-family="{fam}" font-size="{size}" '
            f'font-weight="{weight}" fill="{self.c.get(fill, fill)}" '
            f'text-anchor="{anchor}"{it}>{html.escape(s)}</text>'
        )

    def label(self, x, y, s, size=10, fill="muted", anchor="start"):
        self.parts.append(
            f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" '
            f'font-weight="700" letter-spacing="0.08em" fill="{self.c.get(fill, fill)}" '
            f'text-anchor="{anchor}">{html.escape(s.upper())}</text>'
        )

    def line(self, x1, y1, x2, y2, stroke="line", width=1.5, dash=None, arrow=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        a = f' marker-end="url(#arrow-{arrow})"' if arrow else ""
        self.parts.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" '
            f'stroke="{self.c.get(stroke, stroke)}" stroke-width="{width}"{d}{a}/>'
        )

    def path(self, d, stroke="line", width=1.5, fill="none", arrow=None, dash=None):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        a = f' marker-end="url(#arrow-{arrow})"' if arrow else ""
        self.parts.append(
            f'<path d="{d}" fill="{self.c.get(fill, fill)}" '
            f'stroke="{self.c.get(stroke, stroke)}" stroke-width="{width}"{da}{a}/>'
        )

    def render(self):
        markers = "".join(
            f'<marker id="arrow-{name}" viewBox="0 0 10 10" refX="9" refY="5" '
            f'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
            f'<path d="M 0 1 L 9 5 L 0 9 z" fill="{self.c[name]}"/></marker>'
            for name in ("blue", "teal", "muted", "line", "yellow")
        )
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" '
            f'role="img" width="100%">'
            f"<defs>{markers}</defs>" + "".join(self.parts) + "</svg>"
        )


# --- diagram definitions ----------------------------------------------------


def neuroncore(c):
    """A simplified memory and compute map of NeuronCore-v2 through v4."""
    c.box(20, 20, 660, 312, fill="bg", stroke="line", rx=12, dash="5 4")
    c.label(40, 44, "NeuronCore-v2 through v4")

    engines = [
        ("GpSimd Engine", "general-purpose SIMD", "muted"),
        ("Vector Engine", "reductions, norms", "teal"),
        ("Scalar Engine", "activations, exp", "teal"),
        ("Tensor Engine", "128x128 systolic array", "blue"),
    ]
    for i, (name, sub, colour) in enumerate(engines):
        x = 40 + i * 160
        c.box(x, 58, 145, 62, fill="surface", stroke=colour, width=2)
        c.text(x + 72, 82, name, size=12.5, weight="700")
        c.text(x + 72, 100, sub, size=10, fill="muted", weight="400")

    for i in range(3):
        x = 112 + i * 160
        c.line(x, 120, x, 174, stroke="muted")

    c.path("M 480 173 V 146 H 560 V 121", stroke="blue", width=2, arrow="blue")
    c.line(611, 121, 611, 172, stroke="blue", width=2, arrow="blue")

    c.box(40, 174, 465, 48, fill="surface2", stroke="blue", width=2)
    c.text(272, 195, "SBUF — State Buffer", size=12.5, weight="700")
    c.text(272, 212, "128 partitions - 24-32 MiB - software managed", size=10, fill="muted", weight="400")

    c.box(520, 174, 140, 48, fill="surface", stroke="teal", width=2)
    c.text(590, 195, "PSUM", size=12.5, weight="700")
    c.text(590, 212, "2 MiB for accumulation", size=9.5, fill="muted", weight="400")

    c.text(350, 243, "Vector or Scalar can copy completed results from PSUM to SBUF.",
           size=11, fill="muted")

    c.box(40, 278, 620, 36, fill="surface", stroke="line")
    c.text(350, 301, "HBM (96 GiB on Trainium2)", size=12, weight="600")
    c.line(106, 223, 106, 276, stroke="teal", width=2, arrow="teal")
    c.line(116, 277, 116, 224, stroke="teal", width=2, arrow="teal")
    c.text(130, 256, "DMA", size=10, fill="teal", anchor="start", weight="600")


def memory_hierarchy(c):
    """The four-level memory hierarchy, widening as it gets slower."""
    rows = [
        ("PSUM", "2 MiB per core", "matmul accumulation", "teal", 210),
        ("SBUF", "28 MiB per core", "on-chip scratchpad", "blue", 300),
        ("HBM", "96 GiB per chip", "device memory at up to 2.9 TB/s", "muted", 450),
        ("Host DRAM", "size varies by instance", "memory attached to the host CPU", "muted", 600),
    ]
    y = 30
    for name, size, note, colour, width in rows:
        x = 30 + (600 - width) / 2
        c.box(x, y, width, 52, fill="surface", stroke=colour, width=2)
        c.text(x + width / 2, y + 22, f"{name} — {size}", size=13, weight="700")
        c.text(x + width / 2, y + 39, note, size=10, fill="muted", weight="400")
        y += 68

    c.path("M 655 300 L 655 46", stroke="blue", width=2, arrow="blue")
    c.text(648, 56, "faster", size=10.5, fill="blue", anchor="end", weight="700")
    c.text(648, 296, "bigger", size=10.5, fill="muted", anchor="end", weight="700")
    c.text(345, 322, "Trainium2 example. SBUF and PSUM are software-managed.",
           size=11.5, fill="text", weight="600")


def compile_flow(c):
    """Framework lowering paths that share a compiler and runtime."""
    c.label(20, 27, "PyTorch and JAX compilation", fill="muted")
    paths = [
        ("TorchNeuron eager", "ATen dispatch → StableHLO", "Compile operators on cache misses", "blue"),
        ("TorchNeuron torch.compile", "Dynamo / FX → AOT Autograd", "Lower captured graphs to StableHLO", "blue"),
        ("XLA frontends", "JAX or legacy PyTorch NeuronX", "Lower graphs to HLO", "muted"),
    ]
    for i, (name, stage, detail, colour) in enumerate(paths):
        y = 46 + 90 * i
        c.box(20, y, 252, 76, stroke=colour, width=2)
        c.text(34, y + 22, name, size=16, anchor="start", weight="700")
        c.text(34, y + 43, stage, size=14, anchor="start", fill="muted")
        c.text(34, y + 62, detail, size=13, anchor="start", fill="muted")
        c.line(272, y + 38, 298, y + 38, stroke=colour, width=2)
    c.line(298, 84, 298, 264, stroke="muted", width=2)
    c.line(298, 84, 326, 84, stroke="blue", width=2, arrow="blue")

    shared = [
        ("neuronx-cc", "Optimize and compile", "blue"),
        ("NEFF", "Device executable", "teal"),
        ("Neuron Runtime", "Load and execute", "teal"),
    ]
    for i, (name, detail, colour) in enumerate(shared):
        y = 54 + 90 * i
        c.box(328, y, 172, 60, fill="surface2", stroke=colour, width=2)
        c.text(414, y + 25, name, size=16, weight="700")
        c.text(414, y + 45, detail, size=14, fill="muted")
        if i < len(shared) - 1:
            c.line(414, y + 60, 414, y + 88, stroke="teal", width=2, arrow="teal")


def workload_paths(c):
    """Map new Trn2 and Trn3 workloads to the documented frameworks."""
    c.label(20, 28, "Workload paths on Trn2 and Trn3", fill="muted")
    c.text(500, 28, "Neuron 2.33.1", size=12, anchor="end", fill="muted")
    groups = [
        ("Training", "blue", [
            ("PyTorch training", "TorchNeuron"),
            ("Distributed pretraining", "TorchTitan Neuron"),
        ]),
        ("Inference", "teal", [
            ("LLM serving", "vLLM Neuron"),
            ("Diffusion and multimodal", "vLLM Omni Neuron"),
            ("Custom PyTorch inference", "TorchNeuron"),
        ]),
    ]
    y = 48
    for heading, colour, rows in groups:
        height = 42 + 42 * len(rows)
        c.box(20, y, 480, height, stroke=colour, width=2)
        c.text(38, y + 28, heading, size=17, anchor="start", weight="700", fill=colour)
        for i, (workload, path) in enumerate(rows):
            row = y + 42 + 42 * i
            c.line(38, row, 482, row)
            c.text(38, row + 26, workload, size=14, anchor="start")
            c.line(253, row + 21, 286, row + 21, stroke=colour, arrow=colour)
            c.text(302, row + 26, path, size=15, anchor="start", weight="700")
        y += height + 16


def interconnect(c):
    """Show bandwidth and aggregation scope for Trn2."""
    c.label(30, 27, "Trn2 bandwidth by scope", fill="muted")
    tiers = [
        ("HBM", "2.9 TB/s per chip", "teal"),
        ("NeuronLink-v3 within an instance", "1,024 GiB/s per chip", "blue"),
        ("NeuronLink-v3 between UltraServer members", "256 GiB/s per chip", "blue"),
        ("EFAv3 for scale-out", "3.2 Tbps per 48xlarge instance", "muted"),
    ]
    for i, (scope, bandwidth, colour) in enumerate(tiers):
        y = 44 + 62 * i
        c.box(30, y, 460, 52, stroke=colour, width=2)
        c.text(46, y + 22, scope, size=15, anchor="start", weight="700")
        c.text(46, y + 41, bandwidth, size=14, anchor="start", fill="muted")


def stationary_moving(c):
    """How the Tensor Engine consumes its two operands."""
    c.label(30, 30, "Tensor Engine dataflow · NeuronCore-v3 example", fill="muted")

    c.box(40, 60, 120, 120, fill="surface", stroke="blue", width=2)
    c.text(100, 112, "stationary", size=12, weight="700")
    c.text(100, 130, "128 x 128 max", size=9.5, fill="muted", weight="400")
    c.text(100, 148, "held in the array", size=9.5, fill="muted", weight="400")

    c.box(230, 60, 210, 120, fill="surface2", stroke="line", width=2)
    c.text(335, 108, "128 x 128", size=12.5, weight="700")
    c.text(335, 126, "processing elements", size=10, fill="muted", weight="400")
    c.text(335, 146, "accumulates along partitions", size=9.5, fill="muted", weight="400")

    c.box(40, 210, 400, 46, fill="surface", stroke="teal", width=2)
    c.text(240, 230, "moving  —  free axis up to 512", size=12, weight="700")
    c.text(240, 247, "streamed across the array", size=9.5, fill="muted", weight="400")

    c.line(160, 120, 228, 120, stroke="blue", width=2, arrow="blue")
    c.text(194, 112, "LS", size=9.5, fill="blue", weight="700")
    c.path("M 335 208 L 335 182", stroke="teal", width=2, arrow="teal")
    c.text(352, 198, "MM", size=9.5, fill="teal", anchor="start", weight="700")

    c.box(500, 60, 170, 120, fill="surface", stroke="teal", width=2)
    c.text(585, 100, "PSUM", size=12.5, weight="700")
    c.text(585, 120, "output [M, N]", size=10, fill="muted", weight="400")
    c.text(585, 140, "FP32 destination", size=9.5, fill="muted", weight="400")
    c.line(440, 120, 498, 120, stroke="teal", width=2, arrow="teal")

    c.text(350, 292, "nc_matmul(dst, stationary, moving)  →  stationary.T @ moving",
           size=12, mono=True, weight="600", fill="blue")
    c.text(350, 314, "The free axis of stationary becomes the PARTITION axis of the output.",
           size=10.5, fill="muted", weight="500")


def roofline(c):
    """The roofline, with the operations you actually run placed on it."""
    ox, oy, w, h = 70, 250, 560, 200
    c.line(ox, oy, ox + w, oy, stroke="line", width=2)
    c.line(ox, oy, ox, oy - h, stroke="line", width=2)
    c.text(ox + w / 2, oy + 42, "arithmetic intensity (FLOPs / byte)", size=11, fill="muted")
    self_y = oy - h / 2
    c.parts.append(
        f'<text x="26" y="{self_y}" font-family="{FONT}" font-size="11" '
        f'fill="{c.c["muted"]}" text-anchor="middle" '
        f'transform="rotate(-90 26 {self_y})">attainable FLOPS</text>'
    )

    knee_x, knee_y = ox + 250, oy - 150
    c.path(f"M {ox} {oy} L {knee_x} {knee_y}", stroke="blue", width=2.5)
    c.path(f"M {knee_x} {knee_y} L {ox + w} {knee_y}", stroke="blue", width=2.5)
    c.text(ox + 100, oy - 92, "memory bound", size=11, fill="blue", weight="700")
    c.text(ox + 430, knee_y - 12, "compute bound", size=11, fill="blue", weight="700")
    c.line(knee_x, knee_y, knee_x, oy, stroke="line", width=1.2, dash="4 4")
    c.text(knee_x, oy + 20, "machine balance", size=10, fill="muted", weight="600")

    # Leader lines let the clustered memory-bound points share a label column.
    memory_points = [
        (ox + 20, oy - 12, ox + 150, oy - 8, "elementwise", "teal"),
        (ox + 35, oy - 21, ox + 150, oy - 32, "LLM decode", "yellow"),
        (ox + 60, oy - 36, ox + 150, oy - 56, "layer norm", "teal"),
    ]
    for px, py, lx, ly, name, colour in memory_points:
        c.line(px, py, lx - 6, ly - 4, stroke="line", width=1)
        c.parts.append(f'<circle cx="{px}" cy="{py}" r="5" fill="{c.c[colour]}"/>')
        c.text(lx, ly, name, size=10, anchor="start", fill="muted", weight="600")

    for px, py, name in ((ox + 380, knee_y + 26, "LLM prefill"),
                         (ox + 470, knee_y + 12, "large matmul")):
        c.parts.append(f'<circle cx="{px}" cy="{py}" r="5" fill="{c.c["teal"]}"/>')
        c.text(px + 11, py + 4, name, size=10, anchor="start", fill="muted", weight="600")

    c.label(30, 30, "Roofline example", fill="muted")
    c.text(218, 54, "Bandwidth sets the ceiling at low intensity.",
           size=12, weight="600")
    c.text(218, 73, "The points show illustrative workloads.", size=11, fill="muted", weight="500")


def trn2_topology(c):
    """The 4x4 torus inside one Trn2, and the rings that join four of them."""
    c.label(30, 28, "trn2.48xlarge - 4x4 2D torus", fill="muted")
    ox, oy, step = 60, 55, 62
    for r in range(4):
        for col in range(4):
            x, y = ox + col * step, oy + r * step
            c.box(x, y, 44, 40, fill="surface", stroke="blue", width=1.6, rx=6)
            c.text(x + 22, y + 25, str(r * 4 + col), size=11, weight="700")
    for r in range(4):
        for col in range(4):
            x, y = ox + col * step, oy + r * step
            if col < 3:
                c.line(x + 44, y + 20, x + step, y + 20, stroke="line", width=1.4)
            if r < 3:
                c.line(x + 22, y + 40, x + 22, y + step, stroke="line", width=1.4)
    # Wrap-around links are what make it a torus rather than a mesh.
    for r in range(4):
        y = oy + r * step + 20
        c.path(f"M {ox} {y} C {ox - 32} {y}, {ox - 32} {y}, {ox - 20} {y}",
               stroke="teal", width=1.4, dash="3 3")
        c.path(f"M {ox + 3 * step + 44} {y} C {ox + 3 * step + 76} {y}, "
               f"{ox + 3 * step + 76} {y}, {ox + 3 * step + 64} {y}",
               stroke="teal", width=1.4, dash="3 3")
    for col in range(4):
        x = ox + col * step + 22
        c.line(x, oy - 15, x, oy, stroke="teal", width=1.4, dash="3 3")
        c.line(x, oy + 3 * step + 40, x, oy + 3 * step + 57,
               stroke="teal", width=1.4, dash="3 3")
    c.text(158, 320, "1,024 GiB/s per chip", size=11, fill="blue", weight="700")
    c.text(158, 338, "wrap-around links dashed", size=9.5, fill="muted", weight="400")

    c.label(400, 28, "UltraServer - 4 instances", fill="muted")
    for i in range(4):
        y = 55 + i * 62
        c.box(400, y, 230, 44, fill="surface", stroke="muted", width=1.6)
        c.text(515, y + 20, f"trn2u.48xlarge #{i}", size=11, weight="700")
        c.text(515, y + 35, "16 chips", size=9.5, fill="muted", weight="400")
    c.path("M 646 77 C 690 77, 690 285, 646 285", stroke="teal", width=2, dash="5 4")
    c.text(660, 186, "ring", size=10, fill="teal", anchor="start", weight="700")
    c.text(515, 320, "256 GiB/s per chip between instances", size=11, fill="muted", weight="700")
    c.text(515, 338, "same coordinate in each instance forms a ring", size=9.5, fill="muted", weight="400")



def trn3_topology(c):
    """Compare the two Trn3 scale-up domains at rack level."""
    c.label(20, 27, "Trn3 UltraServer scale-up domains", fill="muted")
    generations = [
        ("Gen1", 64, "2 hosts × 16 chips", "1 × radix-32 rack switch", "Direct links pair chips within each host"),
        ("Gen2", 144, "18 hosts × 4 chips", "2 × radix-36 rack switches", "A radix-4 switch connects the chips within each host"),
    ]
    for i, (name, chips, hosts, switches, intra_host) in enumerate(generations):
        y = 44 + 182 * i
        c.box(20, y, 480, 166, fill="bg", stroke="blue", width=2)
        c.text(36, y + 27, f"{name} · {chips} Trainium3 chips", size=18, anchor="start", weight="700")
        for rack, x in enumerate((36, 294), 1):
            c.box(x, y + 43, 190, 75, fill="surface2", stroke="line")
            c.text(x + 12, y + 65, f"Rack {rack}", size=15, anchor="start", weight="700")
            c.text(x + 12, y + 85, hosts, size=13, anchor="start")
            c.text(x + 12, y + 104, switches, size=13, anchor="start", fill="muted")
        c.line(229, y + 81, 291, y + 81, stroke="teal", width=2, dash="4 3")
        c.text(260, y + 136, "Direct NeuronLink-v4 links pair chips across racks",
               size=13, fill="teal", weight="700")
        c.text(260, y + 154, intra_host, size=12.5, fill="muted")


def data_type_bits(c):
    """Bit layouts of every format Neuron supports, drawn to scale."""
    c.label(24, 26, "One bar = one format, drawn to scale over 32 bits", fill="muted")

    rows = [
        ("FP32", 1, 8, 23, "full precision"),
        ("TF32", 1, 8, 10, "FP32 range, less precision"),
        ("BF16", 1, 8, 7, "FP32 range in 16 bits"),
        ("FP16", 1, 5, 10, "more precision, less range"),
        ("FP8_e5m2", 1, 5, 2, "gradients"),
        ("FP8_e4m3", 1, 4, 3, "weights, activations"),
        ("FP8_e3m4", 1, 3, 4, "no double-rate matmul"),
    ]
    unit = 15.0
    x0 = 118
    y = 48
    for name, sgn, exp, man, note in rows:
        c.text(108, y + 15, name, size=11.5, anchor="end", weight="700", mono=True)
        x = x0
        for bits, colour, ink in (
            (sgn, "muted", "on_accent"),
            (exp, "blue", "on_accent"),
            (man, "teal", "on_accent"),
        ):
            w = bits * unit
            c.box(x, y, w, 22, fill=colour, stroke=colour, rx=2)
            if bits >= 2:
                c.text(x + w / 2, y + 15, str(bits), size=10, fill=ink, weight="700")
            x += w
        c.text(x + 10, y + 15, note, size=10, fill="muted", anchor="start", weight="400")
        y += 30

    # legend
    ly = y + 8
    for label, colour, dx in (("sign", "muted", 0), ("exponent = range", "blue", 74),
                              ("mantissa = precision", "teal", 234)):
        c.box(x0 + dx, ly, 13, 13, fill=colour, stroke=colour, rx=2)
        c.text(x0 + dx + 19, ly + 11, label, size=10.5, fill="muted",
               anchor="start", weight="600")

    c.text(350, y + 48, "Eight bits can be split three ways. That is what the c in cFP8 means.",
           size=11, weight="600")


def engine_pipeline(c):
    """A Gantt view of the overlap that keeps a NeuronCore busy."""
    c.label(24, 26, "One tile of work, four units, overlapping", fill="muted")

    lanes = [
        ("DMA in", "teal", [(0, 1), (1, 1), (2, 1), (3, 1)]),
        ("Tensor Engine", "blue", [(1, 1), (2, 1), (3, 1), (4, 1)]),
        ("Vector / Scalar", "teal", [(2, 1), (3, 1), (4, 1), (5, 1)]),
        ("DMA out", "muted", [(3, 1), (4, 1), (5, 1), (6, 1)]),
    ]
    x0, colw, y = 150, 68, 52
    for i in range(8):
        c.text(x0 + i * colw + colw / 2, 44, f"t{i}", size=9.5, fill="muted", weight="700")

    for li, (name, colour, blocks) in enumerate(lanes):
        c.text(140, y + 17, name, size=11, anchor="end", weight="700")
        c.line(x0, y + 26, x0 + 8 * colw, y + 26, stroke="line", width=1)
        for bi, (start, span) in enumerate(blocks):
            c.box(x0 + start * colw + 2, y, span * colw - 4, 22, fill="surface",
                  stroke=colour, width=1.6, rx=2)
            c.text(x0 + start * colw + span * colw / 2, y + 15, f"n+{bi}" if bi else "n",
                   size=10, weight="600")
        y += 40

    # the steady-state column
    c.box(x0 + 3 * colw, 48, colw, 4 * 40 - 12, fill="bg", stroke="yellow",
          width=2, rx=3, dash="4 3")
    c.text(x0 + 3 * colw + colw / 2, 48 + 4 * 40, "all four busy", size=10,
           fill="yellow_text", weight="700")

    c.text(350, 236, "At t3 the DMA engines, Tensor Engine, and Vector/Scalar engines",
           size=11, weight="600")
    c.text(350, 254, "are all working on different tiles. That overlap is the whole game.",
           size=11, fill="muted", weight="500")


def tiling(c):
    """Contrast the NeuronCore-v3 tile with the wider v4 destination."""
    c.label(24, 26, "Matmul tiling · NeuronCore-v3 example", fill="muted")

    # stationary
    c.box(60, 56, 120, 120, fill="surface", stroke="line", width=1.5)
    c.text(120, 48, "A [M, K]", size=10.5, fill="muted", weight="700")
    for i in range(3):
        for j in range(3):
            fill = "surface2" if (i, j) == (0, 0) else "surface"
            c.box(60 + j * 40, 56 + i * 40, 40, 40, fill=fill,
                  stroke="blue" if (i, j) == (0, 0) else "line",
                  width=2 if (i, j) == (0, 0) else 1, rx=0)
    c.text(80, 80, "128", size=9, fill="blue", weight="700")
    c.text(80, 92, "x128", size=9, fill="blue", weight="700")

    # moving
    c.box(230, 56, 200, 120, fill="surface", stroke="line", width=1.5)
    c.text(330, 48, "B [K, N]", size=10.5, fill="muted", weight="700")
    for i in range(3):
        for j in range(2):
            first = (i, j) == (0, 0)
            c.box(230 + j * 100, 56 + i * 40, 100, 40,
                  fill="surface2" if first else "surface",
                  stroke="teal" if first else "line",
                  width=2 if first else 1, rx=0)
    c.text(280, 80, "128", size=9, fill="teal", weight="700")
    c.text(280, 92, "x512", size=9, fill="teal", weight="700")

    c.text(455, 120, "=", size=18, fill="muted", weight="700")

    c.box(480, 56, 180, 120, fill="surface", stroke="line", width=1.5)
    c.text(570, 48, "PSUM [M, N]", size=10.5, fill="muted", weight="700")
    c.box(480, 56, 90, 40, fill="surface2", stroke="yellow", width=2, rx=0)
    c.text(525, 80, "one bank", size=9, fill="yellow_text", weight="700")

    rows = [
        ("partition axis", "128", "SBUF partitions and systolic-array rows"),
        ("stationary free axis", "128", "systolic-array columns"),
        ("moving free axis", "512", "one PSUM bank, 512 FP32 per partition"),
    ]
    y = 208
    for name, limit, why in rows:
        c.text(200, y, name, size=11, anchor="end", weight="700")
        c.box(212, y - 14, 44, 20, fill="blue", stroke="blue", rx=2)
        c.text(234, y, limit, size=11, fill="on_accent", weight="700")
        c.text(268, y, why, size=10.5, fill="muted", anchor="start", weight="400")
        y += 28

    c.box(60, 288, 600, 52, fill="surface2", stroke="teal", width=1.5)
    c.text(360, 309, "NeuronCore-v4 moving free axis", size=13, weight="700")
    c.text(360, 327, "Up to 4,096 FP32 or 8,192 BF16 output elements across eight PSUM banks",
           size=12, fill="muted")


def prefill_decode(c):
    """Compare weight reuse and likely bottlenecks in LLM inference."""
    c.label(20, 27, "Prefill and decode", fill="muted")
    panels = [
        ("Prefill", "blue", 20, [
            "Process prompt tokens",
            "Reuse weights across tokens",
            "Often compute-bound",
        ]),
        ("Decode", "teal", 268, [
            "One token per sequence",
            "Reuse weights across a batch",
            "Often memory-bound",
        ]),
    ]
    for name, colour, x, lines in panels:
        c.box(x, 45, 232, 126, stroke=colour, width=2)
        c.text(x + 14, 72, name, size=17, fill=colour, anchor="start", weight="700")
        for i, line in enumerate(lines):
            c.text(x + 14, 97 + 24 * i, line, size=13.5, anchor="start")

    c.box(20, 189, 480, 110, fill="surface2", stroke="line")
    c.text(36, 216, "Batch-1 decode · 8B BF16 on one Trainium2", size=15,
           anchor="start", weight="700")
    c.text(36, 240, "16 GB of weights at 2.9 TB/s → about 180 tokens/s", size=14, anchor="start")
    c.text(36, 263, "Weight-only ceiling at full HBM bandwidth", size=13,
           anchor="start", fill="muted")
    c.text(36, 283, "Excludes KV traffic, compute and communication", size=13,
           anchor="start", fill="muted")


def parallelism(c):
    """Typical placements for distributed training on Trn2."""
    c.label(28, 27, "Parallelism placement · Trn2 training example", fill="muted")

    rows = [
        ("Tensor parallelism", "Layer collectives", "Prefer a fast NeuronLink domain", "blue"),
        ("Context parallelism", "Attention communication", "Prefer a fast NeuronLink domain", "blue"),
        ("Pipeline parallelism", "Stage-boundary transfers", "Can span instances over EFA", "teal"),
        ("Data parallelism", "Gradient synchronization", "Can span instances over EFA", "teal"),
    ]
    for i, (name, traffic, placement, colour) in enumerate(rows):
        y = 46 + 62 * i
        c.box(28, y, 464, 52, stroke=colour)
        c.text(42, y + 23, name, size=14, anchor="start", weight="700")
        c.text(42, y + 42, traffic, size=12, anchor="start", fill="muted")
        c.text(260, y + 32, placement, size=14, anchor="start", fill=colour)


def generations(c):
    """Trainium 1 to 3, on the axes that actually moved."""
    c.label(24, 26, "Trainium generations, per chip", fill="muted")

    metrics = [
        ("8-bit TFLOPS¹", [190, 1299, 2517]),
        ("BF16 TFLOPS", [190, 667, 671]),
        ("HBM GiB", [32, 96, 144]),
        ("HBM TB/s", [0.8, 2.9, 4.9]),
    ]
    names = ["Trainium", "Trainium2", "Trainium3"]
    colours = ["muted", "blue", "teal"]

    panel_w, x0, top, bar_h = 156, 22, 60, 18
    for mi, (title, values) in enumerate(metrics):
        px = x0 + mi * (panel_w + 14)
        c.text(px + panel_w / 2, top - 12, title, size=10.5, weight="700")
        peak = max(values)
        for vi, v in enumerate(values):
            by = top + vi * 34
            w = max(3, (v / peak) * 62)
            c.text(px + 45, by + 13, names[vi], size=9, anchor="end",
                   fill="muted", weight="700")
            c.box(px + 51, by, w, bar_h, fill=colours[vi], stroke=colours[vi], rx=2)
            txt = f"{v:g}" if v < 10 else f"{v:,.0f}"
            c.text(px + 57 + w, by + 13, txt, size=9.5, anchor="start", weight="700")

    c.text(350, 196, "Peak BF16 changed from 667 to 671 TFLOPS.",
           size=11, weight="700")
    c.text(350, 215, "¹ cFP8 on Trainium, FP8 on Trainium2, and MXFP8 on Trainium3.",
           size=11, fill="muted")
    c.text(350, 234, "HBM bandwidth follows AWS's chip comparison tables.",
           size=10.5, fill="muted")


def logical_neuroncore(c):
    """Why a trn2.48xlarge reports 64 cores and not 128."""
    c.label(24, 26, "Logical NeuronCore configuration on Trainium2", fill="muted")

    c.text(160, 56, "LNC = 1", size=12, weight="700")
    c.text(160, 74, "8 physical cores", size=10, fill="muted", weight="400")
    for i in range(8):
        x, y = 46 + (i % 4) * 58, 90 + (i // 4) * 46
        c.box(x, y, 52, 38, fill="surface", stroke="line", width=1.5)
        c.text(x + 26, y + 17, f"v3 #{i}", size=9.5, weight="600")
        c.text(x + 26, y + 30, "28 MiB", size=8, fill="muted", weight="400")

    c.line(292, 130, 336, 130, stroke="blue", width=2, arrow="blue")
    c.text(314, 120, "pair", size=9.5, fill="blue", weight="700")

    c.text(500, 56, "LNC = 2  (Trn2 runtime default)", size=12, weight="700")
    c.text(500, 74, "4 logical cores", size=10, fill="muted", weight="400")
    for i in range(4):
        x, y = 366 + (i % 2) * 140, 90 + (i // 2) * 46
        c.box(x, y, 134, 38, fill="surface2", stroke="blue", width=2)
        c.text(x + 67, y + 17, f"logical #{i}", size=9.5, weight="700")
        c.text(x + 67, y + 30, "2 × 28 MiB local SBUF", size=9, fill="muted", weight="400")

    c.box(46, 194, 608, 34, fill="surface", stroke="yellow", width=2)
    c.text(350, 216, "trn2.48xlarge: 16 chips x 4 logical = 64 NeuronCores, not 128",
           size=11.5, weight="700")
    c.text(350, 252, "At LNC=2, an NKI kernel uses a separate local tile on each physical core.",
           size=10.5, fill="muted", weight="500")


def sparsity(c):
    """What an M:N pattern actually looks like."""
    c.label(24, 26, "Structured sparsity patterns", fill="muted")

    pats = [("2:4", 2, 4, 50), ("4:8", 4, 8, 240), ("4:16", 4, 16, 430)]
    cell = 19
    for name, m, n, x in pats:
        c.text(x + (min(n, 8) * cell) / 2, 54, name, size=12.5, weight="700")
        c.text(x + (min(n, 8) * cell) / 2, 70, f"Up to {m} of every {n} nonzero",
               size=9.5, fill="muted", weight="400")
        cols = 8
        for i in range(n):
            cx = x + (i % cols) * cell
            cy = 82 + (i // cols) * cell
            live = (i % n) < m
            c.box(cx, cy, cell - 2, cell - 2,
                  fill="blue" if live else "bg",
                  stroke="blue" if live else "line", width=1.2, rx=1)
        kept = int(100 * m / n)
        c.text(x + (min(n, 8) * cell) / 2, 82 + ((n - 1) // cols + 1) * cell + 16,
               f"Keeps at most {kept}%", size=10, fill="muted", weight="600")

    c.text(350, 178, "Filled cells show nonzero values at the pattern limit.",
           size=11, weight="600")
    c.text(350, 195, "The regular pattern lets the Tensor Engine skip multiplications by zero.",
           size=10.5, fill="muted", weight="500")
    c.text(350, 222, "Peak gains depend on input format and NeuronCore generation.",
           size=10.5, fill="blue", weight="700")


def psum_banks(c):
    """PSUM's eight banks, and what they are for."""
    c.label(24, 26, "PSUM: 128 partitions x 8 banks", fill="muted")

    c.text(88, 62, "partition 0", size=9.5, anchor="end", fill="muted", weight="600")
    c.text(88, 92, "partition 1", size=9.5, anchor="end", fill="muted", weight="600")
    c.text(88, 122, "...", size=9.5, anchor="end", fill="muted", weight="600")
    c.text(88, 152, "partition 127", size=9.5, anchor="end", fill="muted", weight="600")

    for row, y in enumerate((50, 80, 110, 140)):
        for b in range(8):
            x = 100 + b * 68
            highlight = b == 2
            c.box(x, y, 64, 24, fill="surface2" if highlight else "surface",
                  stroke="yellow" if highlight else "line",
                  width=2 if highlight else 1, rx=2)
            if row == 0:
                c.text(x + 32, 42, f"bank {b}", size=9, fill="muted", weight="700")
            if row != 2:
                c.text(x + 32, y + 16, "512 FP32", size=8.5, fill="muted", weight="400")

    c.text(350, 193, "On v3, nc_matmul writes to one bank per partition.",
           size=13, weight="700")
    c.text(350, 216, "On v4, nc_matmul can use all eight banks.",
           size=13, fill="teal", weight="700")
    c.text(350, 237, "4,096 FP32 or 8,192 BF16 elements per partition",
           size=12, fill="muted")


# --- device block diagrams --------------------------------------------------
#
# Every generation shares one structure, so one generator covers all of them.
# Modelled on the layout AWS uses in its own architecture pages: memory as edge
# stacks, a grid of NeuronCores, and the data-movement blocks underneath.

DEVICE_SPECS = {
    "inferentia-device": {
        "name": "Inferentia",
        "core": "NeuronCore-v1",
        "cores": 4,
        "cols": 2,
        "sram": "on-chip SRAM",
        "mem": "DDR",
        "mem_stacks": 2,
        "cap": "8 GiB",
        "bw": "50 GiB/s",
        "dma": "DMA engines",
        "cc": None,
        "link": "NeuronLink-v1",
        "links": 2,
        "engines": "3 engines: Tensor, Vector, Scalar",
        "summary": "64 FP16/BF16 TFLOPS  -  128 INT8 TOPS  -  8 GiB  -  50 GiB/s",
    },
    "trainium-device": {
        "name": "Trainium",
        "core": "NeuronCore-v2",
        "cores": 2,
        "cols": 2,
        "sram": "24 MiB SBUF  -  2 MiB PSUM",
        "mem": "HBM",
        "mem_stacks": 2,
        "cap": "32 GiB",
        "bw": "820 GiB/s",
        "dma": "32 DMA engines  -  1 TB/s",
        "cc": "6 CC-Cores",
        "link": "NeuronLink-v2",
        "links": 4,
        "engines": "4 engines: + GpSimd",
        "summary": "190 FP16/BF16/cFP8 TFLOPS  -  47.5 FP32  -  32 GiB  -  820 GiB/s",
    },
    "trainium2-device": {
        "name": "Trainium2",
        "core": "NeuronCore-v3",
        "cores": 8,
        "cols": 4,
        "sram": "28 MiB SBUF",
        "mem": "HBM",
        "mem_stacks": 4,
        "cap": "96 GiB",
        "bw": "2.9 TB/s",
        "dma": "128 DMA engines  -  3.5 TB/s",
        "cc": "CC-Cores (AWS sources disagree)",
        "link": "NeuronLink-v3",
        "links": 4,
        "engines": "+ sparsity, hardware DGE, DMA transpose",
        "summary": "1,299 FP8 TFLOPS  -  667 BF16  -  96 GiB  -  2.9 TB/s",
    },
    "trainium3-device": {
        "name": "Trainium3",
        "core": "NeuronCore-v4",
        "cores": 8,
        "cols": 4,
        "sram": "32 MiB SBUF",
        "mem": "HBM",
        "mem_stacks": 4,
        "cap": "144 GiB",
        "bw": "See sources",
        "dma": "128 DMA engines · inline computation",
        "cc": "CC-Cores (AWS sources disagree)",
        "link": "NeuronLink-v4",
        "links": 4,
        "engines": "+ MXFP8/MXFP4, near-memory accumulation",
        "summary": "2,517 MXFP8/MXFP4 TFLOPS  ·  671 BF16  ·  144 GiB",
    },
}


def _device_diagram(c, spec):
    """Draw one Neuron device: memory, cores, data movement, interconnect."""
    c.box(18, 18, 664, 292, fill="bg", stroke="blue", rx=10, width=2)
    c.text(38, 44, spec["name"], size=16, anchor="start", weight="700", fill="blue")

    # Host PCIe sits top-right, as in AWS's own diagrams.
    c.box(536, 30, 128, 26, fill="surface", stroke="line", rx=4)
    c.text(600, 48, "Host PCIe", size=10.5, fill="muted", weight="600")

    # memory stacks down the left edge
    stacks = spec["mem_stacks"]
    top, bottom = 82, 218
    gap = 6
    sh = (bottom - top - gap * (stacks - 1)) / stacks
    for i in range(stacks):
        y = top + i * (sh + gap)
        c.box(34, y, 46, sh, fill="surface2", stroke="teal", width=1.6, rx=3)
    c.text(57, top - 10, spec["mem"], size=10.5, weight="700")
    c.text(57, bottom + 16, spec["cap"], size=9.5, fill="muted", weight="700")
    c.text(57, bottom + 29, spec["bw"], size=9, fill="muted", weight="400")

    # NeuronCore grid
    cols = spec["cols"]
    rows = spec["cores"] // cols
    gx0, gw = 94, 578
    cw = (gw - (cols - 1) * 8) / cols
    ch_ = (bottom - top - (rows - 1) * 8) / rows
    for i in range(spec["cores"]):
        cx = gx0 + (i % cols) * (cw + 8)
        cy = top + (i // cols) * (ch_ + 8)
        c.box(cx, cy, cw, ch_, fill="surface", stroke="blue", width=1.6, rx=4)
        label = spec["core"] if cols <= 2 else spec["core"].replace("NeuronCore-", "NC-")
        if ch_ <= 100:
            c.text(cx + cw / 2, cy + ch_ / 2 - 3, label,
                   size=10.5 if cols > 2 else 12, weight="700")
        if ch_ > 100:
            # room for the engine strip: show what is actually inside a core
            c.text(cx + cw / 2, cy + 26, label, size=12, weight="700")
            c.text(cx + cw / 2, cy + 42, spec["sram"], size=9.5, fill="muted",
                   weight="400")
            names = ["Tensor", "Vector", "Scalar", "GpSimd"]
            if spec["core"].endswith("v1"):
                names = names[:3]
            ew = (cw - 32 - (len(names) - 1) * 6) / len(names)
            for k, en in enumerate(names):
                ex = cx + 16 + k * (ew + 6)
                c.box(ex, cy + 56, ew, 30, fill="surface2" if en == "Tensor" else "bg",
                      stroke="blue" if en == "Tensor" else "line", width=1.4, rx=3)
                c.text(ex + ew / 2, cy + 75, en, size=9, weight="600")
        elif ch_ > 40:
            c.text(cx + cw / 2, cy + ch_ / 2 + 13, spec["sram"],
                   size=8.5 if cols > 2 else 10, fill="muted", weight="400")

    # data movement row
    dy = 232
    if spec["cc"]:
        c.box(94, dy, 285, 26, fill="surface", stroke="teal", width=1.4, rx=3)
        c.text(236, dy + 18, spec["dma"], size=9.5, fill="muted", weight="600")
        c.box(387, dy, 285, 26, fill="surface", stroke="teal", width=1.4, rx=3)
        c.text(529, dy + 18, spec["cc"], size=9.5, fill="muted", weight="600")
    else:
        c.box(94, dy, 578, 26, fill="surface", stroke="teal", width=1.4, rx=3)
        c.text(383, dy + 18, spec["dma"], size=9.5, fill="muted", weight="600")

    # interconnect row
    ly = 268
    n = spec["links"]
    lw = (578 - (n - 1) * 8) / n
    for i in range(n):
        c.box(94 + i * (lw + 8), ly, lw, 24, fill="surface", stroke="muted",
              width=1.4, rx=3)
        c.text(94 + i * (lw + 8) + lw / 2, ly + 16, spec["link"], size=9,
               fill="muted", weight="600")

    c.text(350, 330, spec["summary"], size=11, weight="700", fill="blue")
    c.text(350, 348, spec["engines"], size=10, fill="muted", weight="500")


def _make_device(key):
    return lambda c, _k=key: _device_diagram(c, DEVICE_SPECS[_k])


def neuroncore_generations(c):
    """What each NeuronCore generation added."""
    c.label(24, 26, "What each generation added", fill="muted")

    gens = [
        ("v1", "Inferentia", ["Tensor", "Vector", "Scalar"],
         ["3 engines", "no custom ops", "no FP8", "RNE only"], "muted"),
        ("v2", "Trainium\nInferentia2", ["Tensor", "Vector", "Scalar", "GpSimd"],
         ["+ GpSimd engine", "+ control flow", "+ cFP8, TF32", "+ stochastic rounding"], "teal"),
        ("v3", "Trainium2", ["Tensor", "Vector", "Scalar", "GpSimd"],
         ["+ 2x FP8 matmul", "+ sparsity", "+ hardware DGE", "+ DMA transpose"], "blue"),
        ("v4", "Trainium3", ["Tensor", "Vector", "Scalar", "GpSimd"],
         ["+ MXFP8 / MXFP4", "+ SBUF accumulate", "+ fast exp on Vector", "MXFP8 peak: 4x BF16"], "blue"),
    ]
    x0, pw = 26, 164
    for i, (ver, chip, engines, adds, colour) in enumerate(gens):
        x = x0 + i * (pw + 4)
        c.box(x, 40, pw, 250, fill="bg", stroke=colour, width=2, rx=6)
        c.text(x + pw / 2, 62, f"NeuronCore-{ver}", size=12, weight="700")
        for j, line in enumerate(chip.split("\n")):
            c.text(x + pw / 2, 78 + j * 13, line, size=9, fill="muted", weight="400")

        ey = 104
        for e in engines:
            c.box(x + 14, ey, pw - 28, 20, fill="surface",
                  stroke="blue" if e == "Tensor" else "line", width=1.4, rx=2)
            c.text(x + pw / 2, ey + 14, e, size=9.5, weight="600")
            ey += 24
        if len(engines) == 3:
            c.box(x + 14, ey, pw - 28, 20, fill="bg", stroke="line", width=1,
                  rx=2, dash="3 3")
            c.text(x + pw / 2, ey + 14, "no GpSimd", size=9, fill="muted", weight="400")
            ey += 24

        ay = 208
        for a in adds:
            c.text(x + 14, ay, a, size=9, fill="muted", anchor="start", weight="500")
            ay += 15

        if i < 3:
            c.line(x + pw + 1, 165, x + pw + 3, 165, stroke="line", width=1)

    c.text(350, 312, "Structure settled at v2. Everything since is precision and data movement.",
           size=11, weight="700")


def torus_topology(c):
    """A 4x4 2D torus, the layout inside both Trn1 and Trn2."""
    c.label(24, 26, "16 chips in a 4x4 2D torus", fill="muted")
    ox, oy, step = 132, 52, 74
    for r in range(4):
        for col in range(4):
            x, y = ox + col * step, oy + r * step
            c.box(x, y, 52, 46, fill="surface", stroke="blue", width=1.6, rx=4)
            c.text(x + 26, y + 28, str(r * 4 + col), size=12, weight="700")
    for r in range(4):
        for col in range(4):
            x, y = ox + col * step, oy + r * step
            if col < 3:
                c.line(x + 52, y + 23, x + step, y + 23, stroke="line", width=1.5)
            if r < 3:
                c.line(x + 26, y + 46, x + 26, y + step, stroke="line", width=1.5)
    # wrap-around links are what make it a torus rather than a mesh
    for r in range(4):
        y = oy + r * step + 23
        c.path(f"M {ox} {y} C {ox - 46} {y}, {ox - 46} {y}, {ox - 28} {y}",
               stroke="teal", width=1.5, dash="4 3")
        rx = ox + 3 * step + 52
        c.path(f"M {rx} {y} C {rx + 46} {y}, {rx + 46} {y}, {rx + 28} {y}",
               stroke="teal", width=1.5, dash="4 3")
    for col in range(4):
        x = ox + col * step + 26
        c.path(f"M {x} {oy} C {x} {oy - 32}, {x} {oy - 32}, {x} {oy - 18}",
               stroke="teal", width=1.5, dash="4 3")
        by = oy + 3 * step + 46
        c.path(f"M {x} {by} C {x} {by + 32}, {x} {by + 32}, {x} {by + 18}",
               stroke="teal", width=1.5, dash="4 3")

    c.text(350, 388, "Every chip has exactly four neighbours. Dashed links wrap around,",
           size=11, weight="600")
    c.text(350, 405, "which is what makes it a torus and not a mesh.", size=10.5,
           fill="muted", weight="500")
    c.text(350, 428, "Used by trn1.32xlarge and trn2.48xlarge alike.", size=10.5,
           fill="blue", weight="700")


def inf_instances(c):
    """How many chips each Inf instance size gives you."""
    c.label(22, 26, "Inferentia instance sizes", fill="muted")

    fams = [
        ("Inf1", "NeuronCore-v1  -  4 cores per chip", [
            ("inf1.xlarge", 1), ("inf1.2xlarge", 1),
            ("inf1.6xlarge", 4), ("inf1.24xlarge", 16)], 16, "muted"),
        ("Inf2", "NeuronCore-v2  -  2 cores per chip", [
            ("inf2.xlarge", 1), ("inf2.8xlarge", 1),
            ("inf2.24xlarge", 6), ("inf2.48xlarge", 12)], 356, "blue"),
    ]
    for fam, note, sizes, x, colour in fams:
        c.box(x, 40, 328, 190, fill="bg", stroke=colour, width=2, rx=6)
        c.text(x + 164, 64, fam, size=14, weight="700")
        c.text(x + 164, 80, note, size=9.5, fill="muted", weight="400")
        y = 100
        for name, chips in sizes:
            # single row of small squares, so nothing can wrap into the label
            c.text(x + 96, y + 11, name, size=9, anchor="end", weight="600", mono=True)
            for i in range(chips):
                c.box(x + 104 + i * 11, y + 2, 9, 11, fill=colour, stroke=colour, rx=1)
            c.text(x + 108 + chips * 11, y + 11,
                   f"{chips} chip" + ("s" if chips > 1 else ""),
                   size=9, anchor="start", fill="muted", weight="700")
            y += 28

    c.text(350, 258, "Inf1 tops out at 16 chips, Inf2 at 12 — but an Inf2 chip is a whole",
           size=11, weight="600")
    c.text(350, 275, "generation newer, with 4x the memory and 16x the bandwidth.",
           size=10.5, fill="muted", weight="500")


DIAGRAMS = {
    "neuroncore": (700, 342, neuroncore),
    "memory-hierarchy": (700, 340, memory_hierarchy),
    "compile-flow": (520, 320, compile_flow),
    "workload-paths": (520, 378, workload_paths),
    "interconnect": (520, 304, interconnect),
    "stationary-moving": (700, 330, stationary_moving),
    "roofline": (700, 310, roofline),
    "inferentia-device": (700, 366, _make_device("inferentia-device")),
    "trainium-device": (700, 366, _make_device("trainium-device")),
    "trainium2-device": (700, 366, _make_device("trainium2-device")),
    "trainium3-device": (700, 366, _make_device("trainium3-device")),
    "neuroncore-generations": (700, 330, neuroncore_generations),
    "torus-topology": (700, 446, torus_topology),
    "inf-instances": (700, 292, inf_instances),
    "trn2-topology": (700, 355, trn2_topology),
    "trn3-topology": (520, 412, trn3_topology),
    "data-type-bits": (700, 330, data_type_bits),
    "engine-pipeline": (700, 270, engine_pipeline),
    "tiling": (700, 354, tiling),
    "prefill-decode": (520, 314, prefill_decode),
    "parallelism": (520, 299, parallelism),
    "generations": (700, 252, generations),
    "logical-neuroncore": (700, 268, logical_neuroncore),
    "sparsity": (700, 236, sparsity),
    "psum-banks": (700, 274, psum_banks),
}


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, (w, h, fn) in DIAGRAMS.items():
        for theme in THEMES:
            canvas = Canvas(w, h, theme)
            fn(canvas)
            path = os.path.join(OUT, f"{name}-{theme}.svg")
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(canvas.render())
        print(f"  {name}-{{light,dark}}.svg")
    print(f"{len(DIAGRAMS)} diagrams written to assets/diagrams/")


if __name__ == "__main__":
    main()
