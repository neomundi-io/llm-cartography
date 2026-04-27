# Runtime rating of LLMs

> *We observe, we do not judge.*

A reproducible methodology for measuring the runtime stability of Large
Language Models, with a public reference dataset and a permanently
frozen grade vocabulary.

🌍 [Français](README_FR.md)

## What this is

This repository contains the specification, reference implementation,
and reference dataset for the runtime rating of LLMs.

The rating is built from two structurally orthogonal runtime
measurements (G-Score, FLAG rate), aggregated into a composite,
classified onto a 7-grade scale (AAA…CCC), and complemented by a
trend indicator over time.

The methodology is fully open and versioned. The reference dataset
is anonymized: providers appear under pseudonymous identifiers
(P-001, P-002, …). The mapping to commercial names is not
published.

## Architecture

```
[runtime traffic]
       │
       ▼
   Layer 1 — Measurement      → G-Score, FLAG events
   Layer 2 — Aggregation      → composite score
   Layer 3 — Classification   → rating (AAA…CCC) + tier
   Layer 4 — Trend            → Stable / Positive / Negative
       +
   Colorimetric convention    → frozen hex codes per grade
```

Four measurement layers, plus a transversal colorimetric convention.
Full specification in [`Methodology_EN.md`](Methodology_EN.md).

## Headline finding (v1-2026-04-26 dataset)

> *No observed LLM reaches level AA without runtime governance.*

Across the five providers measured: 1 reaches A, 2 reach BBB, 1 BB,
1 B. The AAA and AA bands remain empty in raw observation. Runtime
governance shifts the operational composite upward by filtering FLAG
events.

DOI of the reference dataset: [10.5281/zenodo.19762753](https://doi.org/10.5281/zenodo.19762753)

## Quick start

```bash
git clone https://github.com/Neomundi-Labs/<repo-name>.git
cd <repo-name>
python -m venv venv && source venv/bin/activate
pip install pandas numpy
python methodology.py     # runs self-tests
python score.py           # produces ratings.csv from public/measurements.csv
```

Full step-by-step instructions: [`USAGE_FR.md`](USAGE_FR.md).

## Status

Methodology **v1.0 — Public Draft** (revision 2026-04-27).

The methodology is versioned. The grade vocabulary (AAA…CCC) is
permanently frozen. Any methodological change is published as a
dated and timestamped Methodology Update Document. See
[`Methodology_EN.md`](Methodology_EN.md) §9 for the versioning rules.

## File map

| File | Role |
|---|---|
| [`Methodologie_FR.md`](Methodologie_FR.md) | Methodology specification (French — source of truth) |
| [`Methodology_EN.md`](Methodology_EN.md) | Methodology specification (English translation) |
| [`USAGE_FR.md`](USAGE_FR.md) | Step-by-step usage guide |
| `methodology.py` | Reference implementation: scoring (frozen) |
| `score.py` | Pipeline runner: `measurements.csv` → `ratings.csv` |
| `anonymize_release.py` | Anonymization pipeline (raw → public) |
| `judge_truthfulqa.py` | LLM judge calibration (optional) |
| `CHECKSUMS.sha256` | Integrity checksums for all versioned files |
| `License` | Repository license |
| `data/` | Historical reference datasets (immutable) |
| `public/` | Anonymized publishable outputs |

## Three sources of truth

The repository carries three independent sources of truth for three
distinct concerns:

- **`methodology.py`** — scoring (layers 2, 3, 4, and colorimetric convention)
- **`anonymize_release.py`** — publication (anonymization, hashing, public schema)
- **`judge_truthfulqa.py`** — calibration (TruthfulQA ground truth, TP/FP/TN/FN)

All three are version-tagged together at each release.

## Citation

```
NeoMundi Recherche, 2026.
Runtime rating of LLMs — Reference dataset v1-2026-04-26.
DOI: 10.5281/zenodo.19762753
```

## License

Code: MIT (see `License`).
Data and methodology: CC-BY-4.0.

## About

NeoMundi Recherche is a research initiative on AI runtime stability
measurement. Operated by NeoMundi Recherche (association loi 1901,
France) and Louis M Sàrl (Switzerland).

Contact: contact@neomundi.org
