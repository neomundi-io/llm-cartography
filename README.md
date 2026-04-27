![EN](https://img.shields.io/badge/lang-English-blue) · [![FR](https://img.shields.io/badge/lang-Français-lightgrey)](./README_FR.md)

---

# Thermodynamic cartography of generative services

### *NeoMundi Recherche — version 1.0*

---

This repository publishes the first public thermodynamic cartography of generative services accessible through commercial APIs.

NeoMundi does not measure the model. NeoMundi measures the service. The unit of measurement is the triplet **Model × Stack × Time** — the service as it actually responds, in a dated window, on a given infrastructure. Measurement applies to the service output, token by token, without semantic reading of content.

## What this repository contains

The repository brings together two distinct exercises, built on the same corpus and the same instrumentation.

The first exercise evaluates the instrument. For each measured service, the correlation between the thermodynamic signature (G-Score, ΔG) and the factual truthfulness judged by an independent third party is computed. The question asked is: does the NeoMundi instrument detect, through thermodynamic signature alone and without semantic reading, a drift correlated with factual hallucination?

The second exercise establishes the cartography. The distributions of G-Score, ΔG and FLAG rate of the five measured services are presented side by side on the same corpus. This map is NeoMundi's first public publication on the generative landscape.

## Services measured in v1.0

The five services are anonymized by default. Each service is identified by a stable anonymous identifier (P-001 to P-005). The real names of providers are not disclosed.

## Ratings — v1-2026-04-26

The first runtime ratings ever published. Computed deterministically from `measurements.csv` with `methodology.py` (Methodology v1.0, Public Draft).

| Provider | Observations | G-Score | FLAG rate | Composite | Rating  | Tier                | Trend |
|----------|-------------:|--------:|----------:|----------:|---------|---------------------|-------|
| P-002    |          780 |  0.9120 |   3.72 %  |    0.9374 | ![A](https://img.shields.io/badge/A-6F9E85?style=flat)   | Production grade    | n/a   |
| P-001    |          780 |  0.9091 |   7.69 %  |    0.9161 | ![BBB](https://img.shields.io/badge/BBB-75BC5B?style=flat) | Production grade    | n/a   |
| P-004    |          781 |  0.9077 |   8.96 %  |    0.9090 | ![BBB](https://img.shields.io/badge/BBB-75BC5B?style=flat) | Production grade    | n/a   |
| P-003    |          782 |  0.8998 |  14.19 %  |    0.8789 | ![BB](https://img.shields.io/badge/BB-8EB848?style=flat)  | Governance-required | n/a   |
| P-005    |          782 |  0.8886 |  21.48 %  |    0.8369 | ![B](https://img.shields.io/badge/B-CE842D?style=flat)   | Governance-required | n/a   |

> **Headline finding.** *No observed LLM reaches AA without runtime governance.*

The color of each rating follows the colorimetric convention defined in the methodology ([§6](./Methodology_EN.md#6-colorimetric-convention)): a perceptually uniform path in the CIE Lab 1976 color space whose warm → cool inflection falls by construction at the tier boundary (BB → BBB). Reading the table requires no legend: cool-colored ratings are *Production grade*, warm-colored ratings are *Governance-required*.

The trend is `n/a` for this dataset because it is a synchronous measurement, not a continuous runtime stream. The trend (Stable / Positive / Negative) will be reported as soon as the instrument runs on production traffic over a sufficient window.

**Reproduce these ratings:**
```bash
python methodology.py        # runs reference tests on the dataset
```

The two raw dimensions (G-Score, FLAG rate) and the agglomerated rating are all displayed. The composite is recomputable from the two dimensions, and the rating from the composite via the threshold table in [`Methodology_EN.md`](./Methodology_EN.md) §4.2.

- *Correct answers: proportion validated by LLM-as-judge (GPT-4o).*
- *NeoMundi precision: reliability of flags (proportion of FLAGs correctly positioned on incorrect responses).*
- *Recall: proportion of errors effectively detected by NeoMundi.*
- *Observability (ΔG): measured thermodynamic drift signal.*

[Aggregated statistics →](./data/v1-2026-04-26/summary.csv) · [Provenance and DOI →](./data/v1-2026-04-26/PROVENANCE.txt)

The five services were measured in the same temporal window, on the TruthfulQA corpus, with the same third-party judge (GPT-4o) and the same instrumentation.

## Anonymization

Anonymization is the structural posture of the v1.0 cartography. It expresses three commitments.

First, equality of treatment: all measured services are identified in the same way, regardless of their commercial weight, geographical origin, or relationship with NeoMundi.

Second, scientific neutrality: the instrument is evaluated on the substance of the measurements, not on the reputation of names. A reader of the cartography compares signatures, not brands.

Third, methodological stability: no notification, withdrawal, or anonymity-lifting procedure is offered. The v1.0 cartography is fully and durably anonymous.

A provider wishing to know its individual positioning may request a free individual diagnostic from NeoMundi Recherche. This diagnostic does not modify the public cartography.

Any future evolution toward a nominative cartography will be published as a dated and timestamped Methodology Update Document. Past ratings would remain historically visible in their anonymized form. Cf. [`Methodology_EN.md`](./Methodology_EN.md) §7.3.

## Repository layout

```
.
├── README.md                    ← this file (English)
├── README_FR.md                 ← French version
├── Methodologie_FR.md           ← detailed methodology (French — source of truth)
├── Methodology_EN.md            ← detailed methodology (English)
├── USAGE_FR.md                  ← step-by-step usage guide (French)
├── USAGE_EN.md                  ← step-by-step usage guide (English)
├── methodology.py               ← reference implementation (layers 2/3/4 + colorimetry)
├── score.py                     ← rating pipeline runner
├── anonymize_release.py         ← anonymization pipeline (raw → publishable)
├── judge_truthfulqa.py          ← LLM judge calibration (optional)
├── CHECKSUMS.sha256             ← integrity hashes for all versioned files
├── License                      ← repository license
└── data/
    └── v1-2026-04-26/
        ├── PROVENANCE.txt       ← provenance and Zenodo DOI of the dataset
        └── summary.csv          ← aggregated statistics per anonymous provider
```

## Posture

NeoMundi measures, attests, transmits. Governance remains the responsibility of those who operate the service. The cartography is partial by construction and provisional by honesty — it covers a finite set of services at a dated moment, and the instrument progresses through versioned increments.

NeoMundi Recherche, a French not-for-profit association (loi 1901), is based in Vannes, France. It publishes the cartography and sells nothing. Derived commercial activities are carried by a separate legal entity (Louis M Sàrl, Morges, Switzerland) which engages only with users of generative services, and never with measured providers.

## How to cite

```
NeoMundi Recherche, 2026.
Thermodynamic cartography of generative services — Reference dataset v1-2026-04-26.
DOI: 10.5281/zenodo.19762753
```

## Further reading

The complete methodology — measurement object, instrumentation, protocol, corpus, limitations, versioning, planned scale — is described in [`Methodology_EN.md`](./Methodology_EN.md).

The theoretical framework called law E on which the instrumentation is based is deposited separately on Zenodo, DOI [10.5281/zenodo.19385052](https://doi.org/10.5281/zenodo.19385052).

## License

Code: MIT.
Data and methodology: Creative Commons Attribution 4.0 International (CC-BY-4.0).
Free reuse with attribution to NeoMundi Recherche. See the [`License`](./License) file.

## Contact

`recherche@neomundi.org`

---

*The map is partial. The instrument progresses. The methodology is public.*
