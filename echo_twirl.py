"""Finite-pulse Bloch-vector model: Hahn echo versus {I, X} channel twirl.

A spin prepared along +X precesses under a static detuning for a total free
time T.  Three sequences are propagated with square pi pulses of finite
duration (the detuning stays on during the pulses):

    echo      free(T/2) - pi - free(T/2) - pi
    branch I  free(T)
    branch X  pi - free(T) - pi

The pooled channel twirl is the equal-weight mean of branches I and X.  Each
prediction is averaged over shot-static Gaussian detuning jitter by
Gauss-Hermite quadrature and scaled by a common visibility factor.

Units: frequencies in Hz (not rad/s), times in seconds.  Bloch-vector
components are dimensionless expectation values <X>, <Y>, <Z>.

Run ``python echo_twirl.py`` to print the reference points, check the ideal
limit and regenerate ``echo_twirl.csv``, ``echo_twirl.json`` and
``echo_twirl.svg`` next to this file.  Requires Python >= 3.9 and NumPy;
Matplotlib is needed only for the figure.

SPDX-License-Identifier: MIT
"""
from __future__ import annotations

import argparse
import csv
import json
import platform
from dataclasses import asdict, dataclass, replace
from pathlib import Path

import numpy as np
from numpy.polynomial.hermite import hermgauss

__version__ = "0.2.0"

MODES = ("echo", "I", "X")


@dataclass(frozen=True)
class Params:
    """Model parameters.  Defaults are illustrative, not calibrated values."""

    T: float = 200e-6      # total free precession, s
    rabi: float = 50e3     # nominal resonant Rabi frequency, Hz
    area: float = 1.01     # actual / nominal Rabi frequency (pulse-area error)
    jitter: float = 100.0  # shot-static Gaussian detuning rms, Hz
    vis: float = 0.95      # independent common contrast factor
    shots: int = 2000      # binary shots per quadrature per protocol
    closing: int = 1       # +1: the same pi pulse closes the frame (X.X);
                           # -1: a phase-reversed pulse closes it (X.X^-1)
    gh_nodes: int = 24     # Gauss-Hermite nodes for the jitter average


DEFAULT = Params()
IDEAL = Params(rabi=1e12, area=1.0, jitter=0.0, vis=1.0)

PARAM_UNITS = {
    "T": "s", "rabi": "Hz", "area": "1", "jitter": "Hz", "vis": "1",
    "shots": "1", "closing": "1", "gh_nodes": "1",
}


def evolve(v, drive, offset, duration):
    """Rotate Bloch vector ``v`` about the field (drive, 0, offset), in Hz."""
    field = np.array([drive, 0.0, offset])
    norm = np.linalg.norm(field)
    if norm == 0:
        return v
    axis = field / norm
    angle = 2 * np.pi * norm * duration
    return (v * np.cos(angle) + np.cross(axis, v) * np.sin(angle)
            + axis * np.dot(axis, v) * (1 - np.cos(angle)))


def sequence(offset, mode, p=DEFAULT):
    """Final Bloch vector for one shot at a fixed detuning ``offset`` (Hz)."""
    if mode not in MODES:
        raise ValueError(f"mode must be one of {MODES}, got {mode!r}")
    v = np.array([1.0, 0.0, 0.0])  # prepared +X; common readout in lab frame

    def pulse(v, sign=1):
        return evolve(v, sign * p.area * p.rabi, offset, 0.5 / p.rabi)

    def free(v, t):
        return evolve(v, 0.0, offset, t)

    if mode == "echo":
        # The closing pulse returns the toggling frame to the analysis frame.
        return pulse(free(pulse(free(v, p.T / 2)), p.T / 2), p.closing)
    if mode == "X":
        return pulse(free(pulse(v), p.T), p.closing)
    return free(v, p.T)


def predict(offset, mode, p=DEFAULT):
    """Jitter-averaged Bloch vector, scaled by the common visibility."""
    if p.jitter == 0:
        return p.vis * sequence(offset, mode, p)
    nodes, weights = hermgauss(p.gh_nodes)
    weights = weights / np.sqrt(np.pi)
    return p.vis * sum(w * sequence(offset + np.sqrt(2) * p.jitter * x, mode, p)
                       for x, w in zip(nodes, weights))


def branches(offset, p=DEFAULT):
    """Branch-resolved twirl predictions (frame bit kept): (I, X)."""
    return predict(offset, "I", p), predict(offset, "X", p)


def signals(offset, p=DEFAULT):
    """(echo, pooled twirl) Bloch vectors at detuning ``offset`` (Hz)."""
    branch_i, branch_x = branches(offset, p)
    return predict(offset, "echo", p), (branch_i + branch_x) / 2


def null_detuning(p=DEFAULT):
    """Detuning of the first ideal pooled-twirl zero, cos(2 pi f T) = 0, in Hz."""
    return 1 / (4 * p.T)


def transverse(v):
    """Magnitude of the transverse (X-Y) coherence of a Bloch vector."""
    return float(np.hypot(v[0], v[1]))


