# From Hahn to Twirling · Start here

**At 1.25 kHz, sweeping the analysis phase gives almost no fringe in the pooled shots. Has the ion lost its coherence?** Prepare a spin along +X, allow 200 µs of free evolution and log one bit per shot. A fair coin selects ordinary Ramsey (I) or Ramsey bracketed by π pulses (X). Predict what happens to the fringe when you sort by the bit. Which analysis phase would you measure first? [Post a prediction or sketch in issue #2](https://github.com/uwarring82/from-hahn-to-twirling-in-60-seconds/issues/2).

<details>
<summary>Compare your prediction with the finite-pulse model</summary>

![Simulated transverse contrast and signed Y quadrature by branch and after pooling](echo_twirl.svg)

With ideal pulses, branch X is Ramsey at −δ. Both branches have the same X quadrature, cos(δT), and opposite Y quadratures, ±sin(δT). At the ideal null δT = π/2, sorting by the frame bit reveals opposite Y signals. The finite-pulse prediction for that measurement is **P(+Y | I) − P(+Y | X) = 0.941 ± 0.008**, with one projection-noise standard error for 1,000 shots per branch. Each branch has about 94% transverse contrast. Their equal-weight average has contrast 0.0025. The 0.474 probability difference between echo and pooled X is a control for refocusing.

</details>

[Simulation and parameter record](echo_twirl.json) · [Experiment and literature](echo_twirl_perspective.md) · [Source verification](REVIEW.md) · [Open work](https://github.com/uwarring82/from-hahn-to-twirling-in-60-seconds/issues)

## Reproduce or change the experiment

Run from the repository root in a Python environment. Each run writes the scan, parameters and figure to its own directory.

```sh
python -m pip install -r requirements.txt
python test_echo_twirl.py
python echo_twirl.py --outdir build/baseline
python echo_twirl.py --T 40e-6 --rabi 50000 --area 1.01 --jitter 100 --vis 0.95 --shots 2000 --closing -1 --outdir build/short
```

Time is in seconds and drive, detuning and rms jitter are in Hz. The code propagates H = h(drive·X + offset·Z)/2, so φ = 2πfT. A closing sign of +1 repeats the drive phase and −1 reverses it. The short run moves the nominal null to 6.25 kHz. At 50 kHz the two π pulses add 20 µs to the 40 µs of free evolution. The model predicts echo contrast 0.88, a pooled residual of 0.02, and the pooled minimum shifted to about 6.1 kHz. With `--rabi 200000` the echo returns to 0.947 and the pooled residual falls below 0.001. The models assume static detuning within a shot; the clock-state pulse and jitter values are illustrative.

## What would one run cost?

One trapped ion, microwave control with a π phase switch and programmable offset, a logged frame bit, standard preparation and fluorescence readout. The spectroscopy probe stays off. Three detunings × two arms (echo and twirl) × two analysis quadratures × 2,000 shots gives **24,000 shots**, plus calibration. Multiply by the measured shot-cycle time. Randomize a balanced branch schedule or record the actual counts from a fair coin. Quote the conditional uncertainty with those counts.

The [Freiburg registry](https://single-25mg-plus-d679f9.pages.uni-freiburg.de/content/experiment/parameters.yaml) assigns a no-line-trigger Ramsey time of 114 µs to the stretch-state microwave transition. If that transition is already calibrated, T = 40 µs is a possible pilot. Measure its probe-off Ramsey envelope, pulse area and echo first. Changing T alone in the script explores timing; it does not supply a stretch-state noise calibration.

## Choose a contribution

| Work | Starting point | Result to post |
|---|---|---|
| [Reproduce the Ramsey null and plot the two conditional fringes · #2](https://github.com/uwarring82/from-hahn-to-twirling-in-60-seconds/issues/2) | About an hour with Python and the [branch CSV](echo_twirl.csv) | Reconstruct the branch and pooled contrasts at 0, 1.25 and 2.50 kHz. Include the sample counts and an uncertainty on the signed Y statistic. |
| [Design the clock-qubit Ramsey control sequence · #3](https://github.com/uwarring82/from-hahn-to-twirling-in-60-seconds/issues/3) | An afternoon for a pulse table; apparatus access for calibration | Give each pulse phase and duration. Compare the bracketed X branch with a pulse-free reversal of the synthesizer offset. Physical X conjugation also flips unknown Z offsets; changing the synthesizer flips only the programmed one. Bound residual detuning and account for the extra pulse time. |
| [Test the noncommuting order-reversal prediction · #4](https://github.com/uwarring82/from-hahn-to-twirling-in-60-seconds/issues/4) | An afternoon with Bloch rotations and the [order-reversal test](test_echo_twirl.py) | Plot the Z signals for the two orders and find the range of T where the leading coefficient agrees with exact propagation to 5%. Include the pulse convention. |

For a change to code or text, link a pull request to the issue and give the command and inputs needed to reproduce it. Record contributions in [CONTRIBUTORS.md](CONTRIBUTORS.md) with the contributor’s preferred attribution. For a manuscript, discuss authorship with contributors based on the work actually carried into the paper. Readers with repository access can subscribe to one issue or use **Watch** for project updates.

## Three questions that lead to a number

- **Can we resolve a tilt after randomizing its sign?** For ideal short evolutions with a weak transverse drive, the two orders tilt +X toward ±Z by θ ≃ εδT²/4 (angular frequencies). The individual tilt is order T²; pooling yields a leading transverse contrast loss θ²/2, order T⁴. Determine the smallest T at which each effect is resolvable for a stated shot budget and calibrated pulse error.
- **How much does the bit tell us?** For ideal commuting dynamics at π/2, the +X output purity is 1 in either branch and 1/2 after pooling. The unitarity of the ideal pooled dephasing map is 1/3; this channel property averages over input directions. What extra preparations and shots would estimate it with a standard error of 0.05? [Wallman et al.](https://doi.org/10.1088/1367-2630/17/11/113020)
- **Where is the record?** Compare the classical frame bit, a logged detuning monitor and a detected scattered photon. Ion-only measurements cannot discriminate mechanisms that produce identical reduced channels. Choose an auxiliary record, specify a detection model and calculate the record efficiency needed for a stated precision. [Clos et al.](https://doi.org/10.1103/PhysRevLett.112.113003) · [Akerman et al.](https://doi.org/10.1103/PhysRevLett.109.103601) · [Uys et al.](https://doi.org/10.1103/PhysRevLett.105.200401)

Post a first estimate with your assumptions in the thread for [order reversal and tilt sensitivity (#4)](https://github.com/uwarring82/from-hahn-to-twirling-in-60-seconds/issues/4), [pooled-channel unitarity (#7)](https://github.com/uwarring82/from-hahn-to-twirling-in-60-seconds/issues/7), or [auxiliary-record efficiency (#8)](https://github.com/uwarring82/from-hahn-to-twirling-in-60-seconds/issues/8).

For journal club, follow the development from spin rephasing to bilateral twirling, randomized paths on a control group and randomized sensing sequences. [Hahn (1950)](https://doi.org/10.1103/PhysRev.80.580) · [Bennett et al. (1996), §3.1](https://arxiv.org/pdf/quant-ph/9604024v1#page=22) · [Viola and Knill (2005)](https://doi.org/10.1103/PhysRevLett.94.060502) · [Wang et al. (2019)](https://doi.org/10.1103/PhysRevLett.122.200403)
