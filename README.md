# CANFleetQA

![CI](https://github.com/YogithaRamu09/canfleetqa/actions/workflows/ci.yml/badge.svg)

A Python test automation framework simulating vehicle CAN bus data and a telemetry REST API — built to demonstrate hands-on QA and automation skills during a career break.

## What This Project Does

CANFleetQA simulates two things a real vehicle system provides:

- **CAN bus signals** — speed and battery data, broadcast the way a vehicle ECU would
- **A telemetry REST API** — a Flask service representing a vehicle backend/dashboard

It then automatically validates that data using Pytest — including plain assertions, parametrized boundary tests, and BDD-style Gherkin scenarios — the same way a real automotive QA engineer would validate vehicle systems with tools like CANoe/CANalyzer.

## Tech Stack

- **Python** — core language
- **Pytest** — test framework (fixtures, parametrization, markers)
- **pytest-bdd** — BDD-style Gherkin scenarios
- **python-can** — CAN bus simulation
- **Flask** — mock vehicle telemetry API
- **GitHub Actions** — CI pipeline, runs the full suite on every push
- **pytest-html** — HTML test reports

## Project Structure
canfleetqa/
├── app/ # Simulates the vehicle
│ ├── can_simulator.py  #Broadcasts CAN speed/battery messages
│ └── telemetry_service.py  #Flask API simulating a vehicle backend
├── framework/  #Reusable test helpers
│ ├── can_utils.py  #CAN connect/receive/validate/classify
│ └── api_client.py #API request wrapper
├── tests/
│ ├── conftest.py #Shared Pytest fixtures
│ ├── test_can_messages.py #CAN bus tests (incl. parametrized)
│ ├── test_telemetry_api.py #API tests
│ └── features/ #Gherkin BDD scenarios
├── .github/workflows/ci.yml #CI pipeline
└── requirements.txt


## How to Run Locally

1. Clone the repo and set up a virtual environment:
```bash
   git clone https://github.com/YogithaRamu09/canfleetqa.git
   cd canfleetqa
   python -m venv venv
   source venv/Scripts/activate   # Windows (Git Bash)
   pip install -r requirements.txt
```

2. Start the simulators (in Git Bash, run in the background):
```bash
   python app/can_simulator.py &
   python app/telemetry_service.py &
```

3. Run the tests:
```bash
   pytest tests/ -v --html=reports/report.html --self-contained-html
```

4. Open `reports/report.html` in a browser to view the test report.

## CI/CD

Every push to `main` automatically triggers a GitHub Actions workflow that installs dependencies, starts both simulators, and runs the full test suite — including an HTML report saved as a downloadable artifact.

## A Technical Decision Worth Noting

The CAN simulator initially used python-can's `virtual` bus interface, which only shares messages within a single Python process. Since the simulator and test runner run as **separate processes** (and separately again in CI), this caused tests to silently receive nothing. The fix was switching to the `udp_multicast` interface, which allows independent processes to share simulated CAN messages — a more realistic setup for how CI environments actually run tests.

## Background

Built by Yogitha Ramu, a Senior QA & Test Automation Engineer with 9+ years of experience in automotive, EV, and embedded systems testing, during a career break — to keep automation skills current and demonstrate framework design ability.