import pytest

from sanjeevani import Complaint, GeoPoint, PatientReport, Vitals
from sanjeevani.lora_payload import PAYLOAD_SIZE, decode, encode


def _report():
    return PatientReport(
        "x", Vitals(112, 22, 94, 105, 37.2, "confused"), GeoPoint(25.55, 85.2),
        complaint=Complaint.SNAKEBITE, heavy_bleeding=True,
    )


def test_fits_lorawan_limit():
    assert len(encode(_report(), 7)) == PAYLOAD_SIZE <= 51


def test_roundtrip():
    dev, r = decode(encode(_report(), 42))
    assert dev == 42
    assert (r.vitals.heart_rate, r.vitals.spo2, r.vitals.consciousness) == (112, 94, "confused")
    assert abs(r.vitals.temperature_c - 37.2) < 0.06
    assert abs(r.location.lat - 25.55) < 1e-5
    assert r.complaint is Complaint.SNAKEBITE and r.heavy_bleeding and not r.seizure


def test_bad_length_rejected():
    with pytest.raises(ValueError):
        decode(b"\x00" * 5)
