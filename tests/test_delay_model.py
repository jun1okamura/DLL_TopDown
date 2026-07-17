"""
test_delay_model.py

Unit tests for delay_model.py

Issue #6 : Ideal Delay Model
"""

from dll.delay_model import IdealDelayModel
from dll.params import DLLParams


# ============================================================
# Constructor
# ============================================================

def test_create_delay_model():

    params = DLLParams.default()

    model = IdealDelayModel(params)

    assert model.delay_init == params.delay.delay_init
    assert model.delay_gain == params.delay.delay_gain
    assert model.delay_min == params.delay.delay_min
    assert model.delay_max == params.delay.delay_max


# ============================================================
# Zero Control
# ============================================================

def test_zero_control():

    params = DLLParams.default()

    model = IdealDelayModel(params)

    delay = model.update(0.0)

    assert delay == params.delay.delay_init


# ============================================================
# Positive Control
# ============================================================

def test_positive_control():

    params = DLLParams.default()

    model = IdealDelayModel(params)

    control = 0.5

    delay = model.update(control)

    expected = (
        params.delay.delay_init
        + control * params.delay.delay_gain
    )

    assert delay == expected


# ============================================================
# Negative Control
# ============================================================

def test_negative_control():

    params = DLLParams.default()

    model = IdealDelayModel(params)

    control = -0.5

    delay = model.update(control)

    expected = (
        params.delay.delay_init
        + control * params.delay.delay_gain
    )

    assert delay == expected


# ============================================================
# Minimum Limit
# ============================================================

def test_minimum_limit():

    params = DLLParams.default()

    model = IdealDelayModel(params)

    delay = model.update(-1.0e9)

    assert delay == params.delay.delay_min


# ============================================================
# Maximum Limit
# ============================================================

def test_maximum_limit():

    params = DLLParams.default()

    model = IdealDelayModel(params)

    delay = model.update(1.0e9)

    assert delay == params.delay.delay_max


# ============================================================
# Deterministic Behavior
# ============================================================

def test_repeatability():

    params = DLLParams.default()

    model = IdealDelayModel(params)

    control = 0.12345

    delay1 = model.update(control)
    delay2 = model.update(control)

    assert delay1 == delay2

def test_model_does_not_modify_parameters():

    params = DLLParams.default()

    model = IdealDelayModel(params)

    _ = model.update(0.5)

    assert params.delay.delay_init == model.delay_init