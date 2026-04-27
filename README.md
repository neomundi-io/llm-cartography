![EN](https://img.shields.io/badge/lang-English-blue) · [![FR](https://img.shields.io/badge/lang-Français-lightgrey)](./README_FR.md)

---

# Thermodynamic cartography of generative services

### *Neomundi Recherche — version 1.0*

---

This repository publishes the first public thermodynamic cartography of generative services accessible through commercial API.

Neomundi does not measure the model. Neomundi measures the service. The unit of measurement is the triplet **Model × Stack × Time** — the service as it actually responds, at a dated window, on a given infrastructure. Measurement applies to the service output, token by token, without semantic reading of content.

## What this repository contains

The repository brings together two distinct exercises, built on the same corpus and the same instrumentation.

The first exercise evaluates the instrument. For each measured service, the correlation between the thermodynamic signature (G-Score, ΔG) and the factual truthfulness judged by an independent third party is computed. The question asked is: does the Neomundi instrument detect, through thermodynamic signature alone and without semantic reading, a drift correlated with factual hallucination?

The second exercise establishes the cartography. The distributions of G-Score, ΔG and flag rate of the five measured services are presented side by side on the same corpus. This map is Neomundi's first public publication on the generative landscape.

## Services measured in v1.0

The five services are anonymized by default. Each service is identified by a stable anonymous identifier (P-001 to P-005) and a broad geographic region. Real provider names are not disclosed in this version.

## Published measurements — v1.0 summary

## Published measurements — v1.0 summary

## Ratings — v1-2026-04-26

The first ControlTower™ Rating ever published. Computed deterministically
from `measurements.csv` using `methodology.py` (Methodology v1.0,
Public Draft).

| Provider | Observations | G-Score | FLAG rate | Composite | Rating  | Tier               | Outlook |
|----------|-------------:|--------:|----------:|----------:|---------|--------------------|---------|
| P-002    |          780 |  0.9120 |   3.72 %  |    0.9374 | **A**   | Investment grade   | n/a     |
| P-001    |          780 |  0.9091 |   7.69 %  |    0.9161 | **BBB** | Investment grade   | n/a     |
| P-004    |          781 |  0.9077 |   8.96 %  |    0.9090 | **BBB** | Investment grade   | n/a     |
| P-003    |          782 |  0.8998 |  14.19 %  |    0.8789 | **BB**  | Speculative grade  | n/a     |
| P-005    |          782 |  0.8886 |  21.48 %  |    0.8369 | **B**   | Speculative grade  | n/a     |

> **Headline finding.** *No observed LLM reaches AA without runtime governance.*

Outlook is `n/a` for this dataset because it is a synchronous measurement,
not a continuous runtime stream. Outlook (Stable / Positive / Negative)
will be reported once ControlTower™ runs on production traffic.

**Reproduce these ratings:**
```bash
python methodology.py        # runs self-tests on the reference dataset
```

Both raw dimensions (G-Score, FLAG rate) and the agglomerated rating are
shown. The composite is recomputable from the two dimensions, and the
rating from the composite using the threshold table in
[`Methodology_EN.md`](./Methodology_EN.md) §4.2.

- *Correct answers: proportion validated by LLM-as-judge (GPT-4o). 
- Neomundi precision: reliability of Neomundi flags (share of FLAG decisions correctly positioned on incorrect answers).
- Recall: share of incorrect answers actually detected by Neomundi.
- Observability (ΔG): thermodynamic drift signal measured without semantic reading.*

[Raw measurements →](./data/v1-23-04-26) · [Aggregated statistics →](./data/summary-v1)

**How to read the table.** The five services exhibit factual truthfulness rates (Correct answers) ranging from 35.55% to 59.87% on the TruthfulQA corpus, with significant dispersion. The precision of the Neomundi instrument (proportion of flags correctly positioned on incorrect answers) varies from 58.62% to 81.55% depending on the service measured. The thermodynamic signature (Observability ΔG) is the independent signal underlying the flags: it is measured without semantic reading of the content, from the generation trajectory alone.

**The salient result.** The service with the lowest factual truthfulness (P-005, 35.55%) is also the one for which the Neomundi instrument exhibits the highest precision (81.55%) and the most pronounced thermodynamic signature (20.84%). This correlation supports Neomundi's founding hypothesis: factual drift leaves a measurable trace in the thermodynamic signature of generation, independently of semantic content.

The five services were measured within the same temporal window, on the TruthfulQA corpus, with the same third-party judge (GPT-4o) and the same instrumentation.

## Anonymization

Anonymization is the default position of cartography v1.0. It expresses three commitments.

First, equality of treatment: all measured services are identified in the same way, regardless of their commercial weight, geographic origin, or relationship with Neomundi.

Second, irrevocability of the protection: an anonymous identifier cannot be lifted by Neomundi unilaterally. Only an explicit and written request from a measured provider can lead to public naming, in a subsequent version of the cartography.

Third, scientific neutrality: the instrument is evaluated on the substance of the measurements, not on the reputation of the names. A reader of the cartography compares signatures, not brands.

The procedure for lifting anonymity, on the explicit request of a measured provider, is documented in `CONTEST.md`.

## Repository layout

```
.
├── README.md                    ← this file
├── README_FR.md                 ← French version
├── METHODOLOGY_EN.md            ← detailed methodology (English)
├── METHODOLOGY_FR.md            ← detailed methodology (French)
├── CONTEST.md                   ← contestation and naming procedure
├── CITATION.cff                 ← citation format
├── LICENSE                      ← Creative Commons Attribution 4.0
└── data/
    └── v1.0/
        ├── measurements.csv     ← raw measurements per anonymous provider
        └── providers.csv        ← anonymous provider metadata
```

## Stance

Neomundi measures, attests, transmits. Governance remains the responsibility of whoever operates the service. The cartography is partial by construction and provisional by intellectual honesty — it covers a finite set of providers at a dated moment, and the instrument progresses through versioned increments.

Any measured service may request to be named publicly, or to be removed from the public cartography, at any time. Both procedures are documented in `CONTEST.md`.

Neomundi Recherche, a loi 1901 association, is hosted in Vannes, France. It publishes the cartography and sells nothing. Derived commercial activities are carried by a distinct legal entity (Louis M Sàrl, Morges, Switzerland) that operates only with service buyers, and never with measured providers.

## How to cite

The recommended citation format is provided in the `CITATION.cff` file. The Zenodo DOI for v1.0 will be added to this README upon publication.

## To go further

The full methodology — object of measurement, instrumentation, protocol, corpus, limitations, versioning, planned scale — is described in [METHODOLOGY_EN.md](./Methodology_EN).

The Law E theoretical framework on which the instrumentation relies is deposited separately on Zenodo, DOI 10.5281/zenodo.19385052.

## License

Creative Commons Attribution 4.0 International (CC-BY-4.0). Free reuse with attribution to Neomundi Recherche.

## Contact

`recherche@neomundi.org`

---

*The map is partial. The instrument progresses. The methodology is public.*

