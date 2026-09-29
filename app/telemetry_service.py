"""
telemetry_service.py

A Flask API standing in for a real vehicle telemetry backend.
Unlike earlier versions, this now reads REAL data from the CAN bus
via a background thread, instead of generating independent random
values. This means the API genuinely reflects what the CAN bus is
broadcasting - the same way a real vehicle's gateway module reads
CAN signals and forwards them to an app/backend.

This is what makes it possible to test CONSISTENCY between the CAN
layer and the API layer, not just validity of each on its own.
"""

from flask import Flask, jsonify
import threading
import time
from framework.can_utils import (
    get_bus, receive_message, decode_speed, decode_battery,
    SPEED_ID, BATTERY_ID,
)

app = Flask(__name__)

# Shared state, updated by the background CAN listener thread and
# read by the Flask request handlers. A lock prevents the two from
# reading/writing at the exact same instant and corrupting data.
vehicle_state = {"speed": None, "battery": None, "timestamp": None}
state_lock = threading.Lock()


def can_listener():
    """
    Runs forever in a background thread, listening to the same CAN
    bus as can_simulator.py. Every time a speed or battery message
    arrives, it updates vehicle_state - so the API always reflects
    the most recent real CAN broadcast, not invented data.
    """
    bus = get_bus()
    while True:
        msg = receive_message(bus, timeout=5)
        if msg is None:
            continue
        with state_lock:
            if msg.arbitration_id == SPEED_ID:
                vehicle_state["speed"] = decode_speed(msg)
                vehicle_state["timestamp"] = time.time()
            elif msg.arbitration_id == BATTERY_ID:
                vehicle_state["battery"] = decode_battery(msg)
                vehicle_state["timestamp"] = time.time()


@app.route("/vehicle/status", methods=["GET"])
def get_status():
    """Returns the latest speed/battery values received from the CAN bus."""
    with state_lock:
        return jsonify(dict(vehicle_state))


@app.route("/vehicle/battery", methods=["GET"])
def get_battery():
    with state_lock:
        return jsonify({"battery": vehicle_state["battery"]})


if __name__ == "__main__":
    # Start the CAN listener as a background thread before the Flask
    # server starts. daemon=True means it stops automatically when
    # the main program exits.
    listener_thread = threading.Thread(target=can_listener, daemon=True)
    listener_thread.start()

    # debug=False and use_reloader=False are important here: Flask's
    # reloader normally restarts the app in a second process, which
    # would start a second, duplicate CAN listener thread.
    app.run(debug=False, use_reloader=False, threaded=True, port=5000)