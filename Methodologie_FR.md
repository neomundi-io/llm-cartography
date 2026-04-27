# Notation runtime des LLM

> *Nous observons, nous ne jugeons pas.*

Une méthodologie reproductible pour mesurer la stabilité runtime des
Large Language Models, avec un dataset de référence public et un
vocabulaire de notation figé de façon permanente.

🌍 [English](README.md)

## De quoi il s'agit

Ce dépôt contient la spécification, l'implémentation de référence, et
le dataset de référence pour la notation runtime des LLM.

La notation est construite à partir de deux mesures runtime
structurellement orthogonales (G-Score, taux de FLAG), agglomérées en
un score composite, classifiées sur une échelle à 7 grades
(AAA…CCC), et complétées par un indicateur de tendance dans le
temps.

La méthodologie est entièrement ouverte et versionnée. Le dataset
de référence est anonymisé : les fournisseurs apparaissent sous
identifiants pseudonymes (P-001, P-002, …). Le mapping vers les
noms commerciaux n'est pas publié.

## Architecture

```
[trafic runtime]
       │
       ▼
   Couche 1 — Mesure          → G-Score, événements FLAG
   Couche 2 — Agrégation      → score composite
   Couche 3 — Classification  → note (AAA…CCC) + tier
   Couche 4 — Tendance        → Stable / Positive / Négative
       +
   Convention colorimétrique  → codes hex figés par grade
```

Quatre couches de mesure, plus une convention colorimétrique
transversale. Spécification complète dans
[`Methodologie_FR.md`](Methodologie_FR.md).

## Conclusion principale (jeu de données v1-2026-04-26)

> *Aucun LLM observé n'atteint le niveau AA sans gouvernance runtime.*

Sur les cinq fournisseurs mesurés : 1 atteint A, 2 atteignent BBB,
1 BB, 1 B. Les bandes AAA et AA restent vides en observation brute.
La gouvernance runtime déplace le composite opérationnel vers le
haut en filtrant les événements FLAG.

DOI du dataset de référence : [10.5281/zenodo.19762753](https://doi.org/10.5281/zenodo.19762753)

## Démarrage rapide

```bash
git clone https://github.com/Neomundi-Labs/<nom-du-repo>.git
cd <nom-du-repo>
python -m venv venv && source venv/bin/activate
pip install pandas numpy
python methodology.py     # lance les self-tests
python score.py           # produit ratings.csv depuis public/measurements.csv
```

Instructions détaillées pas-à-pas : [`USAGE_FR.md`](USAGE_FR.md).

## Statut

Méthodologie **v1.0 — Public Draft** (révision 2026-04-27).

La méthodologie est versionnée. Le vocabulaire des grades (AAA…CCC)
est figé de façon permanente. Toute modification méthodologique est
publiée sous forme de Methodology Update Document, daté et
horodaté. Voir [`Methodologie_FR.md`](Methodologie_FR.md) §9 pour
les règles de versionnement.

## Carte des fichiers

| Fichier | Rôle |
|---|---|
| [`Methodologie_FR.md`](Methodologie_FR.md) | Spécification méthodologique (français — source de vérité) |
| [`Methodology_EN.md`](Methodology_EN.md) | Spécification méthodologique (traduction anglaise) |
| [`USAGE_FR.md`](USAGE_FR.md) | Guide d'utilisation pas-à-pas |
| `methodology.py` | Implémentation de référence : scoring (figé) |
| `score.py` | Runner pipeline : `measurements.csv` → `ratings.csv` |
| `anonymize_release.py` | Pipeline d'anonymisation (raw → public) |
| `judge_truthfulqa.py` | Calibration juge LLM (optionnel) |
| `CHECKSUMS.sha256` | Empreintes d'intégrité de tous les fichiers versionnés |
| `License` | Licence du dépôt |
| `data/` | Datasets de référence historiques (immuables) |
| `public/` | Sorties publiables anonymisées |

## Trois sources de vérité

Le dépôt porte trois sources de vérité indépendantes pour trois
préoccupations distinctes :

- **`methodology.py`** — scoring (couches 2, 3, 4, et convention colorimétrique)
- **`anonymize_release.py`** — publication (anonymisation, hashing, schéma public)
- **`judge_truthfulqa.py`** — calibration (vérité-terrain TruthfulQA, TP/FP/TN/FN)

Les trois sont version-tagguées ensemble à chaque release.

## Citation

```
NeoMundi Recherche, 2026.
Runtime rating of LLMs — Reference dataset v1-2026-04-26.
DOI : 10.5281/zenodo.19762753
```

## Licence

Code : MIT (voir `License`).
Données et méthodologie : CC-BY-4.0.

## À propos

NeoMundi Recherche est une initiative de recherche sur la mesure
de stabilité runtime des IA. Opérée par NeoMundi Recherche
(association loi 1901, France) et Louis M Sàrl (Suisse).

Contact : contact@neomundi.org
