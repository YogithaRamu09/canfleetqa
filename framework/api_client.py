"""
api_client.py

Reusable wrapper around requests calls to the telemetry API.
Tests call these functions instead of writing raw requests.get()
calls everywhere, keeping test files focused on assertions.
"""

import requests

BASE_URL = "http://127.0.0.1:5000"


def get_vehicle_status():
    """
    Calls GET /vehicle/status and returns the parsed JSON response.
    Raises an error automatically if the request fails (e.g. API
    isn't running) via raise_for_status().
    """
    response = requests.get(f"{BASE_URL}/vehicle/status", timeout=3)
    response.raise_for_status()
    return response.json()


def get_vehicle_battery():
    """Calls GET /vehicle/battery and returns the parsed JSON response."""
    response = requests.get(f"{BASE_URL}/vehicle/battery", timeout=3)
    response.raise_for_status()
    return response.json()