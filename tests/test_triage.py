from sanjeevani import Complaint, GeoPoint, PatientReport, TriageLevel, Vitals, triage

LOC = GeoPoint(25.5, 85.2)
NORMAL = Vitals(heart_rate=72, resp_rate=16, spo2=98, systolic_bp=120, temperature_c=36.8)


def test_healthy_patient_is_green():
    assert triage(PatientReport("p", NORMAL, LOC)).level == TriageLevel.GREEN


def test_unresponsive_patient_is_at_least_orange():
    v = Vitals(72, 16, 98, 120, 36.8, consciousness="unresponsive")
    assert triage(PatientReport("p", v, LOC)).level >= TriageLevel.ORANGE


def test_multi_system_derangement_is_red():
    v = Vitals(135, 28, 88, 85, 39.5)
    assert triage(PatientReport("p", v, LOC)).level == TriageLevel.RED


def test_snakebite_escalates_even_with_normal_vitals():
    r = triage(PatientReport("p", NORMAL, LOC, complaint=Complaint.SNAKEBITE))
    assert r.level == TriageLevel.ORANGE


def test_pregnancy_with_bleeding_is_red():
    r = triage(PatientReport("p", NORMAL, LOC, complaint=Complaint.PREGNANCY, heavy_bleeding=True))
    assert r.level == TriageLevel.RED
