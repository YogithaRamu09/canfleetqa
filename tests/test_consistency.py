"""
test_consistency.py

Verifies the telemetry API's data actually matches real CAN bus
broadcasts - not just that each looks "valid" on its own. This is
the test that would catch a bug where the translation layer between
CAN and the API shows incorrect data to the user (e.g. app shows
45% battery while the real CAN data says 8%).
"""

import time
from framework.api_client import get_vehicle_status
from framework.can_utils import receive_message, decode_speed, SPEED_ID


def test_api_speed_matches_can_broadcast(can_bus):
    """
    Listens directly to the CAN bus for real speed values, then
    immediately checks the API's reported speed against that set -
    proving the API is genuinely relaying CAN data, not inventing
    its own. No extra sleep before checking, since the simulator
    broadcasts every second and any delay causes the API to move
    on to a newer value than what we collected.
    """
    seen_speeds = set()

    for _ in range(15):  # slightly wider window for safety
        msg = receive_message(can_bus, timeout=3)
        if msg is not None and msg.arbitration_id == SPEED_ID:
            seen_speeds.add(decode_speed(msg))
        if len(seen_speeds) >= 5:
            break

    assert seen_speeds, "No speed messages observed on the CAN bus"

    # Check immediately - no sleep here, to minimize timing drift
    api_speed = get_vehicle_status()["speed"]

    assert api_speed in seen_speeds, (
        f"API reported speed {api_speed}, but recent CAN broadcasts were "
        f"{seen_speeds} - the telemetry service may not be relaying CAN data correctly"
    )