# Usage guide — neomundi-methodology

> *How to re-run the complete scoring pipeline from scratch, locally.*
> Audience: any researcher, engineer, or reviewer wishing to reproduce the pipeline.
> Version: v1.0 (revision 2026-04-27)

---

## 0. Pipeline overview

```
[private raw files]                                 [public, in the repo]
P-XXX_truthfulqa_<provider>_judged.csv  ──┐
                                           ├──►  anonymize_release.py  ──►  public/measurements.csv
truthfulqa_ground_truth.csv                │                                public/summary.csv
                                           │
                                           └──►  judge_truthfulqa.py    (optional calibration, OpenAI API)
                                                       │
                                                       ▼
                                                truthfulqa_benchmark_metrics.json

public/measurements.csv  ──►  score.py  ──►  methodology.py  ──►  ratings.csv
```

Three roles, three independent scripts:

- **`anonymize_release.py`** — transforms raw CSVs (with provider names in clear, prompts, responses) into anonymized and hashed publishable CSVs.
- **`judge_truthfulqa.py`** — uses GPT-4o to judge each LLM response `CORRECT`/`INCORRECT` against TruthfulQA, and computes TP/FP/TN/FN to calibrate the FLAG mechanism. **Optional** — only when recalibrating.
- **`score.py`** — aggregates `public/measurements.csv` per provider and applies the methodology (`methodology.py`) to produce `ratings.csv`.

---

## 1. Prerequisites

- **Python 3.11 or later** (check with `python --version`)
- **Git** (for cloning and committing)
- **An OpenAI API key** (only for `judge_truthfulqa.py`; not needed for `score.py`)

---

## 2. Initial setup (one-time)

### 2.1 Clone the repo

```bash
git clone https://github.com/Neomundi-Labs/<repo-name>.git
cd <repo-name>
```

### 2.2 Create a Python virtual environment

**Mac / Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows PowerShell:**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> If PowerShell rejects with an "execution policy" error, run first:
> `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`

### 2.3 Install dependencies

```bash
pip install pandas numpy openai python-dotenv
```

### 2.4 Configure the OpenAI API key

Create a `.env` file at the project root (NEVER commit it):

