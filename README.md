# From Hahn to Twirling in 60 Seconds

[Start here · predict the outcome, reproduce the baseline and explore open work](TEAM.md)

**What exactly are we averaging?** Start a spin along +X and let a static detuning give it a phase φ in time T. A Hahn echo reverses the sign of the detuning halfway through each shot. The spin accumulates +φ/2 and −φ/2 and refocuses. A channel twirl over {I, X} chooses one frame for the entire free interval and undoes the frame change before readout. The branches acquire +φ and −φ. Their mean transverse coherence is cos φ. At φ = π/2 both branches show full Ramsey fringes; the pooled fringe vanishes. Keep the frame bit and measure Y to see the opposite phases. At φ = π the pooled fringe returns with reversed sign.

![Predicted transverse contrast and Y quadrature for the echo, individual branches and pooled record](echo_twirl.svg)

### What the ion would measure

For T = 200 µs the nominal null is at 1.25 kHz. The predicted branch-resolved signal is **P(+Y &#124; I) − P(+Y &#124; X) = 0.941 ± 0.008** (1,000 shots per branch, one projection-noise standard error). The branch Y quadratures are +0.943 and −0.939. Each branch retains about 94% transverse contrast, yet their equal-weight mixture has contrast 0.0025. In an ideal detuning experiment the branches have identical X, so an X zero crossing alone also occurs in ordinary Ramsey. The echo retains contrast 0.9493. These are model predictions. The 50 kHz microwave Rabi frequency, +1% pulse amplitude error, 100 Hz rms shot-static jitter and 95% base visibility are illustrative. The model closes each frame with the same π pulse, so pulse-area errors add; reversing the closing pulse phase reverses its drive error, leaves its detuning term unchanged and lowers the pooled residual to 0.04%. The Freiburg registry assigns the 114 µs Ramsey time to the stretch-state microwave transition. The spectroscopy laser is off in the proposed comparison. In the published experiment it was the loss of coherence through scattering that supplied the optical signal. [Freiburg parameters](https://single-25mg-plus-d679f9.pages.uni-freiburg.de/content/experiment/parameters.yaml) · [Clos et al., PRL 112, 113003 (2014), Fig. 2](https://doi.org/10.1103/PhysRevLett.112.113003).

### Three meanings of averaging

| Object | Physical implementation | What survives |
|---|---|---|
| Hamiltonian | Evolve successively in two toggling frames | At leading order, terms invariant under X conjugation. Refocusing of static Z detuning is exact. |
| Channel | Apply a randomly conjugated process and pool the outputs | The group-invariant part of the process. Here this is a dephasing channel with phase-flip probability sin²(φ/2). |
| State | Apply a random group element to the prepared state and average | The invariant components of the state. A bilateral rotation preserves singlet weight. |

An ensemble can implement a state twirl by spatial averaging in one acquisition. The distinction is between composing evolutions and averaging outcomes over an unresolved label. [Anwar et al., PRA 71, 032327 (2005)](https://doi.org/10.1103/PhysRevA.71.032327).

### Where the word came from

Hahn demonstrated spin echoes in 1950. Haeberlen and Waugh described cyclic control with average-Hamiltonian theory in 1968. In November 1995 Bennett and colleagues described random bilateral rotations for entanglement purification. The earliest explicit use of the technical noun **twirl** verified in this review is the first version of Bennett, DiVincenzo, Smolin and Wootters, dated **23 April 1996**. Oral coinage and the first appearance of the exact phrase “quantum twirl” remain undetermined. [Hahn](https://doi.org/10.1103/PhysRev.80.580) · [Haeberlen and Waugh](https://doi.org/10.1103/PhysRev.175.453) · [November 1995 preprint](https://arxiv.org/abs/quant-ph/9511027), published as [PRL 76, 722 (1996)](https://doi.org/10.1103/PhysRevLett.76.722) · [April 1996 preprint, v1](https://arxiv.org/pdf/quant-ph/9604024v1#page=22), published as [PRA 54, 3824 (1996)](https://doi.org/10.1103/PhysRevA.54.3824).

### What others have demonstrated

Single-NV sensing showed that randomizing decoupling-block phases suppresses spurious spectral lines. Superconducting transmons have combined dynamical decoupling and randomized compiling in one circuit. A single-ion photon-scattering experiment showed that recovering information from the photon can enable conditional spin correction. [Wang et al., PRL 122, 200403 (2019)](https://doi.org/10.1103/PhysRevLett.122.200403) · [Evert et al., arXiv:2403.07836v2, Fig. 7](https://arxiv.org/html/2403.07836v2) · [Akerman et al. (2012)](https://doi.org/10.1103/PhysRevLett.109.103601).

### Run or extend the study

With Python 3.9 or later, NumPy and Matplotlib installed (`pip install -r requirements.txt`), run `python echo_twirl.py`. It prints five detuning points, checks the ideal limit, and regenerates the figure together with its data (`echo_twirl.csv`) and a metadata record (`echo_twirl.json`). `python -m pytest` checks every number quoted here against the model. The [perspective and experimental proposal](echo_twirl_perspective.md) gives the source-by-source platform comparison, readout statistics, and a follow-up test: add a transverse field and reverse the order of the two noncommuting evolutions. The order-sensitive signal is a prediction for a future experiment.

### Files

| File | Content |
|---|---|
| `README.md` | The 60-second summary |
| [TEAM.md](TEAM.md) | Prediction exercise, reproducible commands and experimental tasks |
| `echo_twirl_perspective.md` | Perspective and experimental proposal (discussion draft) |
| `echo_twirl.py` | Finite-pulse Bloch model; regenerates the three files below |
| `echo_twirl.csv` | Predicted Bloch vectors versus detuning: echo, pooled twirl and both twirl branches |
| `echo_twirl.json` | Parameters with units, column definitions, derived numbers and software versions for the CSV |
| `echo_twirl.svg` | Figure drawn from the CSV; title, creator and licence are embedded |
| `test_echo_twirl.py` | Checks of the ideal limit, the quoted numbers and the order-reversal scaling |
| `references.bib` | All cited sources with DOIs or arXiv identifiers |
| `CITATION.cff`, `codemeta.json` | Citation and software metadata |
| `CHANGELOG.md`, `CONTRIBUTORS.md`, `REVIEW.md` | Version history, contributions including AI assistance, and the review record with the source-verification table |

All numbers are model predictions with illustrative parameters. The repository contains no measured data.

### Cite and reuse

Cite this work using [`CITATION.cff`](CITATION.cff) (GitHub: “Cite this repository”). No DOI has been minted yet; until an archived release exists, cite the repository URL with the version and commit.

Code (`*.py`) is released under the [MIT License](LICENSE). Text, figure and data (`*.md`, `*.svg`, `*.csv`, `*.json`, `*.bib`) are released under [CC BY 4.0](LICENSE-CC-BY-4.0.txt). Contributions and the use of AI assistance are recorded in [`CONTRIBUTORS.md`](CONTRIBUTORS.md).