def shot_noise(offset, p=DEFAULT):
    """Echo-minus-twirl difference in P(+X outcome) and its projection-noise
    standard error for ``p.shots`` independent binary shots per arm."""
    echo, twirl = signals(offset, p)
    pe, pt = np.clip((np.array([echo[0], twirl[0]]) + 1) / 2, 0, 1)
    se = np.sqrt(pe * (1 - pe) / p.shots + pt * (1 - pt) / p.shots)
    return float(pe - pt), float(se)


def conditional_y(offset, p=DEFAULT):
    """P(+Y|I) minus P(+Y|X) and binomial SE for a balanced allocation."""
    i, x = branches(offset, p)
    pi, px = np.clip((np.array([i[1], x[1]]) + 1) / 2, 0, 1)
    n_i = p.shots // 2
    n_x = p.shots - n_i
    return float(pi - px), float(np.sqrt(pi * (1 - pi) / n_i + px * (1 - px) / n_x))


def check_ideal_limit(p=DEFAULT):
    """Zero-duration, error-free pulses: echo -> +X, twirl -> cos(2 pi f T)."""
    ideal = replace(IDEAL, T=p.T, rabi=IDEAL.rabi * DEFAULT.T / p.T)
    for f in np.linspace(0, 2 / p.T * 0.25, 5):
        echo, twirl = signals(f, ideal)
        expected = [1, 0, np.cos(2 * np.pi * f * p.T), 0]
        assert np.allclose([*echo[:2], *twirl[:2]], expected, atol=1e-7), f


def scan(offsets, p=DEFAULT):
    """Rows of (f, echo xyz, twirl xyz, branch-I xyz, branch-X xyz)."""
    rows = []
    for f in offsets:
        echo = predict(f, "echo", p)
        branch_i, branch_x = branches(f, p)
        rows.append([f, *echo, *(branch_i + branch_x) / 2, *branch_i, *branch_x])
    return np.array(rows)


COLUMNS = ["detuning_hz"] + [f"{name}_{axis}"
                             for name in ("echo", "twirl", "branch_i", "branch_x")
                             for axis in "xyz"]