```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Make sure `.env` is in `.gitignore`:

```bash
echo ".env" >> .gitignore
```

### 2.5 Verify the installation

```bash
python methodology.py
```

Should display the table of the 5 reference providers and `All self-tests passed.` at the end. If KO, do not continue.

---

## 3. Standard scoring workflow

To run for each new wave of measurements.

### 3.1 Prepare raw files

Place the raw CSVs produced by the runtime pipeline in the `raw/` folder at the root. Naming convention:

```
raw/P-001_truthfulqa_openai_judged.csv
raw/P-002_truthfulqa_anthropic_judged.csv
raw/P-003_truthfulqa_mistral_judged.csv
...
```

### 3.2 Update the provider mapping

Open `anonymize_release.py` and update the `PROVIDER_MAPPING` list:

```python
PROVIDER_MAPPING = [
    ("P-001_truthfulqa_openai_judged.csv", "P-001"),
    ("P-002_truthfulqa_anthropic_judged.csv", "P-002"),
    # ... add / remove according to the cohort
]
```

> The `P-XXX → commercial name` mapping stays **only in this local file**, never in the public repo.

### 3.3 Anonymize

```bash
python anonymize_release.py
```

Result: `public/measurements.csv` and `public/summary.csv` (anonymized, hashed, ready to commit).

### 3.4 Score

```bash
python score.py
```

Result: `ratings.csv` at the root, with one row per provider, sorted by descending composite.

Expected output (example):

```
P-002    G̅=0.9120  FLAG= 3.72%  composite=0.9374  →  A    (Production grade)  #6F9E85
P-001    G̅=0.9091  FLAG= 7.69%  composite=0.9161  →  BBB  (Production grade)  #75BC5B
P-004    G̅=0.9077  FLAG= 8.96%  composite=0.9090  →  BBB  (Production grade)  #75BC5B
P-003    G̅=0.8998  FLAG=14.19%  composite=0.8790  →  BB   (Governance-required)  #8EB848
P-005    G̅=0.8886  FLAG=21.48%  composite=0.8369  →  B    (Governance-required)  #CE842D
```

### 3.5 Verify consistency

```bash
python methodology.py
```

If the self-tests fail or `ratings.csv` does not reproduce the expected dataset, **do not commit**. Investigate.

### 3.6 Commit

```bash
git add public/measurements.csv public/summary.csv ratings.csv
git commit -m "Cohort wave <N> — <date> — <short description>"
git push origin main
```

---

## 4. Calibration workflow (LLM judge)

To run **only** when recalibrating the FLAG mechanism against TruthfulQA, or when changing the LLM judge.

### 4.1 Specific prerequisites

- `truthfulqa_ground_truth.csv` at the root
- Raw CSVs per provider in the format `truthfulqa_<provider>_dg_results.csv`
- `OPENAI_API_KEY` environment variable defined (cf. §2.4)
- Sufficient OpenAI credits (~5-10 USD for 5 providers × 800 questions)

### 4.2 Run

```bash
python judge_truthfulqa.py
```

Duration: ~20-40 minutes depending on the OpenAI rate limit. The script displays progress every 50 questions.

### 4.3 Output

- One enriched CSV per provider: `truthfulqa_<provider>_judged.csv`
- An aggregated metrics file: `truthfulqa_benchmark_metrics.json`

These metrics (TP/FP/TN/FN, precision, recall, F1) should be included in the reporting (cf. METHODOLOGY §10).

---

## 5. Regenerate CHECKSUMS.sha256

To run after any change to versioned `.py` or `.md` files.

**Mac / Linux:**
```bash
shasum -a 256 *.py *.md > CHECKSUMS.sha256
```

**Windows PowerShell:**
```powershell
Get-FileHash -Algorithm SHA256 *.py, *.md | ForEach-Object { "$($_.Hash.ToLower())  $($_.Path | Split-Path -Leaf)" } > CHECKSUMS.sha256
```

Verify the content:
```bash
cat CHECKSUMS.sha256
```

Then commit:
```bash
git add CHECKSUMS.sha256
git commit -m "Update CHECKSUMS.sha256"
git push origin main
```

---

## 6. Git tag for a release

After a stabilized methodological revision:

```bash
git tag -a v1.0-methodology -m "Methodology v1.0 (Public Draft, revision YYYY-MM-DD)"
git push origin v1.0-methodology
```

The tag is immutable. It fixes the exact state of the repo at a moment T for scientific traceability.

---

## 7. Troubleshooting

| Symptom | Likely cause | Solution |
|---|---|---|
| `OPENAI_API_KEY environment variable not set` | `.env` missing or variable not loaded | Verify `.env` exists at root, contains `OPENAI_API_KEY=...`, and that `python-dotenv` is installed |
| `ModuleNotFoundError: No module named 'pandas'` | venv not activated or packages not installed | Activate the venv (cf. §2.2), then `pip install pandas numpy` |
| `methodology.py` self-tests fail | Corrupted file or methodology modified locally | `git checkout methodology.py` to restore the repo version, then re-run |
| `ratings.csv` does not reproduce the expected dataset | Wrong `measurements.csv` or old version of `methodology.py` | Check the date of `methodology.py`, verify checksums with `shasum -c CHECKSUMS.sha256` |
| `Set-ExecutionPolicy` required on Windows | PowerShell execution policy too strict | `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned` |
| OpenAI judge rate-limits | Too many calls per minute | Increase `DELAY_S` in `judge_truthfulqa.py` (default 0.5s) |

---

## 8. File architecture (reference)

```
neomundi-methodology/
├── Methodologie_FR.md          # methodology spec (FR — source of truth)
├── Methodology_EN.md           # methodology spec (EN translation)
├── README.md                   # repo description (EN)
├── README_FR.md                # repo description (FR)
├── USAGE_FR.md                 # step-by-step usage guide (FR)
├── USAGE_EN.md                 # this document (EN)
├── License                     # license for code and data
├── CHECKSUMS.sha256            # integrity hashes for versioned files
│
├── methodology.py              # source of truth scoring (layers 2/3/4 + colorimetry)
├── score.py                    # runner: measurements.csv → ratings.csv
├── anonymize_release.py        # raw → publishable pipeline
├── judge_truthfulqa.py         # optional LLM judge calibration
│
├── data/
│   └── (historical datasets, immutable)
│
├── public/
│   ├── measurements.csv        # anonymized measurements (publishable)
│   └── summary.csv             # aggregated statistics (publishable)
│
├── ratings.csv                 # output of score.py
│
├── raw/                        # ⚠️ NEVER committed (gitignore)
│   └── P-XXX_..._judged.csv    # CSVs with commercial names in clear
│
├── .env                        # ⚠️ NEVER committed (gitignore)
└── .gitignore                  # must contain .env, raw/, venv/
```

---

*Usage guide v1.0 — NeoMundi Recherche · 2026-04-27*
