"""Test excel_math.py."""

import pytest
from model import excel_math



def test_round():
    assert excel_math.round(1.4) == 1
    assert excel_math.round(1.5) == 2
    assert excel_math.round(1.6) == 2
    assert excel_math.round(-1.4) == -1
    assert excel_math.round(-1.5) == -2
    assert excel_math.round(-1.6) == -2

    # from OnshoreWind
    assert excel_math.round(63998.595 / 2844.382) == 23

    # from Water Efficiency
    assert excel_math.round(1629.9388631986958 / 72.44172725327537) == 23
    assert excel_math.round(1086.6259087991305 / 72.44172725327537) == 15
