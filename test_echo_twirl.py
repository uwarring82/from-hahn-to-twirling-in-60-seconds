"""Checks for echo_twirl.py.  Run ``python -m pytest`` or ``python test_echo_twirl.py``.

SPDX-License-Identifier: MIT
"""
import json
from contextlib import redirect_stdout
from dataclasses import replace
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np

import echo_twirl as et

P = et.DEFAULT
F0 = et.null_detuning(P)  # 1250 Hz for T = 200 us


def test_null_location():
    assert np.isclose(F0, 1250.0)


def test_ideal_limit():
    et.check_ideal_limit(P)


def test_values_quoted_in_text():
    """Numbers quoted in README.md and echo_twirl_perspective.md."""
    quoted = {0.0: (0.950, 0.943), 1250.0: (0.949, 0.002), 2500.0: (0.941, -0.933)}
    for f, (echo_x, twirl_x) in quoted.items():
        echo, twirl = et.signals(f, P)
        assert abs(echo[0] - echo_x) < 5e-4, (f, echo[0])
        assert abs(twirl[0] - twirl_x) < 5e-4, (f, twirl[0])
    echo, twirl = et.signals(F0, P)
    assert abs(et.transverse(echo) - 0.949) < 5e-4
    assert abs(et.transverse(twirl) - 0.0025) < 5e-5


def test_shot_noise_quoted_in_text():
    diff, se = et.shot_noise(F0, P)
    assert abs(diff - 0.474) < 5e-4
    assert abs(se - 0.012) < 5e-4


def test_branches_have_opposite_y_at_null():
    """Keeping the frame bit recovers full, opposite fringes at the pooled zero."""
    branch_i, branch_x = et.branches(F0, P)
    assert branch_i[1] > 0.93 and branch_x[1] < -0.93
    assert abs(et.signals(F0, P)[1][0]) < 5e-3


def test_conditional_probability_signal_and_precision():
    difference, se = et.conditional_y(F0, P)
    assert round(difference, 3) == 0.941 and round(se, 3) == 0.008
    assert np.isclose(et.conditional_y(F0, replace(P, shots=8000))[1], se / 2)
    assert np.isclose(et.conditional_y(F0, replace(P, vis=0, shots=5))[1],
                      np.sqrt(0.25 / 2 + 0.25 / 3))


def test_cli_scan_and_shot_allocation():
    with TemporaryDirectory() as temp, redirect_stdout(StringIO()):
        et.main(["--T", "0.083", "--rabi", "60000", "--area", "1.02",
                 "--jitter", "0", "--vis", "0.85", "--shots", "1001",
                 "--closing", "-1", "--no-figure", "--outdir", temp])
        out = Path(temp)
        meta = json.loads((out / "echo_twirl.json").read_text())
        params = {k: v["value"] for k, v in meta["parameters"].items()}
        assert params == dict(T=0.083, rabi=60000, area=1.02, jitter=0,
                              vis=0.85, shots=1001, closing=-1, gh_nodes=24)
        assert meta["derived"]["conditional_y_branch_shots"] == {"I": 500, "X": 501}
        assert meta["figure_file"] is None
        data = np.loadtxt(out / "echo_twirl.csv", delimiter=",", skiprows=1)
        assert data.shape == (101, 13)
        assert np.allclose(data[:, 0], np.linspace(0, 1 / (2 * params["T"]), 101))


def test_csv_detuning_labels_are_clean():
    """Scans at other T must not leak binary rounding (124.99999999999999)."""
    with TemporaryDirectory() as temp, redirect_stdout(StringIO()):
        et.main(["--T", "40e-6", "--no-figure", "--outdir", temp])
        rows = (Path(temp) / "echo_twirl.csv").read_text().splitlines()[1:]
    labels = [row.split(",")[0] for row in rows]
    assert labels[:3] == ["0.0", "125.0", "250.0"] and labels[-1] == "12500.0"


def test_closing_pulse_convention_matters():
    """A phase-reversed closing pulse cancels the pulse-area error to first
    order, so the residual at the null is smaller than with X.X."""
    same = et.transverse(et.signals(F0, P)[1])
    inverse = et.transverse(et.signals(F0, replace(P, closing=-1))[1])
    assert inverse < same / 3


def test_jitter_average_matches_analytic_ramsey():
    """Branch I at zero mean detuning: vis * exp(-(2 pi sigma T)^2 / 2)."""
    expected = P.vis * np.exp(-(2 * np.pi * P.jitter * P.T) ** 2 / 2)
    assert np.isclose(et.predict(0.0, "I", P)[0], expected, atol=1e-9)


def test_order_reversal_signal_scales_as_eps_delta_T2():
    """Follow-up proposal: with a transverse field eps the half-interval order
    matters.  Leading order: Z = +/- (2 pi)^2 eps delta T^2 / 4 for +X input."""
    v = np.array([1.0, 0.0, 0.0])
    for eps, delta in [(50.0, 50.0), (100.0, 50.0), (100.0, 100.0)]:
        plus_first = et.evolve(et.evolve(v, eps, +delta, P.T / 2), eps, -delta, P.T / 2)
        minus_first = et.evolve(et.evolve(v, eps, -delta, P.T / 2), eps, +delta, P.T / 2)
        leading = (2 * np.pi) ** 2 * eps * delta * P.T ** 2 / 4
        assert np.isclose(plus_first[2], -minus_first[2])
        assert np.isclose(plus_first[2], leading, rtol=5e-3)


if __name__ == "__main__":
    tests = [value for name, value in sorted(globals().items())
             if name.startswith("test_") and callable(value)]
    for test in tests:
        test()
        print("ok ", test.__name__)
    print(f"{len(tests)} checks passed")
