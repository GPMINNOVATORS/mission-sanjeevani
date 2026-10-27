"""Compact 17-byte uplink format for sending a PatientReport over LoRaWAN.

Layout (big-endian):
  u16 device_id | i32 lat_e6 | i32 lon_e6 | u8 HR | u8 RR | u8 SpO2 | u8 SBP |
  u8 temp ((t-30)*10) | u8 (consciousness<<4 | complaint) | u8 flags (b0 bleeding, b1 seizure)
"""
from __future__ import annotations

import struct

from .models import Complaint, GeoPoint, PatientReport, Vitals

_FMT = ">HiiBBBBBBB"
PAYLOAD_SIZE = struct.calcsize(_FMT)  # 17 bytes
CONSCIOUSNESS = ["alert", "confused", "voice", "pain", "unresponsive"]
COMPLAINTS = list(Complaint)


def _u8(x: float) -> int:
    return max(0, min(255, int(round(x))))


def encode(report: PatientReport, device_id: int) -> bytes:
    cons = CONSCIOUSNESS.index(report.vitals.consciousness)
    comp = COMPLAINTS.index(report.complaint)
    flags = (1 if report.heavy_bleeding else 0) | (2 if report.seizure else 0)
    v = report.vitals
    return struct.pack(
        _FMT,
        device_id,
        round(report.location.lat * 1e6),
        round(report.location.lon * 1e6),
        _u8(v.heart_rate), _u8(v.resp_rate), _u8(v.spo2), _u8(v.systolic_bp),
        _u8((v.temperature_c - 30) * 10),
        (cons << 4) | comp,
        flags,
    )


def decode(data: bytes) -> tuple[int, PatientReport]:
    if len(data) != PAYLOAD_SIZE:
        raise ValueError(f"expected {PAYLOAD_SIZE} bytes, got {len(data)}")
    dev, lat, lon, hr, rr, spo2, sbp, temp, cc, flags = struct.unpack(_FMT, data)
    report = PatientReport(
        patient_id=f"D{dev}",
        vitals=Vitals(hr, rr, spo2, sbp, temp / 10 + 30, CONSCIOUSNESS[cc >> 4]),
        location=GeoPoint(lat / 1e6, lon / 1e6),
        complaint=COMPLAINTS[cc & 0x0F],
        heavy_bleeding=bool(flags & 1),
        seizure=bool(flags & 2),
        reported_by="lorawan",
    )
    return dev, report
