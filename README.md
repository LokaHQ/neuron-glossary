# Neuron Glossary

A plain-language reference to AWS Trainium and Inferentia. Its 98 terms cover
the chips, the software that runs on them, and how to diagnose performance.

**This glossary is not endorsed by Amazon, AWS, or Annapurna Labs.**

Read it: **https://lokahq.github.io/neuron-glossary/**

Inspired by [Modal's GPU Glossary](https://modal.com/gpu-glossary), which does
the same job for NVIDIA hardware.

## Where to start

Open [Home → README](https://lokahq.github.io/neuron-glossary/#/readme) for a tour
from PyTorch to the chip. It explains the difference between an EC2 instance,
a Neuron device, and a NeuronCore. The GPU comparison table gives CUDA users
familiar starting points, and the term pages link to related concepts and
primary references.

## Structure

```
glossary/
  device-hardware/    33 terms — chips, cores, engines, memories, interconnect
  device-software/    21 terms — NKI, NISA, NEFF, tiling, data types
  host-software/      26 terms — compiler, runtime, drivers, frameworks, tools
  perf/               18 terms — roofline, bottlenecks, parallelism strategies
assets/               themed diagrams, ASCII wordmark, and social preview PNG
utils/                renderer, stylesheet, app JS, page shell, diagram source
build.py              produces index.html
index.html            the built site (committed)
```

Each term is one Markdown file with `title` and `short` frontmatter. Internal
links use absolute glossary paths, which the build rewrites into hash routes:

```markdown
---
title: What is a NeuronCore?
short: NeuronCore
---

A **NeuronCore** is the independent compute unit inside a
[Neuron device](/neuron-glossary/device-hardware/neuron-device).
```

## Building

No dependencies. Python 3.9+ and nothing else.

```sh
python3 build.py              # write index.html
python3 build.py --check      # validate links and diagrams, fail on any problem
python3 utils/diagrams.py     # regenerate the themed SVG pairs
```

`--check` verifies internal routes, checks both themes of each diagram, and
checks the share card's PNG dimensions. Run it before opening a pull request.

The output is a single self-contained `index.html` — inline CSS and JS, inlined
SVG — that works from `file://`, with no build step for the reader. It ships
light and Terminal themes (light default, persisted, applied before first
paint), client-side search, and deep links to every term.

Glossary prose lives in `glossary/`, including the site's README
(`glossary/index.md`). The Contributors page reads `AUTHORS.md`.
`index.html` is a build artifact. Two consecutive builds are byte-identical.
Edit Markdown, then regenerate the HTML.

## Design

The interface follows [Modal's GPU Glossary](https://modal.com/gpu-glossary) —
monospace throughout, a terminal window frame, a dashed sidebar rule, breadcrumb
paths, arrow-prefixed lists, and abbreviation chips — rendered in the Loka
palette (blue `#1877F2`, green `#0C6F71`, yellow `#F7D043`, black `#050517`).

Modal uses the paid Degular Mono and CoFo Sans Pixel. The free equivalents here
are **JetBrains Mono** for body text and **Silkscreen** for the glossary title
and small pixel-style accents.

The homepage and social preview share an
[ASCII version of the Loka wordmark](assets/loka-wordmark.txt).
To redraw the preview after editing the artwork or its layout, run
`python3 utils/share_card.py` with Chrome or Chromium and access to Google Fonts.
When deploying to GitHub Pages, publish both `index.html` and
`assets/neuron-glossary-og.png` at those paths on `gh-pages`.

## Contributing

Pull requests are welcome, whether you're fixing a typo, clarifying an
explanation, or adding a term. You can also flag a correction or suggest a
topic by opening an issue. [Pull requests](https://github.com/LokaHQ/neuron-glossary/pulls) · [Issues](https://github.com/LokaHQ/neuron-glossary/issues)

For technical changes, link to the relevant public documentation. When AWS
references disagree, cite both and identify which source the entry uses for
its figures.

To add a term: create `glossary/<section>/<slug>.md`, link it from related
terms, run `python3 build.py --check`, and commit the rebuilt `index.html`.

Please do not add specifications that are not in public documentation, and do
not copy AWS's diagrams — the ones here are generated from
`utils/diagrams.py` precisely so the repository stays cleanly licensed.

## Authors

The site's Contributors page reads [AUTHORS.md](AUTHORS.md).

## Sources

The hardware and software entries draw on the
[AWS Neuron documentation](https://awsdocs-neuron.readthedocs-hosted.com/en/latest/).
Framework and lifecycle guidance uses
[Neuron 2.33.1](https://awsdocs-neuron.readthedocs-hosted.com/en/v2.33.1/release-notes/2.33.1.html)
as the baseline. The TorchNeuron entry also links to Hugging Face's Trainium
recipes. Entries with announced changes give the effective release and
hardware scope.

## License

Code is [MIT](LICENSE). The glossary text in `glossary/` and the diagrams in
`assets/diagrams/` are [CC BY 4.0](glossary/LICENSE) — share and adapt freely
with attribution.

Built by [Loka](https://www.loka.com/).
