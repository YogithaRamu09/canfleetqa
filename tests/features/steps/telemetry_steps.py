"""
telemetry_steps.py

Step definitions connecting the Gherkin scenarios in telemetry.feature
to real Python code. Each @given/@when/@then function matches a line
of English in the .feature file by its exact wording.
"""
from pytest_bdd import scenarios, given, when, then, parsers
from framework.api_client import get_vehicle_status, get_vehicle_battery
from framework.can_utils import validate_signal_range, classify_battery

# Loads every scenario from telemetry.feature automatically
scenarios("../telemetry.feature")

@given("the telemetry service is running")
def telemetry_servive_running():
    """
    No setup code needed here - this step just documents an assumption.
    The actual service must be started manually in a separate terminal
    (python app/telemetry_service.py) before running these tests.
    """
    pass

@when("I request the vehicle status",target_fixture="status_response")
def request_vehicle_status():
     """Calls the API and stores the result for the Then step to check."""
     return get_vehicle_status()

@then("the response should include speed, battery, and timestamp")
def check_status_fields(status_response):
     assert "speed" in status_response 
     assert "battery" in status_response
     assert "timestamp" in status_response


@when("I request the vehicle battery level", target_fixture = "battery_resposne")
def request_vehicle_battery():
    return get_vehicle_battery()

@then("the battery percentage should be between 0 and 100")
def check_battery_range(battery_resposne):
    battery = battery_resposne["battery"] 
    assert validate_signal_range(battery,0,100),f"Battery {battery}% out of range"

@given(parsers.parse("the battery level is {battery_percent:d}%"), target_fixture="battery_percent")
def given_battery_level(battery_percent):
    """Stores the battery value from the Examples table for later steps."""
    return battery_percent


@when("the battery status is evaluated", target_fixture="evaluated_status")
def evaluate_battery_status(battery_percent):
    return classify_battery(battery_percent)


@then(parsers.parse('the status should be "{expected_status}"'))
def check_battery_status(evaluated_status, expected_status):
    assert evaluated_status == expected_status