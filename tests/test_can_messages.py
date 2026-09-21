"""
test_can_messages.py

Pytest tests validating CAN messages broadcast by can_simulator.py.
Requires can_simulator.py to be running in a separate terminal,
since messages are received over udp_multicast in real time.
"""

import pytest
from framework.can_utils import (
    receive_message,
    decode_speed,
    decode_battery,
    validate_signal_range,
    SPEED_ID,
    BATTERY_ID,
)


def test_speed_message_is_received(can_bus):
    """Confirms at least one speed message arrives within the timeout."""
    msg = receive_message(can_bus, timeout=3)
    assert msg is not None, "No CAN message received — is can_simulator.py running?"


def test_speed_value_within_valid_range(can_bus):
    """
    Listens until a speed message specifically arrives (ignoring
    battery messages), then checks the value is realistic.
    """
    for _ in range(10):  # try up to 10 messages in case battery comes first
        msg = receive_message(can_bus, timeout=3)
        assert msg is not None, "No message received — check simulator is running"
        if msg.arbitration_id == SPEED_ID:
            speed = decode_speed(msg)
            assert validate_signal_range(speed, 0, 180), f"Speed {speed} out of range"
            return
    pytest.fail("No speed message received in 10 attempts")


def test_battery_value_within_valid_range(can_bus):
    """Same pattern as above, but for battery messages."""
    for _ in range(10):
        msg = receive_message(can_bus, timeout=3)
        assert msg is not None, "No message received — check simulator is running"
        if msg.arbitration_id == BATTERY_ID:
            battery = decode_battery(msg)
            assert validate_signal_range(battery, 0, 100), f"Battery {battery}% out of range"
            return
    pytest.fail("No battery message received in 10 attempts")