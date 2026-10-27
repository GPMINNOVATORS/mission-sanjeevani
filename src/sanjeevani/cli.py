"""Command line: `sanjeevani triage|serve|compare`."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from .dispatch import DEMO_FLEET, plan_dispatch
from .impact import SCENARIOS, compare
from .models import PatientReport
from .triage import triage


def _cmd_triage(args: argparse.Namespace) -> int:
    report = PatientReport.from_dict(json.loads(args.report.read_text()))
    result = triage(report)
    plan = plan_dispatch(report, result, DEMO_FLEET)
    print(f"Patient   : {report.patient_id}")
    print(f"Triage    : {result.level.name} (score {result.score})")
    for r in result.reasons:
        print(f"  - {r}")
    print(f"Dispatch  : {'YES' if plan.dispatched else 'NO'}")
    if plan.dispatched:
        print(f"  Drone {plan.drone_id}, payload {plan.payload}, {plan.distance_km} km, ETA {plan.eta_minutes} min")
    for n in plan.notes:
        print(f"  * {n}")
    return 0


def _cmd_serve(args: argparse.Namespace) -> int:
    from .server import make_server

    srv = make_server(args.host, args.port)
    print(f"Control room running at http://{args.host}:{args.port}  (Ctrl+C to stop)")
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    return 0


def _cmd_compare(args: argparse.Namespace) -> int:
    print(f"Illustrative ETA for {args.km} km straight-line distance (ASSUMPTIONS, not measured data)")
    for s in SCENARIOS:
        r = compare(args.km, s)
        print(f"  {r['scenario']:<22} road {r['road_min']:>6} min | drone {r['drone_min']:>5} min | saved {r['saved_min']:>6} min")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="sanjeevani", description="Mission Sanjeevani toolkit")
    sub = p.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("triage", help="triage a patient report JSON and plan dispatch")
    t.add_argument("report", type=Path)
    t.set_defaults(fn=_cmd_triage)
    s = sub.add_parser("serve", help="run the control-room web dashboard")
    s.add_argument("--host", default="127.0.0.1")
    s.add_argument("--port", type=int, default=8000)
    s.set_defaults(fn=_cmd_serve)
    c = sub.add_parser("compare", help="illustrative road vs drone ETA")
    c.add_argument("--km", type=float, default=10.0)
    c.set_defaults(fn=_cmd_compare)
    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
