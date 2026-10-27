import json
import threading
import urllib.error
import urllib.request

from sanjeevani.impact import SCENARIOS, compare
from sanjeevani.server import make_server


def test_drone_faster_and_flood_gap_larger():
    normal, flood = (compare(10, s) for s in SCENARIOS)
    assert normal["saved_min"] > 0
    assert flood["saved_min"] > normal["saved_min"]


def _serve():
    srv = make_server("127.0.0.1", 0)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv, f"http://127.0.0.1:{srv.server_address[1]}"


def test_api_assess_and_page():
    srv, base = _serve()
    try:
        body = {
            "patient_id": "t", "complaint": "snakebite",
            "vitals": {"heart_rate": 112, "resp_rate": 22, "spo2": 94, "systolic_bp": 105,
                       "temperature_c": 37.2, "consciousness": "alert"},
            "location": {"lat": 25.55, "lon": 85.2},
        }
        req = urllib.request.Request(base + "/api/assess", json.dumps(body).encode(),
                                     {"Content-Type": "application/json"})
        data = json.loads(urllib.request.urlopen(req).read())
        assert data["level"] == "ORANGE" and data["dispatch"]["dispatched"]
        assert b"Mission Sanjeevani" in urllib.request.urlopen(base + "/").read()
    finally:
        srv.shutdown()


def test_bad_request_returns_400():
    srv, base = _serve()
    try:
        req = urllib.request.Request(base + "/api/assess", b'{"oops":1}', {"Content-Type": "application/json"})
        try:
            urllib.request.urlopen(req)
            raise AssertionError("expected 400")
        except urllib.error.HTTPError as e:
            assert e.code == 400
    finally:
        srv.shutdown()
