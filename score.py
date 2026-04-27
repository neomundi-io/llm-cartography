"""
score.py — Compute notation runtime ratings from a measurements.csv file.

Usage:
    python score.py

Place this file in the same folder as:
    - methodology.py        (frozen reference v1.0)
    - measurements.csv      (raw output from the runtime measurement pipeline)

Generates:
    - ratings.csv           (provider-level ratings)
    - prints summary table to console
"""

import pandas as pd
from methodology import rate, METHODOLOGY_VERSION, METHODOLOGY_STATUS


def main():
    # --- 1. Load raw measurements
    df = pd.read_csv("measurements.csv")
    print(f"Loaded {len(df)} rows from measurements.csv")
    print(f"Methodology v{METHODOLOGY_VERSION} ({METHODOLOGY_STATUS})\n")

    # --- 2. Aggregate per provider (Layer 1 outputs → Layer 2 inputs)
    agg = df.groupby("provider_id").agg(
        n_observations=("question_id", "count"),
        g_mean=("g_score", "mean"),
        flag_rate=("decision", lambda x: (x == "FLAG").mean()),
    ).reset_index()

    # --- 3. Apply pipeline (Layers 2 → 3 → 4)
    rows = []
    for _, row in agg.iterrows():
        r = rate(row["g_mean"], row["flag_rate"])
        rows.append({
            "provider_id": row["provider_id"],
            "n_observations": int(row["n_observations"]),
            "g_score_mean": round(row["g_mean"], 4),
            "flag_rate": round(row["flag_rate"], 4),
            "composite": round(r.composite, 4),
            "rating": r.grade,
            "tier": r.tier,
            "trend": "n/a",  # static dataset; runtime stream needed for live trend
            "color": r.color(),
            "trend_color": r.trend_color(),
            "methodology_version": f"v{r.methodology_version}",
        })

    # --- 4. Sort by composite (best → worst) and persist
    ratings = pd.DataFrame(rows).sort_values("composite", ascending=False)
    ratings.to_csv("ratings.csv", index=False)

    # --- 5. Print summary
    print("Notation runtime — results")
    print("=" * 100)
    for _, r in ratings.iterrows():
        print(f"  {r['provider_id']:<8}  G̅={r['g_score_mean']:.4f}  "
              f"FLAG={r['flag_rate']*100:>5.2f}%  "
              f"composite={r['composite']:.4f}  →  "
              f"{r['rating']:<4} ({r['tier']})  {r['color']}")
    print("=" * 100)
    print(f"\nWritten: ratings.csv")


if __name__ == "__main__":
    main()
