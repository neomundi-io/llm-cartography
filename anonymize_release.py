#!/usr/bin/env python3
"""
NeoMundi — Anonymization pipeline for cartography releases.

Transforms raw per-provider measurement CSVs (with provider names, prompts,
and responses in clear) into anonymized public/measurements.csv and
public/summary.csv for commit to the public repository.

==============================================================================
PRIVACY POSTURE
==============================================================================

The methodology (METHODOLOGY.md §7.3) commits to "fully and durably
anonymous" cartography: the P-XXX → commercial name mapping is never
published.

This script enforces that commitment at the publication layer:
  - The mapping is read from `provider_mapping.local.json` at runtime.
  - That file MUST be in .gitignore and never enters the public repo.
  - If the file is missing, the script refuses to run with clear
    instructions for setup.

The public version of this script in the repository contains only the
schema and the loader. It cannot leak provider identities by design.
==============================================================================

Local setup (once per release):

    Create `provider_mapping.local.json` at the repo root, with format:

    [
      {"raw_filename": "P-001_truthfulqa_<provider>_judged.csv", "pseudonym": "P-001"},
      {"raw_filename": "P-002_truthfulqa_<provider>_judged.csv", "pseudonym": "P-002"}
    ]

    Then verify it is in .gitignore:
        grep -q "provider_mapping.local.json" .gitignore || \\
            echo "provider_mapping.local.json" >> .gitignore

Usage:
    python anonymize_release.py

Inputs:
    raw/<raw_filename>.csv     (one per provider, listed in the local config)

Outputs:
    public/measurements.csv    (anonymized, hashed, publishable)
    public/summary.csv         (aggregated statistics, publishable)

Author: NeoMundi Recherche
License: MIT (this script). Generated data is CC-BY-4.0.
"""

import hashlib
import json
import os
import sys
from pathlib import Path

import pandas as pd

# =============================================================================
# CONFIGURATION
# =============================================================================

INPUT_DIR = "raw"
OUTPUT_DIR = "public"
CONFIG_PATH = Path("provider_mapping.local.json")

# Columns kept in the public measurements.csv — anything else is dropped
PUBLIC_COLUMNS = [
    "provider_id",
    "question_id",
    "decision",
    "g_score",
    "regime",
    "dg_profile",
    "dg_flagged",
    "dg_variation",
    "judge_verdict",
    "is_correct",
    "response_hash",
    "cost_usd",
]


# =============================================================================
# CONFIG LOADER
# =============================================================================

def load_provider_mapping():
    """
    Load the P-XXX mapping from the local (gitignored) config file.
    Refuses to run if the file is missing or malformed.
    """
    if not CONFIG_PATH.exists():
        sys.stderr.write(
            f"\nERROR: {CONFIG_PATH} not found.\n\n"
            f"The provider mapping must be configured locally. The mapping is\n"
            f"NEVER committed to the public repository (cf. METHODOLOGY.md §7.3).\n\n"
            f"Create {CONFIG_PATH} with this structure:\n\n"
            f"  [\n"
            f'    {{"raw_filename": "P-001_<corpus>_<provider>_judged.csv", "pseudonym": "P-001"}},\n'
            f'    {{"raw_filename": "P-002_<corpus>_<provider>_judged.csv", "pseudonym": "P-002"}}\n'
            f"  ]\n\n"
            f"Then verify the file is in .gitignore:\n"
            f"  echo 'provider_mapping.local.json' >> .gitignore\n\n"
        )
        sys.exit(1)

    try:
        entries = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        sys.stderr.write(f"\nERROR: {CONFIG_PATH} is not valid JSON: {e}\n\n")
        sys.exit(1)

    if not isinstance(entries, list) or not entries:
        sys.stderr.write(
            f"\nERROR: {CONFIG_PATH} must be a non-empty JSON array.\n\n"
        )
        sys.exit(1)

    mapping = []
    for i, entry in enumerate(entries):
        if not isinstance(entry, dict) or "raw_filename" not in entry or "pseudonym" not in entry:
            sys.stderr.write(
                f"\nERROR: {CONFIG_PATH} entry {i} is malformed.\n"
                f"Each entry must have 'raw_filename' and 'pseudonym' fields.\n\n"
            )
            sys.exit(1)
        mapping.append((entry["raw_filename"], entry["pseudonym"]))

    return mapping


# =============================================================================
# TRANSFORMATION FUNCTIONS
# =============================================================================