def write_csv(path, table):
    with open(path, "w", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(COLUMNS)
        for row in table:
            writer.writerow([str(float(row[0]))]
                            + [f"{round(float(x), 6) + 0.0:.6f}" for x in row[1:]])


def write_metadata(path, p, versions):
    f0 = null_detuning(p)
    echo, twirl = signals(f0, p)
    diff, se = shot_noise(f0, p)
    y_diff, y_se = conditional_y(f0, p)
    meta = {
        "title": "Hahn echo versus {I, X} channel twirl: predicted Bloch vectors",
        "description": (
            "Finite-pulse Bloch-vector predictions for a spin prepared along +X "
            "under a static imposed detuning. Model output, not measured data; "
            "all parameters are illustrative."),
        "generated_by": {"script": "echo_twirl.py", "version": __version__,
                         **versions},
        "license": "CC-BY-4.0",
        "data_file": "echo_twirl.csv",
        "figure_file": "echo_twirl.svg" if "matplotlib" in versions else None,
        "parameters": {k: {"value": v, "unit": PARAM_UNITS[k]}
                       for k, v in asdict(p).items()},
        "columns": {
            "detuning_hz": "imposed static detuning, Hz",
            "echo_[xyz]": "Hahn echo Bloch vector",
            "twirl_[xyz]": "pooled channel twirl, mean of branches I and X",
            "branch_i_[xyz]": "twirl branch with frame bit I (plain Ramsey)",
            "branch_x_[xyz]": "twirl branch with frame bit X (pi - free - pi)",
        },
        "derived": {
            "null_detuning_hz": f0,
            "conditional_y_probability_difference": round(y_diff, 6),
            "conditional_y_standard_error": round(y_se, 6),
            "conditional_y_branch_shots": {"I": p.shots // 2, "X": p.shots - p.shots // 2},
            "echo_x_at_null": round(float(echo[0]), 6),
            "twirl_x_at_null": round(float(twirl[0]), 6),
            "echo_transverse_at_null": round(transverse(echo), 6),
            "twirl_transverse_at_null": round(transverse(twirl), 6),
            "echo_minus_twirl_probability_at_null": round(diff, 6),
            "projection_noise_standard_error": round(se, 6),
        },
    }
    with open(path, "w") as handle:
        json.dump(meta, handle, indent=2)
        handle.write("\n")


def write_figure(path, table, p=DEFAULT):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    plt.rcParams["svg.hashsalt"] = "echo_twirl"  # reproducible element ids
    plt.rcParams["font.family"] = "DejaVu Sans"
    fig, (contrast, y_axis) = plt.subplots(1, 2, figsize=(9.4, 4.0), layout="constrained")
    freq = table[:, 0] / 1000
    for column, label, color, style in [
        (1, "Hahn echo", "#29485a", "-"),
        (7, "Branch I", "#00866b", "--"),
        (10, "Branch X", "#965298", "-."),
        (4, "Pooled", "#cd5415", ":"),
    ]:
        x, y = table[:, column], table[:, column + 1]
        contrast.plot(freq, np.hypot(x, y), style, color=color, label=label, lw=2)
        y_axis.plot(freq, y, style, color=color, lw=2)
    for ax in (contrast, y_axis):
        ax.axvline(null_detuning(p) / 1000, color="0.65", ls=":", zorder=0)
        ax.set_xlabel("Detuning (kHz)")
    contrast.set(ylabel="Transverse contrast", ylim=(-0.045, 1.04))
    y_axis.set(ylabel="Signed Y quadrature", ylim=(-1.05, 1.05))
    contrast.legend(frameon=False, loc="lower left", fontsize=9)
    fig.savefig(path, metadata={
        "Date": None,
        "Title": "Conditional Ramsey fringes and the pooled record",
        "Description": ("Model predictions of transverse contrast and signed Y "
                        "for the Hahn echo, branches I and X, and their equal-weight pool."),
        "Creator": "Ulrich Warring",
        "Rights": "CC BY 4.0",
        "Source": "echo_twirl.py",
    })
    plt.close(fig)
    return matplotlib.__version__


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--outdir", type=Path, default=Path(__file__).parent,
                        help="directory for the CSV, JSON and SVG outputs")
    parser.add_argument("--no-figure", action="store_true",
                        help="skip the SVG (no Matplotlib needed)")
    parser.add_argument("--T", type=float, default=DEFAULT.T, help="free evolution time in seconds")
    parser.add_argument("--rabi", type=float, default=DEFAULT.rabi, help="resonant Rabi rate in Hz")
    parser.add_argument("--area", type=float, default=DEFAULT.area, help="actual/nominal pulse area")
    parser.add_argument("--jitter", type=float, default=DEFAULT.jitter, help="rms shot-static jitter in Hz")
    parser.add_argument("--vis", type=float, default=DEFAULT.vis, help="common visibility (0 to 1)")
    parser.add_argument("--shots", type=int, default=DEFAULT.shots, help="shots per arm per quadrature")
    parser.add_argument("--closing", type=int, choices=(-1, 1), default=DEFAULT.closing,
                        help="closing pulse drive sign (+1 same, -1 reversed)")
    args = parser.parse_args(argv)
    if not all(np.isfinite(v) for v in (args.T, args.rabi, args.area, args.jitter, args.vis)):
        parser.error("physical parameters must be finite")
    if args.T <= 0 or args.rabi <= 0 or args.area < 0 or args.jitter < 0:
        parser.error("T and rabi must be positive; area and jitter must be nonnegative")
    if not 0 <= args.vis <= 1 or args.shots < 2:
        parser.error("visibility must be in [0, 1] and shots must allow at least one per branch")
    p = Params(T=args.T, rabi=args.rabi, area=args.area, jitter=args.jitter,
               vis=args.vis, shots=args.shots, closing=args.closing)
    offsets = np.linspace(0, 2 * null_detuning(p), 101)
    table = scan(offsets, p)
    print("detuning_hz  echo_x  echo_y  twirl_x  twirl_y")
    for idx in (0, 25, 50, 75, 100):
        f, ex, ey, _, tx, ty = table[idx, :6]
        values = [round(float(x), 4) + 0.0 for x in (ex, ey, tx, ty)]
        print(f"{f:11.1f} {values[0]:7.4f} {values[1]:7.4f} "
              f"{values[2]:8.4f} {values[3]:8.4f}")

    check_ideal_limit(p)
    f0 = null_detuning(p)
    echo, twirl = signals(f0, p)
    diff, se = shot_noise(f0, p)
    y_diff, y_se = conditional_y(f0, p)
    print(f"P(+Y|I) - P(+Y|X): {y_diff:.3f} +/- {y_se:.3f} "
          f"({p.shots // 2} I shots, {p.shots - p.shots // 2} X shots)")
    print(f"null at {f0:.1f} Hz: transverse contrast echo {transverse(echo):.4f}, "
          f"pooled twirl {transverse(twirl):.4f}")
    print(f"echo - twirl in P(+X) at the null: {diff:.3f} +/- {se:.3f} "
          f"({p.shots} shots per arm)")
    inverse = replace(p, closing=-p.closing)
    print(f"with alternate closing sign {inverse.closing:+d}: pooled twirl contrast at the "
          f"null {transverse(signals(f0, inverse)[1]):.4f}")

    args.outdir.mkdir(parents=True, exist_ok=True)
    versions = {"python": platform.python_version(), "numpy": np.__version__}
    write_csv(args.outdir / "echo_twirl.csv", table)
    if not args.no_figure:
        versions["matplotlib"] = write_figure(args.outdir / "echo_twirl.svg", table, p)
    write_metadata(args.outdir / "echo_twirl.json", p, versions)


if __name__ == "__main__":
    main()
