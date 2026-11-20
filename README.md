# Slides LaTeX Template

A Pandoc Beamer template for academic presentations, built with LuaLaTeX.
White slides use a pale title band, navy headings, a burgundy footer and
crimson accents. Every project can replace the palette and cover metadata.

Licensed under GNU GPL version 3 or, at your option, any later version.
See [LICENSE](LICENSE). The example logo is an original, neutral monogram;
no university logo or institutional endorsement is bundled.

## Build through the template library

Install Pandoc 3.1 or later, LuaLaTeX and the TeX Live packages listed in
`requirements.txt`. That file contains `tlmgr` package names, not Python
dependencies. TeX Live resolves their dependencies. The fonts are Fira Sans,
Fira Mono and Latin Modern Math, supplied by TeX Live rather than host fonts.

With this repository installed as `templates/slides` in TexTemplates:

```sh
generate-pdf.sh --project /path/to/presentation --template slides
```

To build the bundled example from the library root:

```sh
bin/generate-pdf.sh --project templates/slides/usage_example --template slides
```

The library discovers project defaults and automatically runs its shared
Markdown `!include` filter. Template selection is local to that build;
the environment hook exports only the library's standard `TEX_TEMPLATE_*`
variables and a non-recursive TeX search root.

## Project structure

```text
presentation/
├── defaults.yaml
├── metadata.yml
├── slides.md
├── assets/
│   └── logo.pdf
└── build/
```

Project `defaults.yaml` selects the input, metadata and output:

```yaml
from: markdown+raw_tex
input-file: '${.}/slides.md'
metadata-file: '${.}/metadata.yml'
output-file: '${.}/build/slides.pdf'
resource-path:
  - '${.}'
```

Template defaults select the Beamer writer, LuaLaTeX, a 16:9 aspect ratio and
slide level 2. Use `## Frame title` for each frame. `# Section` groups frames
without inserting extra frames automatically. For longer decks, use
`!include sections/01-introduction.md` in a master Markdown file when building
through the library. Keep editorial metadata in the master project's YAML.

## Cover and palette

```yaml
deck: LECTURE 1
title: Linear classifiers and learned representations
subtitle: From decision boundaries to neural networks
shorttitle: Linear classifiers and MLPs
author:
  - Giulio Salvi
team: Research team
institute: Example organisation
lang: en
logo: assets/logo.pdf
transition: fade
transition-duration: 0.5
slides-primary: '7A0026'
slides-accent: 'C70039'
slides-heading: '14243F'
slides-title-background: 'FAE8EF'
slides-text: '202633'
slides-muted: '6B7C92'
```

`deck` appears at the top left, and the optional `logo` at the top right.
Title, subtitle and separator form the central block. Author, optional team,
organisation and date appear below. Omit unused fields, including `logo`.
Supply a PDF, PNG or JPEG logo relative to the project working directory.
The cover is intended for a title of about two lines and a short subtitle.

The footer uses `shorttitle`, falling back to `title`; `footer-text` overrides
it. Palette values are quoted six-digit HTML colours without `#`:

| Metadata key | Used for |
| --- | --- |
| `slides-primary` | Cover title and left footer |
| `slides-accent` | Deck label, separator, bullets and right footer |
| `slides-heading` | Frame titles and cover subtitle |
| `slides-title-background` | Title band and block backgrounds |
| `slides-text` | Body and author |
| `slides-muted` | Team, organisation and secondary text |

Put these values in project `metadata.yml`; there is no need to edit the
template. Standard font variables `mainfont`, `monofont` and `mathfont` can
override its fonts. `mainfont` controls the sans-serif presentation face.
Project `variables.aspectratio` and `variables.fontsize` can override the
template defaults in `defaults.yaml`.

## Progressive reveals and numbering

Beamer overlays simulate element animation with successive PDF pages.
For a list that reveals one item per page:

```markdown
## Build an argument

::: incremental

- Observe the data.
- Construct a model.
- Evaluate its predictions.

:::
```

Use a standalone `\pause` between paragraphs, or native Beamer overlay
commands such as `\only<2>{...}`, `\uncover<2->{...}` and `overprint` for
precise control. Pandoc's project option `incremental: true` makes all lists
incremental; keep it unset when only selected lists should reveal.

The cover counts as frame 1. The footer uses native
`\insertframenumber / \inserttotalframenumber`: every overlay of a frame keeps
the same number. PDF page labels count physical pages separately. The example
contains **8 frames and 12 PDF pages**. PDF navigation therefore advances on
every reveal while the footer advances only on a new frame.

For an overlay-free export, set `handout: true` in metadata. Plain frames hide
the regular header/footer; Beamer's `noframenumbering` frame option can exclude
an exceptional frame explicitly. The default cover remains counted.
For mutually exclusive `overprint` views, use handout selectors such as
`\onslide<1|handout:0>` and `\onslide<2|handout:1>` to choose the final view,
as shown in the example.

## Transitions between frames

`transition` sets the deck default; `transition-duration` sets seconds.
The default effect applies only to the first overlay of each frame, so
ordinary reveals do not replay it. Supported names include `none`, `fade`,
`dissolve`, `wipe`, `push`, `cover` and the other native Beamer transitions.

Override an individual frame in its Markdown body:

```latex
\SlideTransition[duration=0.8,direction=0]{wipe}
```

The optional overlay specification allows a deliberate exception:
`\SlideTransition<2>[duration=0.4]{fade}`. Standard Beamer commands also work,
for example `\transpush<1>[direction=90,duration=0.5]`.

These are native PDF transition instructions, not embedded video. Their
appearance depends on the PDF viewer and presentation mode; a viewer may
ignore them. Progressive pages remain usable in every PDF viewer.

## Direct Pandoc use

From this repository root:

```sh
export TEX_TEMPLATE_HOME="$PWD"
. ./environment.sh
cd usage_example
pandoc --defaults="$TEX_TEMPLATE_HOME/defaults.yaml" \
       --defaults=defaults.yaml \
       --template="$TEX_TEMPLATE_PATH"
```

The standalone template does not install the library's shared include filter.
Use the library command for projects containing `!include` directives.

## Releases and checks

`scripts/package-release.py --tag v0.1.0 --output dist` packages the exact
committed tag using `.gitattributes`. Runtime archives contain the template,
styles, defaults, environment hook, requirements, README and licence. They
exclude Git files, CI, scripts and `usage_example`.

CI compiles the extracted archive and verifies the example's frame count,
physical pages, footer counters, page labels and transition dictionaries.
A `vX.Y.Z` tag publishes `slides-X.Y.Z.tar.gz`, metadata JSON and `SHA256SUMS`.
The library can then select that exact release through its submodule commit.

For automatic notifications, configure `LIBRARY_REPOSITORY` as an Actions
repository variable with value `GiulioSalvi/TexTemplates`, and add an Actions
secret `LIBRARY_DISPATCH_TOKEN` authorised for Contents write on the library.
Without the variable, publication works and notification is skipped. Never
commit credentials or add a personal token to the template environment hook.

Primary documentation: [Pandoc slides](https://pandoc.org/MANUAL.html#producing-slide-shows-with-pandoc)
and the [Beamer manual](https://ctan.org/pkg/beamer).
