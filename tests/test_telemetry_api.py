"""
test_telemetry_api.py

Pytest tests validating the Flask telemetry API.
Requires app/telemetry_service.py to be running separately
(python app/telemetry_service.py) before running these tests.
"""

from framework.api_client import get_vehicle_status, get_vehicle_battery
from framework.can_utils import validate_signal_range


def test_status_endpoint_returns_expected_fields():
    """Confirms the /vehicle/status response has all expected keys."""
    data = get_vehicle_status()
    assert "speed" in data
    assert "battery" in data
    assert "timestamp" in data


def test_status_speed_within_valid_range():
    """Confirms speed from the API is realistic (0-180 km/h)."""
    data = get_vehicle_status()
    speed = data["speed"]
    assert validate_signal_range(speed, 0, 180), f"Speed {speed} out of range"


def test_status_battery_within_valid_range():
    """Confirms battery from the API is realistic (0-100%)."""
    data = get_vehicle_status()
    battery = data["battery"]
    assert validate_signal_range(battery, 0, 100), f"Battery {battery}% out of range"


def test_battery_endpoint_returns_expected_field():
    """Confirms the /vehicle/battery response has the battery key."""
    data = get_vehicle_battery()
    assert "battery" in data


def test_battery_endpoint_value_within_valid_range():
    """Confirms the dedicated battery endpoint also returns a realistic value."""
    data = get_vehicle_battery()
    battery = data["battery"]
    assert validate_signal_range(battery, 0, 100), f"Battery {battery}% out of range"