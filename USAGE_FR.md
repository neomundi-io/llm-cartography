# Mode d'emploi — neomundi-methodology

> *Comment relancer le pipeline complet de scoring depuis zéro, en local.*
> Audience : tout chercheur, ingénieur ou reviewer souhaitant reproduire le pipeline.
> Version : v1.0 (révision 2026-04-27)

---

## 0. Vue d'ensemble du pipeline

```
[fichiers raw privés]                               [public, dans le repo]
P-XXX_truthfulqa_<provider>_judged.csv  ──┐
                                           ├──►  anonymize_release.py  ──►  public/measurements.csv
truthfulqa_ground_truth.csv                │                                public/summary.csv
                                           │
                                           └──►  judge_truthfulqa.py    (calibration optionnelle, OpenAI API)
                                                       │
                                                       ▼
                                                truthfulqa_benchmark_metrics.json

public/measurements.csv  ──►  score.py  ──►  methodology.py  ──►  ratings.csv
```

Trois rôles, trois scripts indépendants :

- **`anonymize_release.py`** : transforme les CSV bruts (avec noms de providers en clair, prompts, réponses) en CSV publiables anonymisés et hashés.
- **`judge_truthfulqa.py`** : utilise GPT-4o pour juger chaque réponse LLM `CORRECT`/`INCORRECT` contre TruthfulQA, et calcule TP/FP/TN/FN pour calibrer le mécanisme FLAG. **Optionnel** — uniquement quand on veut recalibrer.
- **`score.py`** : agrège `public/measurements.csv` par provider et applique la méthodologie (`methodology.py`) pour produire `ratings.csv`.

---

## 1. Pré-requis

- **Python 3.11 ou plus récent** (tester avec `python --version`)
- **Git** (pour cloner et committer)
- **Une clé API OpenAI** (uniquement pour `judge_truthfulqa.py` ; pas nécessaire pour `score.py`)

---

## 2. Installation initiale (à faire une seule fois)

### 2.1 Cloner le repo

```bash
git clone https://github.com/Neomundi-Labs/<nom-du-repo>.git
cd <nom-du-repo>
```

### 2.2 Créer un environnement virtuel Python

**Mac / Linux :**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows PowerShell :**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> Si PowerShell refuse avec une erreur "execution policy", lance d'abord :
> `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`

### 2.3 Installer les dépendances

```bash
pip install pandas numpy openai python-dotenv
```

### 2.4 Configurer la clé API OpenAI

Créer un fichier `.env` à la racine du projet (ne JAMAIS le committer) :

