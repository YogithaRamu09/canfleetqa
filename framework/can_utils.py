"""
can_utils.py

Reusable helper functions for connecting to and interacting with
the CAN bus (via python-can's udp_multicast interface). Tests import
these functions instead of writing raw python-can code directly""
"""
import can

# Shared message ID reference (matches app/can_simulator.py)
SPEED_ID = 0x100
BATTERY_ID = 0x101

def get_bus():
    """
    Connects to the same udp_multicast CAN bus used by can_simulator.py.

    Both the simulator and the tests must use the same multicast
    address ('224.0.0.1') to see each other's messages. This interface
    works across separate processes, unlike the 'virtual' interface,
    which is required here since tests run independently from the
    simulator process.
    """
    return can.interface.Bus(channel = '224.0.0.1', bustype = 'udp_multicast')


def receive_message(bus, timeout=2):
    """
    Waits for a single CAN message to arrive on the bus.

    'timeout' is in seconds — if no message arrives in time,
    this returns None instead of hanging forever 
    (tests fail cleanly instead of freezing).
    """
    return bus.recv(timeout=timeout)

def decode_speed(msg):
    """Extracts the speed value (km/h) from a raw CAN message's first byte."""
    return msg.data[0]


def decode_battery(msg):
    """Extracts the battery value (%) from a raw CAN message's first byte."""
    return msg.data[0]

def validate_signal_range(value, min_value, max_value, signal_name="signal"):
    """
    Checks that a decoded signal value falls within an expected range.

    Returns True/False.
    The actual pass/fail decision and error message
    belongs in the test, not here.
    """
    return min_value <= value <= max_value