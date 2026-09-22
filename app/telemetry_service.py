"""
telemetry_service.py

A small Flask API standing in for a real vehicle telemetry backend.
In a real system, this would pull live data from the vehicle's ECUs;
here we simulate it with in-memory values that update slightly on
each request, so tests have something realistic to validate.

Endpoints:
    GET /vehicle/status   -> speed, battery, timestamp
    GET /vehicle/battery  -> battery level only
"""

from flask import Flask, jsonify
import random
import time

app = Flask(__name__)

# In-memory "vehicle state" - starts at reasonable defaults.
# A real backend would read this from a database or live ECU feed.
vehicle_state = {
    "speed": 0,
    "battery": 100
}


def update_state():
    """
    Simulates the vehicle's state changing slightly over time.
    Speed moves randomly; battery only decreases (like a real EV
    draining while driving), never charges back up on its own.
    """
    vehicle_state["speed"] = random.randint(0, 180)
    vehicle_state["battery"] = max(0, vehicle_state["battery"] - random.randint(0, 2))


@app.route("/vehicle/status", methods=["GET"])
def get_status():
    """Returns full vehicle status: speed, battery, and a timestamp."""
    update_state()
    return jsonify({
        "speed": vehicle_state["speed"],
        "battery": vehicle_state["battery"],
        "timestamp": time.time()
    })


@app.route("/vehicle/battery", methods=["GET"])
def get_battery():
    """Returns just the battery level - useful for a low-battery alert scenario."""
    update_state()
    return jsonify({
        "battery": vehicle_state["battery"]
    })


if __name__ == "__main__":
    # debug=True auto-reloads on code changes - handy while developing.
    # Turn this off before anything resembling production use.
    app.run(debug=True, port=5000)