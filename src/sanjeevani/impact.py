"""Illustrative response-time comparison: road ambulance vs drone.

IMPORTANT: every number here is an ASSUMPTION, not measured data. Replace the
defaults with values measured in a real pilot before quoting any result.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Scenario:
    name: str
    road_factor: float        # road distance / straight-line distance
    ambulance_kmh: float      # average road speed
    mobilise_min: float       # time to get an ambulance moving


SCENARIOS = [
    Scenario("Normal roads", road_factor=1.4, ambulance_kmh=30, mobilise_min=10),
    Scenario("Flood-affected roads", road_factor=2.0, ambulance_kmh=15, mobilise_min=10),
]


def compare(air_km: float, scenario: Scenario, drone_kmh: float = 70, drone_launch_min: float = 3) -> dict:
    road = scenario.mobilise_min + air_km * scenario.road_factor / scenario.ambulance_kmh * 60
    drone = drone_launch_min + air_km / drone_kmh * 60
    return {
        "scenario": scenario.name,
        "air_km": air_km,
        "road_min": round(road, 1),
        "drone_min": round(drone, 1),
        "saved_min": round(road - drone, 1),
    }
