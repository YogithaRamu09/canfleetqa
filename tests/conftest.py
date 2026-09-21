"""
conftest.py

Shared Pytest fixtures for CAN message tests. Fixtures here are
automatically available to any test file in this folder 
"""

import pytest
from framework.can_utils import get_bus


@pytest.fixture
def can_bus():
    """
    Provides a connected CAN bus for a test to use.

    'yield' (instead of 'return') lets us run cleanup code after
    the test finishes — here, we shut down the bus properly so we
    don't get 'not properly shut down' warnings.
    """
    bus = get_bus()
    yield bus
    bus.shutdown()