"""Rule-based triage engine.

The vitals scoring is modelled on the publicly documented NEWS2 early-warning
score (room-air scale), with simple complaint-based escalation rules layered on top.

SAFETY: This is a research prototype. Thresholds and escalation rules MUST be
reviewed and validated by qualified clinicians before any real-world use.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum

from .models import Complaint, PatientReport, Vitals


class TriageLevel(IntEnum):
    GREEN = 0    # non-urgent: telemedicine advice
    YELLOW = 1   # semi-urgent: monitor, schedule transport
    ORANGE = 2   # urgent: dispatch drone + doctor on call
    RED = 3      # critical: immediate dispatch, highest priority


@dataclass
class TriageResult:
    level: TriageLevel
    score: int
    reasons: list[str] = field(default_factory=list)


def _band(value: float, bands: list[tuple[float, float, int]]) -> int:
    for lo, hi, pts in bands:
        if lo <= value <= hi:
            return pts
    return 0


INF = float("inf")


def score_vitals(v: Vitals) -> tuple[int, list[str]]:
    """Return (aggregate score, reasons for any single-parameter red flag)."""
    parts = {
        "respiratory rate": (_band(v.resp_rate, [(-INF, 8, 3), (9, 11, 1), (12, 20, 0), (21, 24, 2), (25, INF, 3)]), v.resp_rate),
        "SpO2": (_band(v.spo2, [(-INF, 91, 3), (92, 93, 2), (94, 95, 1), (96, INF, 0)]), v.spo2),
        "systolic BP": (_band(v.systolic_bp, [(-INF, 90, 3), (91, 100, 2), (101, 110, 1), (111, 219, 0), (220, INF, 3)]), v.systolic_bp),
        "heart rate": (_band(v.heart_rate, [(-INF, 40, 3), (41, 50, 1), (51, 90, 0), (91, 110, 1), (111, 130, 2), (131, INF, 3)]), v.heart_rate),
        "temperature": (_band(v.temperature_c, [(-INF, 35.0, 3), (35.1, 36.0, 1), (36.1, 38.0, 0), (38.1, 39.0, 1), (39.1, INF, 2)]), v.temperature_c),
        "consciousness": (0 if v.consciousness == "alert" else 3, v.consciousness),
    }
    total = sum(p for p, _ in parts.values())
    flags = [f"{name} = {val} (red flag)" for name, (p, val) in parts.items() if p == 3]
    return total, flags


def triage(report: PatientReport) -> TriageResult:
    score, flags = score_vitals(report.vitals)
    reasons = list(flags)

    if score >= 7:
        level = TriageLevel.RED
    elif score >= 5 or flags:
        level = TriageLevel.ORANGE
    elif score >= 1:
        level = TriageLevel.YELLOW
    else:
        level = TriageLevel.GREEN

    def escalate(to: TriageLevel, why: str) -> None:
        nonlocal level
        if to > level:
            level = to
        reasons.append(why)

    c = report.complaint
    if c is Complaint.SNAKEBITE:
        escalate(TriageLevel.ORANGE, "snakebite: time-critical, needs doctor guidance")
    if c is Complaint.PREGNANCY:
        if report.heavy_bleeding or report.seizure:
            escalate(TriageLevel.RED, "pregnancy with bleeding/seizure: obstetric emergency")
        else:
            escalate(TriageLevel.YELLOW, "pregnancy complaint: needs assessment")
    if c is Complaint.ROAD_ACCIDENT:
        if report.heavy_bleeding or report.vitals.consciousness != "alert":
            escalate(TriageLevel.RED, "trauma with bleeding or altered consciousness")
        else:
            escalate(TriageLevel.ORANGE, "road accident: possible occult injury")
    if c is Complaint.CARDIAC:
        escalate(TriageLevel.ORANGE, "suspected cardiac event")

    return TriageResult(level=level, score=score, reasons=reasons)
