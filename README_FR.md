[![EN](https://img.shields.io/badge/lang-English-lightgrey)](./README.md) · ![FR](https://img.shields.io/badge/lang-Français-blue)

---

# Cartographie thermodynamique des services génératifs

### *NeoMundi Recherche — version 1.0*

---

Ce dépôt publie la première cartographie thermodynamique publique des services génératifs accessibles par API commerciale.

NeoMundi ne mesure pas le modèle. NeoMundi mesure le service. L'unité de mesure est le triplet **Modèle × Stack × Temps** — le service tel qu'il répond réellement, à une fenêtre datée, sur une infrastructure donnée. La mesure porte sur la sortie du service, token par token, sans lecture sémantique du contenu.

## Ce que contient ce dépôt

Le dépôt rassemble deux exercices distincts, construits sur le même corpus et la même instrumentation.

Le premier exercice évalue l'instrument. Pour chaque service mesuré, la corrélation entre la signature thermodynamique (G-Score, ΔG) et la véracité factuelle jugée par un tiers indépendant est calculée. La question posée est : l'instrument NeoMundi détecte-t-il, par la seule signature thermodynamique et sans lecture sémantique, une dérive corrélée à l'hallucination factuelle ?

Le second exercice établit la cartographie. Les distributions de G-Score, ΔG et taux de flag des cinq services mesurés sont présentées côte à côte sur le même corpus. Cette carte est la première publication publique de NeoMundi sur le paysage génératif.

## Services mesurés en v1.0

Les cinq services sont anonymisés par défaut. Chaque service est identifié par un identifiant anonyme stable (P-001 à P-005). Les noms réels des providers ne sont pas divulgués.

## Notations — v1-2026-04-26

Les premières notes runtime jamais publiées. Calculées de manière déterministe à partir de `measurements.csv` avec `methodology.py` (Méthodologie v1.0, Public Draft).

| Provider | Observations | G-Score | Taux FLAG | Composite | Note    | Tier                | Tendance |
|----------|-------------:|--------:|----------:|----------:|---------|---------------------|----------|
| P-002    |          780 |  0,9120 |   3,72 %  |    0,9374 | ![A](https://img.shields.io/badge/A-6F9E85?style=flat)   | Production grade    | n/a      |
| P-001    |          780 |  0,9091 |   7,69 %  |    0,9161 | ![BBB](https://img.shields.io/badge/BBB-75BC5B?style=flat) | Production grade    | n/a      |
| P-004    |          781 |  0,9077 |   8,96 %  |    0,9090 | ![BBB](https://img.shields.io/badge/BBB-75BC5B?style=flat) | Production grade    | n/a      |
| P-003    |          782 |  0,8998 |  14,19 %  |    0,8789 | ![BB](https://img.shields.io/badge/BB-8EB848?style=flat)  | Governance-required | n/a      |
| P-005    |          782 |  0,8886 |  21,48 %  |    0,8369 | ![B](https://img.shields.io/badge/B-CE842D?style=flat)   | Governance-required | n/a      |

> **Conclusion principale.** *Aucun LLM observé n'atteint AA sans gouvernance runtime.*

La couleur de chaque note suit la convention colorimétrique fixée dans la méthodologie ([§6](./Methodologie_FR.md#6-convention-colorimétrique)) : un chemin perceptuellement uniforme dans l'espace CIE Lab 1976 dont l'inflection chaud → froid tombe par construction à la frontière de tier (BB → BBB). Lire le tableau ne nécessite aucune légende : les notes froides sont *Production grade*, les notes chaudes sont *Governance-required*.

La tendance est `n/a` pour ce jeu de données car il s'agit d'une mesure synchrone, pas d'un flux runtime continu. La tendance (Stable / Positive / Négative) sera renseignée dès que l'instrument tournera sur du trafic de production sur une fenêtre suffisante.

**Reproduire ces notes :**
```bash
python methodology.py        # lance les tests de référence sur le jeu de données
```

Les deux dimensions brutes (G-Score, taux de FLAG) et la note agglomérée sont toutes affichées. Le composite est recalculable à partir des deux dimensions, et la note à partir du composite via le tableau des seuils de [`Methodologie_FR.md`](./Methodologie_FR.md) §4.2.

- *Correct answers : proportion validée par LLM-as-judge (GPT-4o).*
- *Précision NeoMundi : fiabilité des flags (proportion de FLAG correctement positionnés sur des réponses incorrectes).*
- *Recall : proportion d'erreurs effectivement détectées par NeoMundi.*
- *Observability (ΔG) : signal de dérive thermodynamique mesuré.*

[Statistiques agrégées →](./data/v1-2026-04-26/summary.csv) · [Provenance et DOI →](./data/v1-2026-04-26/PROVENANCE.txt)

Les cinq services ont été mesurés dans la même fenêtre temporelle, sur le corpus TruthfulQA, avec le même juge tiers (GPT-4o) et la même instrumentation.

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
        └── summary.csv          ← statistiques agrégées par provider anonyme
```

## Posture

NeoMundi mesure, atteste, transmet. La gouvernance reste la responsabilité de celui qui opère le service. La cartographie est partielle par construction et provisoire par honnêteté — elle couvre un ensemble fini de services à un instant daté, et l'instrument progresse par paliers versionnés.

NeoMundi Recherche, association loi 1901, est hébergée à Vannes, France. Elle publie la cartographie et ne vend rien. Les activités commerciales dérivées sont portées par une entité juridique distincte (Louis M Sàrl, Morges, Suisse) qui n'intervient qu'auprès des utilisateurs de services génératifs, et jamais auprès des providers mesurés.

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