def normalize_decimal(value):
    """Convert French decimal notation (comma) to standard (point)."""
    if pd.isna(value):
        return value
    if isinstance(value, str):
        return float(value.replace(",", "."))
    return float(value)


def hash_response(text):
    """SHA-256 hash of the response text (truncated to 16 chars for readability)."""
    if pd.isna(text):
        return None
    full_hash = hashlib.sha256(str(text).encode("utf-8")).hexdigest()
    return f"sha256:{full_hash[:16]}"


def format_question_id(qid):
    """Normalize question identifier to TQ-NNNN format."""
    if isinstance(qid, str) and qid.startswith("q_"):
        num = qid.replace("q_", "")
        return f"TQ-{num.zfill(4)}"
    return qid


# =============================================================================
# MAIN PIPELINE
# =============================================================================

def main():
    Path(OUTPUT_DIR).mkdir(exist_ok=True)

    provider_mapping = load_provider_mapping()
    print(f"Loaded mapping for {len(provider_mapping)} providers from {CONFIG_PATH}")

    # 1. Load and concatenate all raw provider CSVs
    print(f"Loading raw files from {INPUT_DIR}/")
    dfs = []
    for filename, provider_id in provider_mapping:
        path = os.path.join(INPUT_DIR, filename)
        if not os.path.exists(path):
            sys.stderr.write(f"\nERROR: raw file not found: {path}\n\n")
            sys.exit(1)
        df = pd.read_csv(path)
        df["provider_id"] = provider_id
        dfs.append(df)
        print(f"  {filename} → {provider_id} ({len(df)} rows)")

    combined = pd.concat(dfs, ignore_index=True)
    print(f"Total measurements: {len(combined)}")

    # 2. Apply transformations (hashing, decimal normalization, ID formatting)
    print("Applying transformations...")
    combined["response_hash"] = combined["response"].apply(hash_response)
    combined["cost_usd"] = combined["cost"].apply(normalize_decimal)
    combined["g_score"] = combined["g_score"].apply(normalize_decimal)
    combined["dg_variation"] = combined["dg_variation"].apply(normalize_decimal)
    combined["question_id"] = combined["question_id"].apply(format_question_id)

    # 3. Keep only public columns, sorted for readability
    public_df = combined[PUBLIC_COLUMNS].copy()
    public_df = public_df.sort_values(["provider_id", "question_id"]).reset_index(drop=True)

    # 4. Export measurements.csv
    measurements_path = os.path.join(OUTPUT_DIR, "measurements.csv")
    public_df.to_csv(measurements_path, index=False, float_format="%.6f")
    print(f"Wrote {measurements_path} ({len(public_df)} rows)")

    # 5. Compute and export summary.csv
    print("Computing aggregated statistics...")
    summary_rows = []
    for provider_id in sorted(public_df["provider_id"].unique()):
        sub = public_df[public_df["provider_id"] == provider_id]
        n = len(sub)

        correct = sub["is_correct"].sum()
        incorrect = (~sub["is_correct"]).sum()
        flag_count = (sub["decision"] == "FLAG").sum()
        flag_correct_on_incorrect = (
            (sub["decision"] == "FLAG") & (~sub["is_correct"])
        ).sum()

        summary_rows.append({
            "provider_id": provider_id,
            "n_measurements": n,
            "correct_answers_rate": round(correct / n, 4),
            "neomundi_precision": round(
                flag_correct_on_incorrect / flag_count if flag_count > 0 else 0, 4
            ),
            "neomundi_recall": round(
                flag_correct_on_incorrect / incorrect if incorrect > 0 else 0, 4
            ),
            "flag_rate": round(flag_count / n, 4),
            "g_score_mean": round(sub["g_score"].mean(), 4),
            "dg_variation_mean": round(sub["dg_variation"].mean(), 4),
            "cost_per_request_usd": round(sub["cost_usd"].mean(), 6),
        })

    summary_df = pd.DataFrame(summary_rows)
    summary_path = os.path.join(OUTPUT_DIR, "summary.csv")
    summary_df.to_csv(summary_path, index=False)
    print(f"Wrote {summary_path} ({len(summary_df)} rows)")

    print("\nSummary preview:")
    print(summary_df.to_string(index=False))
    print(f"\nDone. Files in {OUTPUT_DIR}/ are ready for publication.")


if __name__ == "__main__":
    main()
