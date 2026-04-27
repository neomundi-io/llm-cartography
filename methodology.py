"""
Notation runtime des LLM — Reference Implementation
=====================================================

Methodology version : 1.0 (Public Draft, révision 2026-04-27)
Specification       : METHODOLOGY.md
Reference dataset   : DOI 10.5281/zenodo.19762753

Architecture (four layers + colorimetric convention):
    Layer 1 — Measurement     (G-Score, FLAG events)         [upstream]
    Layer 2 — Aggregation     → composite score
    Layer 3 — Classification  → rating (AAA…CCC), tier, color
    Layer 4 — Trend           → Stable / Positive / Négative
    Convention colorimétrique → hex code per grade and trend

This module is the single source of truth for layers 2, 3, 4, and the
colorimetric convention. Layer 1 (raw runtime measurement) is provided by
the upstream governance pipeline.

Vocabulary (grade names AAA…CCC, tier names) is frozen permanently.
Weights, thresholds, and colors are versioned via METHODOLOGY_VERSION.
Any deployed scoring service must replicate these functions exactly.

Companion modules (each is its own source of truth, all tagged together):
    - score.py                : runner over public/measurements.csv
    - anonymize_release.py    : raw → public anonymization pipeline
    - judge_truthfulqa.py     : LLM-judge calibration (TruthfulQA ground truth)

We observe, we don't judge.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Sequence, Optional

# ---------------------------------------------------------------------------
# Frozen specification
# ---------------------------------------------------------------------------

METHODOLOGY_VERSION = "1.0"
METHODOLOGY_STATUS = "Public Draft (révision 2026-04-27)"

# --- Layer 2: Aggregation ---
# Composite weights — market convention v1.0, revisable in future versions.
# The 50/50 weighting ensures that continuous stability (G-Score) and
# discrete failure events (FLAG rate) have equal first-order impact on
# the composite. The two dimensions are structurally orthogonal.
W_G_SCORE = 0.5
W_FLAG_INVERSE = 0.5

# --- Layer 3: Classification ---
# Grade thresholds — non-uniform log distribution on operational range,
# with qualitative breakpoints at the tier boundary (BB → BBB) and
# asymptotic excellence ceiling (AAA → 1.00). See METHODOLOGY.md §4.1.
# Lower bound, inclusive.
GRADE_THRESHOLDS = (
    ("AAA", 0.981),
    ("AA",  0.947),
    ("A",   0.917),
    ("BBB", 0.883),
    ("BB",  0.864),
    ("B",   0.834),
    ("CCC", 0.000),  # everything below B
)

PRODUCTION_GRADE = frozenset({"AAA", "AA", "A", "BBB"})
GOVERNANCE_REQUIRED = frozenset({"BB", "B", "CCC"})

# --- Convention colorimétrique (See METHODOLOGY.md §6) ---
# Perceptually-anchored mapping from grade to hex color. Path in CIE Lab
# 1976 with three anchors (CCC, pivot at the BB→BBB tier boundary,
# asymptotic ceiling), linear interpolation, conversion
# Lab → XYZ (D65) → linear sRGB → sRGB. Values frozen for v1.0.
GRADE_COLORS_HEX = {
    "AAA": "#1966CB",  # deep blue — asymptotic excellence
    "AA":  "#5A82A9",  # medium blue
    "A":   "#6F9E85",  # teal
    "BBB": "#75BC5B",  # green — first Production grade
    "BB":  "#8EB848",  # yellow-green — last Governance-required
    "B":   "#CE842D",  # orange
    "CCC": "#F82117",  # saturated red — alarm
}

# --- Layer 4: Trend ---
# v1.0 empirical convention; v1.1 will move to a statistical control test
# (Welch / CUSUM).
TREND_DRIFT_THRESHOLD = 0.005
TREND_DEFAULT_WINDOW = 100

# Trend colors. Categorical (5 values), not on the perceptual scale of
# grades. `Positive` and `Négative` deliberately echo the grade colors
# for BBB and B, anchoring the visual meaning of the direction of drift.
# See METHODOLOGY.md §6.4.
TREND_COLORS_HEX = {
    "Stable":       "#999999",  # neutral gray, no movement
    "Positive":     "#75BC5B",  # green (echoes BBB), improvement
    "Négative":     "#CE842D",  # orange (echoes B), degradation
    "Sous revue":   "#E8B83E",  # amber, awaiting more data
    "n/a":          "#CCCCCC",  # pale gray, first measurement campaign
}


# ---------------------------------------------------------------------------
# Public types
# ---------------------------------------------------------------------------

class Trend(str, Enum):
    """Trend value (Layer 4). See METHODOLOGY.md §5 and §6.4."""
    STABLE = "Stable"
    POSITIVE = "Positive"
    NEGATIVE = "Négative"
    UNDER_REVIEW = "Sous revue"


@dataclass(frozen=True)
class Rating:
    g_mean: float
    flag_rate: float
    composite: float
    grade: str
    tier: str           # "Production grade" | "Governance-required"
    trend: Optional[Trend]
    methodology_version: str = METHODOLOGY_VERSION

    def color(self) -> str:
        """Canonical hex color for this rating's grade. See METHODOLOGY.md §6.3."""
        return GRADE_COLORS_HEX[self.grade]

    def trend_color(self) -> str:
        """Canonical hex color for this rating's trend. See METHODOLOGY.md §6.4."""
        if self.trend is None:
            return TREND_COLORS_HEX["n/a"]
        return TREND_COLORS_HEX[self.trend.value]

    def to_row(self) -> dict:
        """Reporting row matching the published standard (METHODOLOGY.md §10)."""
        return {
            "g_score": round(self.g_mean, 4),
            "flag_rate": round(self.flag_rate, 4),
            "composite": round(self.composite, 4),
            "rating": self.grade,
            "tier": self.tier,
            "trend": self.trend.value if self.trend else "n/a",
            "color": self.color(),
            "trend_color": self.trend_color(),
            "methodology": f"v{self.methodology_version}",
        }


