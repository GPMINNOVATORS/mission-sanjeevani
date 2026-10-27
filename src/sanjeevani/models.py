"""Core data models shared by the field unit, triage engine and dispatcher."""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum


class Complaint(str, Enum):
    GENERAL = "general"
    ROAD_ACCIDENT = "road_accident"
    SNAKEBITE = "snakebite"
    PREGNANCY = "pregnancy"
    CARDIAC = "cardiac"


@dataclass(frozen=True)
class GeoPoint:
    lat: float
    lon: float


@dataclass(frozen=True)
class Vitals:
    heart_rate: int          # beats per minute
    resp_rate: int           # breaths per minute
    spo2: int                # oxygen saturation, %
    systolic_bp: int         # mmHg
    temperature_c: float     # degrees Celsius
    consciousness: str = "alert"  # "alert" | "confused" | "voice" | "pain" | "unresponsive"


@dataclass
class PatientReport:
    patient_id: str
    vitals: Vitals
    location: GeoPoint
    complaint: Complaint = Complaint.GENERAL
    age: int | None = None
    heavy_bleeding: bool = False
    seizure: bool = False
    reported_by: str = "field_unit"
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def from_dict(cls, d: dict) -> "PatientReport":
        return cls(
            patient_id=d["patient_id"],
            vitals=Vitals(**d["vitals"]),
            location=GeoPoint(**d["location"]),
            complaint=Complaint(d.get("complaint", "general")),
            age=d.get("age"),
            heavy_bleeding=d.get("heavy_bleeding", False),
            seizure=d.get("seizure", False),
            reported_by=d.get("reported_by", "field_unit"),
        )
