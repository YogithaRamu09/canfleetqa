"""
can_simulator.py

Simulates a vehicle ECU broadcasting sensor data over a CAN bus.
Uses python-can's 'udp_multicast' interface, which simulates a CAN
bus over UDP multicast on the local machine. Unlike the 'virtual'
interface (which only works within a single Python process), this
lets separate scripts/processes (e.g. this simulator and a test
runner) send and receive messages from each other — needed since
our tests run as a separate process from the simulator.

Message ID reference (like a mini DBC):
    0x100 -> Vehicle speed (km/h)
    0x101 -> Battery level (%)
"""
import can
import time
import random

def create_bus():
    """
    Creates and returns a CAN bus connection using UDP multicast.

    '224.0.0.1' is a multicast group address — any process on this
    machine that connects using the same address joins the same
    simulated bus, similar to how real ECUs share one physical CAN
    wire. This interface (unlike 'virtual') works across separate
    processes, which is why we use it here instead.

    Requires the 'msgpack' package to serialize messages.
    """
    return can.interface.Bus(channel = '224.0.0.1', bustype = 'udp_multicast')

def send_speed_message(bus):
    """
    Builds and sends a fake 'vehicle speed' CAN message.

    - arbitration_id=0x100 is the fixed ID that identifies this
      message as speed data (receivers use this ID to know what
      kind of data they're reading).
    - data must always be exactly 8 bytes for a standard CAN frame;
      here we only use the first byte for the speed value and pad
      the rest with zeros.
    """
    speed = random.randint(0, 180)  # simulated vehicle speed in km/h
    msg = can.Message(
        arbitration_id=0x100,
        data=[speed, 0, 0, 0, 0, 0, 0, 0],
        is_extended_id=False    # using standard 11-bit CAN ID
    )
    bus.send(msg)
    print(f"Sent speed message: {speed} km/h")

def send_battery_message(bus):
    """
    Builds and sends a fake 'battery level' CAN message.

    Same structure as send_speed_message, but uses arbitration_id=0x101
    so receivers can tell speed data and battery data apart.
    """
    battery = random.randint(0, 100)
    msg = can.Message(
        arbitration_id=0x101,
        data=[battery, 0, 0, 0, 0, 0, 0, 0],
        is_extended_id=False 
    )
    bus.send(msg)
    print(f"Sent battery message: {battery}%")

# This block only runs when the file is executed directly
# (not when it's imported by a test file later).
if __name__ == "__main__":
    bus = create_bus()
    # Continuously broadcast both signals every second,
    # simulating a real ECU that reports status on a regular interval.
    while True:
        send_speed_message(bus)
        send_battery_message(bus)
        time.sleep(1)