# ---------------------------------------------------------------------------
# Layer 2: Aggregation
# ---------------------------------------------------------------------------

def composite_score(g_mean: float, flag_rate: float) -> float:
    """
    Aggregate the two raw runtime dimensions into a single composite.
    Convention v1.0: 0.5 × G̅ + 0.5 × (1 − FLAG_rate).
    """
    if not (0.0 <= g_mean <= 1.0):
        raise ValueError(f"g_mean must be in [0,1], got {g_mean}")
    if not (0.0 <= flag_rate <= 1.0):
        raise ValueError(f"flag_rate must be in [0,1], got {flag_rate}")
    return W_G_SCORE * g_mean + W_FLAG_INVERSE * (1.0 - flag_rate)


# ---------------------------------------------------------------------------
# Layer 3: Classification
# ---------------------------------------------------------------------------

def grade_from_composite(composite: float) -> str:
    """Map composite ∈ [0,1] to a grade in {AAA, AA, A, BBB, BB, B, CCC}."""
    for label, lower in GRADE_THRESHOLDS:
        if composite >= lower:
            return label
    return "CCC"  # unreachable; CCC threshold is 0.0


def tier_from_grade(grade: str) -> str:
    if grade in PRODUCTION_GRADE:
        return "Production grade"
    if grade in GOVERNANCE_REQUIRED:
        return "Governance-required"
    raise ValueError(f"Unknown grade: {grade}")


def color_from_grade(grade: str) -> str:
    """Return the canonical hex color for a grade. See METHODOLOGY.md §6.3."""
    return GRADE_COLORS_HEX[grade]


# ---------------------------------------------------------------------------
# Layer 4: Trend
# ---------------------------------------------------------------------------

def trend_from_history(
    composite_history: Sequence[float],
    window: int = TREND_DEFAULT_WINDOW,
) -> Trend:
    """
    Drift analysis over a rolling observation window.
    Compares mean of the most recent `window` completions to the mean
    of the previous `window` completions. v1.0 uses a fixed drift
    threshold; v1.1 will introduce a statistical control test.
    """
    if len(composite_history) < 2 * window:
        return Trend.UNDER_REVIEW

    recent = composite_history[-window:]
    prior = composite_history[-2 * window:-window]
    delta = (sum(recent) / window) - (sum(prior) / window)

    if abs(delta) < TREND_DRIFT_THRESHOLD:
        return Trend.STABLE
    if delta >= TREND_DRIFT_THRESHOLD:
        return Trend.POSITIVE
    return Trend.NEGATIVE


def color_from_trend(trend: Optional[Trend]) -> str:
    """Return the canonical hex color for a trend. See METHODOLOGY.md §6.4."""
    if trend is None:
        return TREND_COLORS_HEX["n/a"]
    return TREND_COLORS_HEX[trend.value]


# ---------------------------------------------------------------------------
# Unified entry point
# ---------------------------------------------------------------------------

