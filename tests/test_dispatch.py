from sanjeevani import Complaint, Drone, GeoPoint, PatientReport, Vitals, plan_dispatch, triage
from sanjeevani.dispatch import haversine_km

V = Vitals(72, 16, 98, 120, 36.8)


def _report(lat=25.55, lon=85.20, complaint=Complaint.SNAKEBITE):
    return PatientReport("p", V, GeoPoint(lat, lon), complaint=complaint)


def test_haversine_zero():
    p = GeoPoint(25.0, 85.0)
    assert haversine_km(p, p) == 0


def test_picks_nearest_viable_drone():
    fleet = [Drone("far", GeoPoint(25.9, 85.2), 100, 80, 70), Drone("near", GeoPoint(25.56, 85.2), 100, 80, 70)]
    r = _report()
    plan = plan_dispatch(r, triage(r), fleet)
    assert plan.dispatched and plan.drone_id == "near"
    assert plan.needs_doctor_authorisation


def test_low_battery_drone_skipped():
    fleet = [Drone("weak", GeoPoint(25.56, 85.2), 10, 80, 70)]
    r = _report()
    assert not plan_dispatch(r, triage(r), fleet).dispatched


def test_green_case_not_dispatched():
    r = _report(complaint=Complaint.GENERAL)
    fleet = [Drone("d", GeoPoint(25.56, 85.2), 100, 80, 70)]
    assert not plan_dispatch(r, triage(r), fleet).dispatched