```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Vérifier que `.env` est bien dans `.gitignore` :

```bash
echo ".env" >> .gitignore
```

### 2.5 Vérifier l'installation

```bash
python methodology.py
```

Doit afficher le tableau des 5 providers de référence et `All self-tests passed.` à la fin. Si KO, ne pas continuer.

---

## 3. Workflow standard de scoring

À faire à chaque nouvelle vague de mesures.

### 3.1 Préparer les fichiers raw

Placer les CSV bruts produits par le pipeline runtime dans le dossier `raw/` à la racine. Convention de nommage :

```
raw/P-001_truthfulqa_openai_judged.csv
raw/P-002_truthfulqa_anthropic_judged.csv
raw/P-003_truthfulqa_mistral_judged.csv
...
```

### 3.2 Mettre à jour le mapping provider

Ouvrir `anonymize_release.py` et mettre à jour la liste `PROVIDER_MAPPING` :

```python
PROVIDER_MAPPING = [
    ("P-001_truthfulqa_openai_judged.csv", "P-001"),
    ("P-002_truthfulqa_anthropic_judged.csv", "P-002"),
    # ... ajouter / retirer selon la cohorte
]
```

> Le mapping `P-XXX → nom commercial` reste **uniquement dans ce fichier local**, jamais dans le repo public.

### 3.3 Anonymiser

```bash
python anonymize_release.py
```

Résultat : `public/measurements.csv` et `public/summary.csv` (anonymisés, hashés, prêts à committer).

### 3.4 Scorer

```bash
python score.py
```

Résultat : `ratings.csv` à la racine, avec une ligne par provider, classés par composite décroissant.

Affichage attendu (exemple) :

```
P-002    G̅=0.9120  FLAG= 3.72%  composite=0.9374  →  A    (Production grade)  #6F9E85
P-001    G̅=0.9091  FLAG= 7.69%  composite=0.9161  →  BBB  (Production grade)  #75BC5B
P-004    G̅=0.9077  FLAG= 8.96%  composite=0.9090  →  BBB  (Production grade)  #75BC5B
P-003    G̅=0.8998  FLAG=14.19%  composite=0.8790  →  BB   (Governance-required)  #8EB848
P-005    G̅=0.8886  FLAG=21.48%  composite=0.8369  →  B    (Governance-required)  #CE842D
```

### 3.5 Vérifier la cohérence

```bash
python methodology.py
```

Si les self-tests échouent ou si `ratings.csv` ne reproduit pas le dataset attendu, **ne pas committer**. Investiguer.

### 3.6 Committer

```bash
git add public/measurements.csv public/summary.csv ratings.csv
git commit -m "Cohort vague <N> — <date> — <description courte>"
git push origin main
```

---

## 4. Workflow de calibration (juge LLM)

À faire **uniquement** quand on veut recalibrer le mécanisme FLAG contre TruthfulQA, ou quand on change de juge LLM.

### 4.1 Pré-requis spécifiques

- `truthfulqa_ground_truth.csv` à la racine
- CSV bruts par provider au format `truthfulqa_<provider>_dg_results.csv`
- Variable d'environnement `OPENAI_API_KEY` définie (cf. §2.4)
- Crédits OpenAI suffisants (~5-10 USD pour 5 providers × 800 questions)

### 4.2 Lancer

```bash
python judge_truthfulqa.py
```

Durée : ~20-40 minutes selon le rate limit OpenAI. Le script affiche la progression toutes les 50 questions.

### 4.3 Résultat

- Un CSV enrichi par provider : `truthfulqa_<provider>_judged.csv`
- Un fichier de métriques agrégées : `truthfulqa_benchmark_metrics.json`

Ces métriques (TP/FP/TN/FN, précision, rappel, F1) sont à inclure dans le reporting (cf. METHODOLOGY §10).

---

## 5. Régénérer CHECKSUMS.sha256

À faire après tout changement aux fichiers `.py` ou `.md` versionnés.

**Mac / Linux :**
```bash
shasum -a 256 *.py *.md > CHECKSUMS.sha256
```

**Windows PowerShell :**
```powershell
Get-FileHash -Algorithm SHA256 *.py, *.md | ForEach-Object { "$($_.Hash.ToLower())  $($_.Path | Split-Path -Leaf)" } > CHECKSUMS.sha256
```

Vérifier le contenu :
```bash
cat CHECKSUMS.sha256
```

Puis committer :
```bash
git add CHECKSUMS.sha256
git commit -m "Update CHECKSUMS.sha256"
git push origin main
```

---

## 6. Tag git d'une release

Après une révision méthodologique stabilisée :

```bash
git tag -a v1.0-methodology -m "Methodology v1.0 (Public Draft, révision YYYY-MM-DD)"
git push origin v1.0-methodology
```

Le tag est immuable. Il fixe l'état exact du repo à un instant T pour la traçabilité scientifique.

---

## 7. Troubleshooting

| Symptôme | Cause probable | Solution |
|---|---|---|
| `OPENAI_API_KEY environment variable not set` | `.env` absent ou variable non chargée | Vérifier que `.env` existe à la racine, contient `OPENAI_API_KEY=...`, et que `python-dotenv` est installé |
| `ModuleNotFoundError: No module named 'pandas'` | venv non activé ou packages non installés | Activer le venv (cf. §2.2), puis `pip install pandas numpy` |
| `methodology.py` self-tests échouent | Fichier corrompu ou méthodologie modifiée localement | `git checkout methodology.py` pour restaurer la version repo, puis relancer |
| `ratings.csv` ne reproduit pas le dataset attendu | Mauvais `measurements.csv` ou ancienne version de `methodology.py` | Vérifier la date de `methodology.py`, vérifier les checksums avec `shasum -c CHECKSUMS.sha256` |
| `Set-ExecutionPolicy` requise sur Windows | Politique d'exécution PowerShell trop stricte | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` |
| Le juge OpenAI rate-limite | Trop d'appels par minute | Augmenter `DELAY_S` dans `judge_truthfulqa.py` (par défaut 0.5s) |

---

## 8. Architecture des fichiers (référence)

```
neomundi-methodology/
├── METHODOLOGY.md              # spec FR (source de vérité méthodologique)
├── Methodology_EN.md           # spec EN (équivalent)
├── README.md                   # description du repo (EN)
├── README_FR.md                # description du repo (FR)
├── USAGE_FR.md                 # ce document
├── License                     # licence du code et des données
├── CHECKSUMS.sha256            # empreintes des fichiers versionnés
│
├── methodology.py              # source de vérité scoring (couches 2/3/4 + colorimétrie)
├── score.py                    # runner : measurements.csv → ratings.csv
├── anonymize_release.py        # pipeline raw → publiable
├── judge_truthfulqa.py         # calibration LLM (optionnel)
│
├── data/
│   └── (datasets historiques, immuables)
│
├── public/
│   ├── measurements.csv        # mesures anonymisées (publiable)
│   └── summary.csv             # statistiques agrégées (publiable)
│
├── ratings.csv                 # sortie de score.py
│
├── raw/                        # ⚠️ JAMAIS commité (gitignore)
│   └── P-XXX_..._judged.csv    # CSV avec noms commerciaux en clair
│
├── .env                        # ⚠️ JAMAIS commité (gitignore)
└── .gitignore                  # doit contenir .env, raw/, venv/
```

---

*Mode d'emploi v1.0 — NeoMundi Recherche · 2026-04-27*