def rate(
    g_mean: float,
    flag_rate: float,
    composite_history: Optional[Sequence[float]] = None,
) -> Rating:
    """
    Run the full pipeline (layers 2 → 3 → 4) on raw runtime measurements.

    Parameters
    ----------
    g_mean : float
        Mean G-Score over the observation window (Layer 1 output).
    flag_rate : float
        Share of FLAG decisions over the observation window (Layer 1 output).
    composite_history : sequence of floats, optional
        Rolling history of composite scores. Required for Layer 4 (Trend).
        If absent, Trend is None (rendered as "n/a" in reporting).
    """
    c = composite_score(g_mean, flag_rate)
    g = grade_from_composite(c)
    t = tier_from_grade(g)
    tr = trend_from_history(composite_history) if composite_history else None
    return Rating(
        g_mean=g_mean,
        flag_rate=flag_rate,
        composite=c,
        grade=g,
        tier=t,
        trend=tr,
    )


# ---------------------------------------------------------------------------
# Self-tests (run `python methodology.py` to verify)
# ---------------------------------------------------------------------------

def _self_test() -> None:
    # Reference dataset (v1-2026-04-26) — must reproduce exactly
    reference = [
        # (g_mean, flag_rate, expected_grade, expected_tier)
        (0.9091, 0.0769, "BBB", "Production grade"),    # P-001  composite ≈ 0.9161
        (0.9120, 0.0372, "A",   "Production grade"),    # P-002  composite ≈ 0.9374
        (0.8998, 0.1419, "BB",  "Governance-required"), # P-003  composite ≈ 0.8790
        (0.9077, 0.0896, "BBB", "Production grade"),    # P-004  composite ≈ 0.9091
        (0.8886, 0.2148, "B",   "Governance-required"), # P-005  composite ≈ 0.8369
    ]

    print(f"Notation runtime — methodology v{METHODOLOGY_VERSION} "
          f"({METHODOLOGY_STATUS})")
    print("-" * 88)
    print(f"{'g_score':<10}{'flag_rate':<12}{'composite':<12}"
          f"{'rating':<8}{'tier':<24}{'color':<10}")
    print("-" * 88)
    for g, f, exp_grade, exp_tier in reference:
        r = rate(g, f)
        flag_pct = f"{f*100:.2f}%"
        composite_fmt = f"{r.composite:.4f}"
        print(f"{g:<10}{flag_pct:<12}{composite_fmt:<12}"
              f"{r.grade:<8}{r.tier:<24}{r.color():<10}")
        assert r.grade == exp_grade, (
            f"Regression on (g={g}, flag={f}): "
            f"expected {exp_grade}, got {r.grade}"
        )
        assert r.tier == exp_tier
        assert r.color() == GRADE_COLORS_HEX[exp_grade]

    # Boundary checks — Layer 3
    assert grade_from_composite(0.981) == "AAA"
    assert grade_from_composite(0.9809) == "AA"
    assert grade_from_composite(0.834) == "B"
    assert grade_from_composite(0.8339) == "CCC"

    # Tier checks
    assert tier_from_grade("AAA") == "Production grade"
    assert tier_from_grade("BBB") == "Production grade"
    assert tier_from_grade("BB") == "Governance-required"
    assert tier_from_grade("CCC") == "Governance-required"

    # Color checks (frozen v1.0, see METHODOLOGY.md §6.3)
    assert color_from_grade("AAA") == "#1966CB"
    assert color_from_grade("BBB") == "#75BC5B"
    assert color_from_grade("BB")  == "#8EB848"
    assert color_from_grade("CCC") == "#F82117"

    # Trend checks — Layer 4
    flat = [0.92] * 200
    assert trend_from_history(flat) == Trend.STABLE

    rising = [0.90] * 100 + [0.92] * 100
    assert trend_from_history(rising) == Trend.POSITIVE

    falling = [0.92] * 100 + [0.90] * 100
    assert trend_from_history(falling) == Trend.NEGATIVE

    short = [0.92] * 50
    assert trend_from_history(short) == Trend.UNDER_REVIEW

    # Trend color checks
    assert color_from_trend(Trend.POSITIVE) == "#75BC5B"
    assert color_from_trend(Trend.NEGATIVE) == "#CE842D"
    assert color_from_trend(Trend.STABLE) == "#999999"
    assert color_from_trend(Trend.UNDER_REVIEW) == "#E8B83E"
    assert color_from_trend(None) == "#CCCCCC"  # n/a

    print("-" * 88)
    print("All self-tests passed.")


if __name__ == "__main__":
    _self_test()
