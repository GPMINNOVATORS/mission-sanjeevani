"""Drone selection and payload planning."""
from __future__ import annotations

from dataclasses import dataclass, field
from math import asin, cos, radians, sin, sqrt

from .models import Complaint, GeoPoint, PatientReport
from .triage import TriageLevel, TriageResult

RESERVE_FACTOR = 1.25   # require 25% range margin on the round trip
MIN_BATTERY_PCT = 30

# Payload kits are placeholders. Contents must be defined by clinical protocol.
PAYLOADS: dict[Complaint, tuple[str, bool]] = {
    # complaint: (kit name, needs remote doctor authorisation before release)
    Complaint.SNAKEBITE: ("snakebite_kit", True),
    Complaint.PREGNANCY: ("obstetric_kit", True),
    Complaint.ROAD_ACCIDENT: ("trauma_kit", False),
    Complaint.CARDIAC: ("cardiac_kit", True),
    Complaint.GENERAL: ("first_aid_kit", False),
}


@dataclass
class Drone:
    drone_id: str
    position: GeoPoint
    battery_pct: float
    range_km: float          # full-battery round-trip range
    speed_kmh: float
    available: bool = True


@dataclass
class DispatchPlan:
    dispatched: bool
    drone_id: str | None = None
    payload: str | None = None
    distance_km: float = 0.0
    eta_minutes: float = 0.0
    needs_doctor_authorisation: bool = False
    notes: list[str] = field(default_factory=list)


def haversine_km(a: GeoPoint, b: GeoPoint) -> float:
    r = 6371.0088
    dlat, dlon = radians(b.lat - a.lat), radians(b.lon - a.lon)
    h = sin(dlat / 2) ** 2 + cos(radians(a.lat)) * cos(radians(b.lat)) * sin(dlon / 2) ** 2
    return 2 * r * asin(sqrt(h))


def plan_dispatch(report: PatientReport, result: TriageResult, fleet: list[Drone]) -> DispatchPlan:
    if result.level < TriageLevel.ORANGE:
        return DispatchPlan(False, notes=["Below dispatch threshold: route to telemedicine/ASHA follow-up."])

    payload, needs_auth = PAYLOADS[report.complaint]
    candidates: list[tuple[float, Drone, float]] = []
    for d in fleet:
        if not d.available or d.battery_pct < MIN_BATTERY_PCT:
            continue
        dist = haversine_km(d.position, report.location)
        usable_range = d.range_km * d.battery_pct / 100
        if 2 * dist * RESERVE_FACTOR > usable_range:
            continue
        candidates.append((dist / d.speed_kmh * 60, d, dist))

    if not candidates:
        return DispatchPlan(False, notes=["No drone in range with sufficient battery: escalate to ambulance/helpline."])

    eta, best, dist = min(candidates, key=lambda t: t[0])
    notes = ["Connect doctor via telemedicine on dispatch."]
    if needs_auth:
        notes.append("Payload release requires remote doctor authorisation.")
    return DispatchPlan(True, best.drone_id, payload, round(dist, 2), round(eta, 1), needs_auth, notes)


# Demo fleet used by the CLI and web dashboard (illustrative positions around Patna/Bihar).
DEMO_FLEET = [
    Drone("D-01", GeoPoint(25.61, 85.14), 90, 40, 70),
    Drone("D-02", GeoPoint(25.45, 85.30), 55, 40, 70),
]
