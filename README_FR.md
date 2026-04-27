[![EN](https://img.shields.io/badge/lang-English-lightgrey)](./README.md) · ![FR](https://img.shields.io/badge/lang-Français-blue)

---

# Cartographie thermodynamique des services génératifs

### *NeoMundi Recherche — version 1.0*

---

Ce dépôt publie la première cartographie thermodynamique publique des services génératifs accessibles par API commerciale.

NeoMundi ne mesure pas le modèle. NeoMundi mesure le service. L'unité de mesure est le triplet **Modèle × Stack × Temps** — le service tel qu'il répond réellement, à une fenêtre datée, sur une infrastructure donnée. La mesure porte sur la sortie du service, token par token, sans lecture sémantique du contenu.

## Ce que contient ce dépôt

Le dépôt rassemble deux exercices distincts, construits sur le même corpus et la même instrumentation.

Le premier exercice établit la **cartographie** : les distributions de G-Score, ΔG et taux de FLAG des cinq services mesurés, présentées côte à côte sur le même corpus. Cette carte est la première publication publique de NeoMundi sur le paysage génératif.

Le second exercice évalue **la performance de l'instrument** : pour chaque FLAG levé par NeoMundi, la corrélation avec la véracité factuelle jugée par un tiers indépendant (GPT-4o sur TruthfulQA) est calculée. La question posée est : l'instrument détecte-t-il, par la seule signature thermodynamique et sans lecture sémantique, une dérive corrélée à l'hallucination factuelle ?

## Services mesurés en v1.0

Les cinq services sont anonymisés par défaut. Chaque service est identifié par un identifiant anonyme stable (P-001 à P-005). Les noms réels des providers ne sont pas divulgués.

## Cartographie — v1-2026-04-26

Notes runtime calculées de manière déterministe à partir de `measurements.csv` avec `methodology.py` (Méthodologie v1.0, Public Draft). Le **taux d'hallucination** mesure la part de réponses jugées factuellement incorrectes par GPT-4o sur le corpus TruthfulQA.

| Provider | Observations | G-Score | Taux FLAG | Composite | Note    | Tier                | Tendance | Taux d'hallucination |
|----------|-------------:|--------:|----------:|----------:|---------|---------------------|----------|---------------------:|
| P-002    |          780 |  0,9120 |   3,72 %  |    0,9374 | ![A](https://img.shields.io/badge/A-6F9E85?style=flat)   | Production grade    | n/a      |              40,1 %  |
| P-001    |          780 |  0,9091 |   7,69 %  |    0,9161 | ![BBB](https://img.shields.io/badge/BBB-75BC5B?style=flat) | Production grade    | n/a      |              54,3 %  |
| P-004    |          781 |  0,9077 |   8,96 %  |    0,9090 | ![BBB](https://img.shields.io/badge/BBB-75BC5B?style=flat) | Production grade    | n/a      |              55,7 %  |
| P-003    |          782 |  0,8998 |  14,19 %  |    0,8789 | ![BB](https://img.shields.io/badge/BB-8EB848?style=flat)  | Governance-required | n/a      |              64,3 %  |
| P-005    |          782 |  0,8886 |  21,48 %  |    0,8369 | ![B](https://img.shields.io/badge/B-CE842D?style=flat)   | Governance-required | n/a      |              64,5 %  |

> **Conclusion principale.** *Aucun LLM observé n'atteint AA sans gouvernance runtime.*

La couleur de chaque note suit la convention colorimétrique fixée dans la méthodologie ([§6](./Methodologie_FR.md#6-convention-colorimétrique)) : un chemin perceptuellement uniforme dans l'espace CIE Lab 1976 dont l'inflection chaud → froid tombe par construction à la frontière de tier (BB → BBB). Lire le tableau ne nécessite aucune légende : les notes froides sont *Production grade*, les notes chaudes sont *Governance-required*.

La tendance est `n/a` pour ce jeu de données car il s'agit d'une mesure synchrone, pas d'un flux runtime continu. La tendance (Stable / Positive / Négative) sera renseignée dès que l'instrument tournera sur du trafic de production sur une fenêtre suffisante.

**Reproduire ces notes :**
```bash
python methodology.py        # lance les tests de référence sur le jeu de données
```

[Statistiques agrégées →](./data/v1-2026-04-26/summary.csv) · [Provenance et DOI →](./data/v1-2026-04-26/PROVENANCE.txt)

## Calibration de l'instrument — v1-2026-04-26

Les métriques ci-dessous ne caractérisent pas les LLM mesurés : elles caractérisent **la performance de l'instrument NeoMundi** à détecter les hallucinations factuelles. Calculées sur 3 904 mesures TruthfulQA, vérité-terrain établie par un juge LLM externe (GPT-4o, voir [`Methodologie_FR.md`](./Methodologie_FR.md) §7.2).

> **Quand NeoMundi flag, il a raison ≈ 76 % du temps.**
> **Recall actuel ≈ 15 %.** L'instrument est calibré conservateur : il privilégie la précision sur la couverture. Mieux vaut moins flagger mais flagger juste, qu'inonder de faux positifs.
>
> **Module Vérité actif le 27 mai 2026** — vérification factuelle au-delà de la cohérence.

| Provider | Observations | TP  | FP  | TN   | FN  | Précision | Recall  | F1     | Lift  |
|----------|-------------:|----:|----:|-----:|----:|----------:|--------:|-------:|------:|
| P-005    |          782 | 137 |  31 |  247 | 367 |   81,5 %  | 27,2 %  | 40,8 % | ×1,27 |
| P-003    |          782 |  85 |  26 |  253 | 418 |   76,6 %  | 16,9 %  | 27,7 % | ×1,19 |
| P-004    |          781 |  52 |  18 |  328 | 383 |   74,3 %  | 12,0 %  | 20,6 % | ×1,33 |
| P-001    |          779 |  40 |  19 |  337 | 383 |   67,8 %  |  9,5 %  | 16,6 % | ×1,25 |
| P-002    |          780 |  17 |  12 |  455 | 296 |   58,6 %  |  5,4 %  |  9,9 % | ×1,46 |
| **GLOBAL** |    **3 904** | **331** | **106** | **1 620** | **1 847** | **75,7 %** | **15,2 %** | **25,3 %** | **×1,36** |

**Définitions.**
- **TP** (True Positive) : NeoMundi flag, et la réponse est effectivement factuellement incorrecte.
- **FP** (False Positive) : NeoMundi flag, mais la réponse est correcte (fausse alerte).
- **TN** (True Negative) : NeoMundi laisse passer (PASS), et la réponse est correcte.
- **FN** (False Negative) : NeoMundi laisse passer, mais la réponse est incorrecte (hallucination ratée).
- **Précision** = TP / (TP + FP) : fiabilité d'un FLAG.
- **Recall** = TP / (TP + FN) : couverture sur les hallucinations totales.
- **F1** : moyenne harmonique précision/recall.
- **Lift** = Précision / Taux d'hallucination du provider : multiplicateur de détection vs hasard.

[Métriques de calibration agrégées →](./data/v1-2026-04-26/calibration.csv)

## Anonymisation

L'anonymisation est la position structurelle de la cartographie v1.0. Elle exprime trois engagements.

D'abord, l'égalité de traitement : tous les services mesurés sont identifiés de la même manière, indépendamment de leur poids commercial, de leur origine géographique, ou de leur relation avec NeoMundi.

Ensuite, la neutralité scientifique : l'instrument est évalué sur le fond des mesures, pas sur la réputation des noms. Un lecteur de la cartographie compare des signatures, pas des marques.

Enfin, la stabilité méthodologique : aucune procédure de notification, de retrait, ni de levée d'anonymat n'est offerte. La cartographie v1.0 est intégralement et durablement anonyme.

Un fournisseur souhaitant connaître son positionnement personnel peut demander un diagnostic individuel gratuit auprès de NeoMundi Recherche. Ce diagnostic ne modifie pas la cartographie publique.

L'éventuelle évolution vers une cartographie nominative sera publiée comme Methodology Update Document daté et horodaté. Toute notation passée resterait visible historiquement sous sa forme anonymisée. Cf. [`Methodologie_FR.md`](./Methodologie_FR.md) §7.3.

## Organisation du dépôt

```
.
├── README.md                    ← version anglaise
├── README_FR.md                 ← ce fichier
├── Methodologie_FR.md           ← méthodologie détaillée (français — source de vérité)
├── Methodology_EN.md            ← méthodologie détaillée (anglais)
├── USAGE_FR.md                  ← guide d'utilisation pas-à-pas (français)
├── USAGE_EN.md                  ← guide d'utilisation pas-à-pas (anglais)
├── methodology.py               ← implémentation de référence (couches 2/3/4 + colorimétrie)
├── score.py                     ← runner du pipeline de notation
├── anonymize_release.py         ← pipeline d'anonymisation (raw → publiable)
├── judge_truthfulqa.py          ← calibration juge LLM (optionnel)
├── CHECKSUMS.sha256             ← empreintes d'intégrité de tous les fichiers versionnés
├── License                      ← licence du dépôt
└── data/
    └── v1-2026-04-26/
        ├── PROVENANCE.txt       ← provenance et DOI Zenodo du dataset
        ├── summary.csv          ← cartographie : statistiques agrégées par service
        └── calibration.csv      ← calibration : performance de l'instrument
```

## Posture

NeoMundi mesure, atteste, transmet. La gouvernance reste la responsabilité de celui qui opère le service. La cartographie est partielle par construction et provisoire par honnêteté — elle couvre un ensemble fini de services à un instant daté, et l'instrument progresse par paliers versionnés.

NeoMundi Recherche, association loi 1901, est hébergée à Paris, France. Elle publie la cartographie et ne vend rien. Les activités commerciales dérivées sont portées par une entité juridique distincte (Louis M Sàrl, Morges, Suisse).

## Comment citer

```
NeoMundi Recherche, 2026.
Cartographie thermodynamique des services génératifs — Dataset de référence v1-2026-04-26.
DOI : 10.5281/zenodo.19762753
```

## Pour aller plus loin

La méthodologie complète — objet de mesure, instrumentation, protocole, corpus, limites, versionnement, échelle prévue — est décrite dans [`Methodologie_FR.md`](./Methodologie_FR.md).

Le cadre théorique appelé loi E sur lequel repose l'instrumentation est déposé séparément sur Zenodo, DOI [10.5281/zenodo.19385052](https://doi.org/10.5281/zenodo.19385052).

## Licence

Code : MIT.
Données et méthodologie : Creative Commons Attribution 4.0 International (CC-BY-4.0).
Libre réutilisation avec attribution à NeoMundi Recherche. Voir le fichier [`License`](./License).

## Contact

`recherche@neomundi.org`

---

*La carte est partielle. L'instrument progresse. La méthodologie est publique.*
