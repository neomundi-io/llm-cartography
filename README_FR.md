[![EN](https://img.shields.io/badge/lang-English-lightgrey)](./README.md) · ![FR](https://img.shields.io/badge/lang-Français-blue)

---

# Cartographie thermodynamique des services génératifs

### *Neomundi Recherche — version 1.0*

---

Ce dépôt publie la première cartographie thermodynamique publique des services génératifs accessibles par API commerciale.

Neomundi ne mesure pas le modèle. Neomundi mesure le service. L'unité de mesure est le triplet **Modèle × Stack × Temps** — le service tel qu'il répond réellement, à une fenêtre datée, sur une infrastructure donnée. La mesure porte sur la sortie du service, token par token, sans lecture sémantique du contenu.

## Ce que contient ce dépôt

Le dépôt rassemble deux exercices distincts, construits sur le même corpus et la même instrumentation.

Le premier exercice évalue l'instrument. Pour chaque service mesuré, la corrélation entre la signature thermodynamique (G-Score, ΔG) et la véracité factuelle jugée par un tiers indépendant est calculée. La question posée est : l'instrument Neomundi détecte-t-il, par la seule signature thermodynamique et sans lecture sémantique, une dérive corrélée à l'hallucination factuelle ?

Le second exercice établit la cartographie. Les distributions de G-Score, ΔG et taux de flag des cinq services mesurés sont présentées côte à côte sur le même corpus. Cette carte est la première publication publique de Neomundi sur le paysage génératif.

## Services mesurés en v1.0

Les cinq services sont anonymisés par défaut. Chaque service est identifié par un identifiant anonyme stable (P-001 à P-005) et une région géographique large. Les noms réels des providers ne sont pas divulgués dans cette version.

## Mesures publiées — synthèse v1.0

## Published measurements — v1.0 summary

## Notations — v1-2026-04-26

Les premières notes ControlTower™ jamais publiées. Calculées de manière
déterministe à partir de `measurements.csv` avec `methodology.py`
(Méthodologie v1.0, Public Draft).

| Provider | Observations | G-Score | Taux FLAG | Composite | Note    | Tier               | Outlook |
|----------|-------------:|--------:|----------:|----------:|---------|--------------------|---------|
| P-002    |          780 |  0,9120 |   3,72 %  |    0,9374 | **A**   | Investment grade   | n/a     |
| P-001    |          780 |  0,9091 |   7,69 %  |    0,9161 | **BBB** | Investment grade   | n/a     |
| P-004    |          781 |  0,9077 |   8,96 %  |    0,9090 | **BBB** | Investment grade   | n/a     |
| P-003    |          782 |  0,8998 |  14,19 %  |    0,8789 | **BB**  | Speculative grade  | n/a     |
| P-005    |          782 |  0,8886 |  21,48 %  |    0,8369 | **B**   | Speculative grade  | n/a     |

> **Conclusion principale.** *Aucun LLM observé n'atteint AA sans gouvernance runtime.*

L'outlook est `n/a` pour ce jeu de données car il s'agit d'une mesure
synchrone, pas d'un flux runtime continu. L'outlook (Stable / Positive /
Negative) sera renseigné dès que ControlTower™ tournera sur du trafic
de production.

**Reproduire ces notes :**
```bash
python methodology.py        # lance les tests de référence sur le jeu de données
```

Les deux dimensions brutes (G-Score, taux de FLAG) et la note agglomérée
sont toutes affichées. Le composite est recalculable à partir des deux
dimensions, et la note à partir du composite via le tableau des seuils
de [`Methodologie_FR.md`](./Methodologie_FR.md) §4.2.

- *Correct answers : proportion validée par LLM-as-judge (GPT-4o). 
- Neomundi precision : fiabilité des flags Neomundi (proportion de FLAG correctement positionnés sur des réponses incorrectes). 
- Recall : proportion d'erreurs effectivement détectées par Neomundi. 
- Observability (ΔG) : signal de dérive thermodynamique mesuré.*

[Mesures brutes complètes →](./data/v1-23-04-26) · [Statistiques agrégées →](./data/summary-v1)

Les cinq services ont été mesurés dans la même fenêtre temporelle, sur le corpus TruthfulQA, avec le même juge tiers (GPT-4o) et la même instrumentation.

## Anonymisation

L'anonymisation est la position par défaut de la cartographie v1.0. Elle exprime trois engagements.

D'abord, l'égalité de traitement : tous les services mesurés sont identifiés de la même manière, indépendamment de leur poids commercial, de leur origine géographique, ou de leur relation avec Neomundi.

Ensuite, l'irrévocabilité de la protection : un identifiant anonyme ne peut être levé par Neomundi de manière unilatérale. Seule une demande explicite et écrite d'un provider mesuré peut conduire à un nommage public, dans une version ultérieure de la cartographie.

Enfin, la neutralité scientifique : l'instrument est évalué sur le fond des mesures, pas sur la réputation des noms. Un lecteur de la cartographie compare des signatures, pas des marques.

La procédure de levée d'anonymat, sur demande explicite d'un provider mesuré, est documentée dans `CONTEST.md`.

## Organisation du dépôt

```
.
├── README.md                    ← version anglaise
├── README_FR.md                 ← ce fichier
├── METHODOLOGY_EN.md            ← méthodologie détaillée (anglais)
├── METHODOLOGY_FR.md            ← méthodologie détaillée (français)
├── CONTEST.md                   ← procédure de contestation et de nommage
├── CITATION.cff                 ← format de citation
├── LICENSE                      ← Creative Commons Attribution 4.0
└── data/
    └── v1.0/
        ├── measurements.csv     ← mesures brutes par provider anonyme
        └── providers.csv        ← métadonnées des providers anonymes
```

## Posture

Neomundi mesure, atteste, transmet. La gouvernance reste la responsabilité de celui qui opère le service. La cartographie est partielle par construction et provisoire par honnêteté — elle couvre un ensemble fini de providers à un instant daté, et l'instrument progresse par paliers versionnés.

Tout service mesuré peut demander à être nommé publiquement, ou à être retiré de la cartographie publique, à tout moment. Les deux procédures sont documentées dans `CONTEST.md`.

Neomundi Recherche, association loi 1901, est hébergée à Vannes, France. Elle publie la cartographie et ne vend rien. Les activités commerciales dérivées sont portées par une entité juridique distincte (Louis M Sàrl, Morges, Suisse) qui n'intervient qu'auprès des acheteurs de services, et jamais auprès des providers mesurés.

## Comment citer

Le format de citation recommandé est fourni dans le fichier `CITATION.cff`. Le DOI Zenodo de la v1.0 sera ajouté à ce README dès sa publication.

## Pour aller plus loin

La méthodologie complète — objet de mesure, instrumentation, protocole, corpus, limites, versioning, échelle prévue — est décrite dans [METHODOLOGY_FR.md](./Methodologie_FR).

Le cadre théorique Law E sur lequel repose l'instrumentation est déposé séparément sur Zenodo, DOI 10.5281/zenodo.19385052.

## Licence

Creative Commons Attribution 4.0 International (CC-BY-4.0). Libre réutilisation avec attribution à Neomundi Recherche.

## Contact

`recherche@neomundi.org`

---

*La carte est partielle. L'instrument progresse. La méthodologie est publique.*

