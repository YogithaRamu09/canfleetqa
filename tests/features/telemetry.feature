Feature: Vehicle telemetry monitoring
    As a vehicle monitoring system
    I want to check the vehicle's status
    So that I can detect issues like low battery

    Scenario: Vehicle status is available
        Given the telemetry service is running
        When I request the vehicle status
        Then the response should include speed, battery, and timestamp

    Scenario: Battery level is realistic
        Given the telemetry service is running
        When I request the vehicle battery level
        Then the battery percentage should be between 0 and 100

    Scenario: Battery status is classified correctly
        Given the battery level is <battery_percent>%
        When the battery status is evaluated
        Then the status should be "<expected_status>"

        Examples:
            | battery_percent  | expected_status |
            | 100              | Normal          |
            | 50               | Normal          |
            | 20               | Normal          |
            | 19               | Low             |
            | 10               | Low             |
            | 9                | Critical        |
            | 0                | Critical        |