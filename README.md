![EN](https://img.shields.io/badge/lang-English-blue) · [![FR](https://img.shields.io/badge/lang-Français-lightgrey)](./README_FR.md)

---

# Thermodynamic cartography of generative services

### *NeoMundi Recherche — version 1.0*

---

This repository publishes the first public thermodynamic cartography of generative services accessible through commercial APIs.

NeoMundi does not measure the model. NeoMundi measures the service. The unit of measurement is the triplet **Model × Stack × Time** — the service as it actually responds, in a dated window, on a given infrastructure. Measurement applies to the service output, token by token, without semantic reading of content.

## What this repository contains

The repository brings together two distinct exercises, built on the same corpus and the same instrumentation.

The first exercise establishes the **cartography**: distributions of G-Score, ΔG and FLAG rate of the five measured services, presented side by side on the same corpus. This map is NeoMundi's first public publication on the generative landscape.

The second exercise evaluates **the performance of the instrument**: for each FLAG raised by NeoMundi, the correlation with factual truthfulness judged by an independent third party (GPT-4o on TruthfulQA) is computed. The question asked is: does the instrument detect, through thermodynamic signature alone and without semantic reading, a drift correlated with factual hallucination?

## Services measured in v1.0

The five services are anonymized by default. Each service is identified by a stable anonymous identifier (P-001 to P-005). The real names of providers are not disclosed.

## Cartography — v1-2026-04-26

Runtime ratings computed deterministically from `measurements.csv` with `methodology.py` (Methodology v1.0, Public Draft). The **hallucination rate** measures the share of responses judged factually incorrect by GPT-4o on the TruthfulQA corpus.

| Provider | Observations | G-Score | FLAG rate | Composite | Rating  | Tier                | Trend | Hallucination rate |
|----------|-------------:|--------:|----------:|----------:|---------|---------------------|-------|-------------------:|
| P-002    |          780 |  0.9120 |   3.72 %  |    0.9374 | ![A](https://img.shields.io/badge/A-6F9E85?style=flat)   | Production grade    | n/a   |              40.1 % |
| P-001    |          780 |  0.9091 |   7.69 %  |    0.9161 | ![BBB](https://img.shields.io/badge/BBB-75BC5B?style=flat) | Production grade    | n/a   |              54.3 % |
| P-004    |          781 |  0.9077 |   8.96 %  |    0.9090 | ![BBB](https://img.shields.io/badge/BBB-75BC5B?style=flat) | Production grade    | n/a   |              55.7 % |
| P-003    |          782 |  0.8998 |  14.19 %  |    0.8789 | ![BB](https://img.shields.io/badge/BB-8EB848?style=flat)  | Governance-required | n/a   |              64.3 % |
| P-005    |          782 |  0.8886 |  21.48 %  |    0.8369 | ![B](https://img.shields.io/badge/B-CE842D?style=flat)   | Governance-required | n/a   |              64.5 % |

> **Headline finding.** *No observed LLM reaches AA without runtime governance.*

The color of each rating follows the colorimetric convention defined in the methodology ([§6](./Methodology_EN.md#6-colorimetric-convention)): a perceptually uniform path in the CIE Lab 1976 color space whose warm → cool inflection falls by construction at the tier boundary (BB → BBB). Reading the table requires no legend: cool-colored ratings are *Production grade*, warm-colored ratings are *Governance-required*.

The trend is `n/a` for this dataset because it is a synchronous measurement, not a continuous runtime stream. The trend (Stable / Positive / Negative) will be reported as soon as the instrument runs on production traffic over a sufficient window.

**Reproduce these ratings:**
```bash
python methodology.py        # runs reference tests on the dataset
```

[Aggregated statistics →](./data/v1-2026-04-26/summary.csv) · [Provenance and DOI →](./data/v1-2026-04-26/PROVENANCE.txt)

## Instrument calibration — v1-2026-04-26

The metrics below do not characterize the measured LLMs: they characterize **the performance of the NeoMundi instrument** at detecting factual hallucinations. Computed on 3,904 TruthfulQA measurements, ground truth established by an external LLM judge (GPT-4o, see [`Methodology_EN.md`](./Methodology_EN.md) §7.2).

> **When NeoMundi flags, it's right ≈ 76% of the time.**
> **Current recall ≈ 15%.** The instrument is calibrated conservatively: it favors precision over coverage. Better to flag less but flag right than flood with false positives.
>
> **Truth Module live on May 27, 2026** — factual verification beyond coherence.

| Provider | Observations | TP  | FP  | TN   | FN  | Precision | Recall  | F1     | Lift  |
|----------|-------------:|----:|----:|-----:|----:|----------:|--------:|-------:|------:|
| P-005    |          782 | 137 |  31 |  247 | 367 |   81.5 %  | 27.2 %  | 40.8 % | ×1.27 |
| P-003    |          782 |  85 |  26 |  253 | 418 |   76.6 %  | 16.9 %  | 27.7 % | ×1.19 |
| P-004    |          781 |  52 |  18 |  328 | 383 |   74.3 %  | 12.0 %  | 20.6 % | ×1.33 |
| P-001    |          779 |  40 |  19 |  337 | 383 |   67.8 %  |  9.5 %  | 16.6 % | ×1.25 |
| P-002    |          780 |  17 |  12 |  455 | 296 |   58.6 %  |  5.4 %  |  9.9 % | ×1.46 |
| **GLOBAL** |    **3,904** | **331** | **106** | **1,620** | **1,847** | **75.7 %** | **15.2 %** | **25.3 %** | **×1.36** |

**Definitions.**
- **TP** (True Positive): NeoMundi flags, and the response is factually incorrect.
- **FP** (False Positive): NeoMundi flags, but the response is correct (false alarm).
- **TN** (True Negative): NeoMundi passes (PASS), and the response is correct.
- **FN** (False Negative): NeoMundi passes, but the response is incorrect (missed hallucination).
- **Precision** = TP / (TP + FP): reliability of a FLAG.
- **Recall** = TP / (TP + FN): coverage on all hallucinations.
- **F1**: harmonic mean of precision and recall.
- **Lift** = Precision / Provider hallucination rate: detection multiplier vs random.

[Aggregated calibration metrics →](./data/v1-2026-04-26/calibration.csv)

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
        ├── summary.csv          ← cartography: aggregated statistics per service
        └── calibration.csv      ← calibration: instrument performance
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
