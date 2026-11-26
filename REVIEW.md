# Review record, version 0.1.0 → 0.2.0

**Date:** 26 November 2026 · **Reviewed:** commit `3f2e268` (four files) · **Reviewer:** Claude Fable 5.2 (Anthropic), working for the author; see [`CONTRIBUTORS.md`](CONTRIBUTORS.md)

## Outcome

The physics and the quoted numbers hold. Every number in the README and the perspective reproduces from the model, and the algebraic statements check out. One real mismatch between text and model was found (the closing pulse, item 1), one figure reference could not be confirmed (item 6), and the repository lacked what it needs to be reused and cited: a licence, citation metadata, the data behind the figure, and a byte-reproducible figure. These are fixed in 0.2.0. Seven points remain open for the author and are listed at the end.

## Method

The simulation was run under Python 3.13.18, NumPy 2.5.3 and Matplotlib 3.11.2. Quoted numbers were recomputed independently of the printed output. Sources were checked by web search against arXiv listings, publisher pages and institutional records; full texts were not read. Two sources could not be opened in the session and are marked as such.

## Findings

### Model and code

| # | Finding | Action |
|---|---|---|
| 1 | The text says the frame change is undone by the inverse operation. The model closes the frame with the same π pulse (X·X), so the two +1% pulse-area errors add. With a phase-reversed closing pulse (X·X⁻¹) they cancel to first order. The difference is visible in the quoted numbers: pooled contrast at the null 0.0025 against 0.0004; at 2.5 kHz echo X 0.941 against 0.948 and pooled X −0.933 against −0.943. | Convention stated in README and perspective, both sets of values given, `closing` parameter added. Default left unchanged. Which convention the experiment will use is for the author to decide. |
| 2 | The ideal-limit check rebound the module-level constants and restored them afterwards. This works only when the file runs as a script and breaks silently if the functions are imported. | Parameters are an explicit `Params` record passed to each function. |
| 3 | `N = 2000` was defined and never used. The projection-noise numbers in the perspective (0.474 ± 0.012) could not be regenerated from the script. | `shot_noise()` added; the script prints the numbers and a test pins them. |
| 4 | The figure carried a timestamp and random element identifiers and was written to the current working directory. | Timestamp removed, identifier salt fixed, output written next to the script. Two consecutive runs give identical bytes in the same environment. |
| 5 | The data behind the figure existed only as an SVG path. | `echo_twirl.csv` and `echo_twirl.json` added, including both twirl branches and the Z components. |
| 6 | No tests. | `test_echo_twirl.py`, eight checks. |

Confirmed without change:

- Table values 0.950 / 0.943, 0.949 / 0.002 and 0.941 / −0.933; transverse contrast 0.949 and 0.0025 at the null; difference 0.474 and standard error 0.012 for 2,000 shots per arm.
- Null at 1/(4T) = 1.25 kHz and sign reversal at 2.5 kHz for T = 200 µs.
- Pooling the {I, X} branches gives a dephasing channel with phase-flip probability sin²(φ/2), which multiplies the transverse coherence by cos φ.
- The jitter average: branch I at zero mean detuning equals 0.95·exp(−(2π·100 Hz·200 µs)²/2) = 0.94253. Eight Gauss–Hermite nodes already agree with 48 to 13 significant digits; 24 is ample.
- The follow-up proposal: for H± = ℏ(εX ± δZ)/2 the two half-interval orderings rotate +X into ±Z by εδT²/4 at leading order (ε, δ in angular frequency). Checked numerically with the model propagator to better than 0.5% for ε, δ up to 100 Hz.

Noted, not changed:

- The three sequences differ in length and pulse content: the echo and the X branch contain two 10 µs π pulses with the detuning on, the I branch none (220 µs against 200 µs). The perspective already asks for a time-matched reference.
- With finite pulses the pooled map is not a pure dephasing channel. The X branch ends with Z = −0.078 at the null and −0.186 at 2.5 kHz, the echo with +0.036 and +0.127 (same-pulse closing). An X-quadrature readout does not see this; a population measurement would.
- The README sentence on the registry's 114 µs Ramsey time does not say how it relates to the 200 µs used. The perspective gives the context.

### Text and references

| # | Finding | Action |
|---|---|---|
| 7 | “0.25% visibility” in the README and “0.002” in the perspective table describe the same point with different quantities (transverse magnitude and signed X). | Both named in both places. |
| 8 | Evert et al. was cited with “Fig. 7”. In the current arXiv version (v2, 4 October 2025) the QAOA comparison with randomized compiling is Fig. 4. Whether Fig. 7 was the numbering of v1 or of the journal version could not be checked. | Reference tied to arXiv v2, Fig. 4; journal DOI added. |
| 9 | Three links pointed to arXiv PDFs or a publisher landing page. | Replaced by arXiv abstract pages and DOIs; journal references added. |
| 10 | Biercuk et al. sits in the “Trapped ions” row beside single-ion work, but used ⁹Be⁺ crystals in a Penning trap. | System stated. |

### Source verification

“Confirmed” means the bibliographic record and the specific statement made about the source in this repository were both found consistent with the listing, abstract or excerpt.

| Source | Statement checked | Result |
|---|---|---|
| Hahn, Phys. Rev. 80, 580 (1950) | Spin echoes, 1950 | Confirmed |
| Haeberlen and Waugh, Phys. Rev. 175, 453 (1968) | Average-Hamiltonian treatment, 1968 | Bibliographic record confirmed; content from general knowledge |
| Werner, PRA 40, 4277 (1989) | Rotationally invariant bipartite states | Bibliographic record confirmed |
| Bennett et al., arXiv:quant-ph/9511027, PRL 76, 722 (1996) | November 1995; random bilateral rotation | Confirmed |
| Bennett, DiVincenzo, Smolin, Wootters, arXiv:quant-ph/9604024, PRA 54, 3824 (1996) | v1 dated 23 April 1996; calls the random bilateral rotation a “twirl” | Date of v1 confirmed. The term is confirmed in v2 (8 August 1996). **v1 itself was not opened**, so the statement that v1 already uses the noun rests on the author's reading. |
| Zanardi, Phys. Lett. A 258, 77 (1999) | Symmetrization of evolutions | Confirmed |
| Viola and Knill, PRL 94, 060502 (2005) | Random paths on a control group | Confirmed |
| Anwar et al., PRA 71, 032327 (2005) | Liquid-state NMR twirl to a Werner state using gradients | Confirmed |
| Andersen, Kaplan, Davidson, PRL 90, 023001 (2003) | Echo restores microwave Ramsey contrast, ⁸⁵Rb, optical trap | Confirmed |
| Walborn et al., PRA 65, 033818 (2002) | Interference recovered by a polarization measurement on the partner photon | Confirmed |
| Biercuk et al., PRA 79, 062324 (2009) | CPMG-type and Uhrig sequences under engineered noise, finite pulses | Sequences and engineered noise confirmed; system is ⁹Be⁺ in a Penning trap. The finite-pulse statement was not checked for this paper. |
| Akerman et al., PRL 109, 103601 (2012) | Single-ion scattering error reversed using the photon; fidelity above 85% conditional on detection | Confirmed |
| Clos et al., PRL 112, 113003 (2014) | Loss of ground-state coherence as the spectroscopy signal in ²⁵Mg⁺ | Confirmed. The published sequence itself contains a spin-echo pulse at half the delay. The reference to “Fig. 2” was not checked. |
| Wang et al., PRL 122, 200403 (2019) | Random phases of decoupling blocks suppress spurious responses; single NV | Confirmed |
| Ware et al., PRA 103, 042604 (2021) | Tomography shows coherent errors becoming stochastic under Pauli-frame randomization | Confirmed |
| Evert et al., arXiv:2403.07836 | Syncopated decoupling combined with randomized compiling on transmons, QAOA | Confirmed; figure number corrected (item 8) |
| Yi, Kim, Marvian, PRL 136, 010601 (2026) | Randomized protocol built around deterministic decoupling; proofs and numerics | Confirmed |
| Freiburg parameter registry (`parameters.yaml`) | 114 µs Ramsey time for the stretch-state transition; Raman carrier rates; 200 µs protocol; 1.789 GHz transition | **Not checked.** The page could not be opened in the session. The 1.789 GHz value agrees with the ²⁵Mg⁺ ground-state hyperfine splitting as generally quoted (about 1788.8 MHz). |

## FAIR status

| Principle | 0.1.0 | 0.2.0 | Still open |
|---|---|---|---|
| Findable | Repository description only | `CITATION.cff`, `codemeta.json`, keywords, versioned changelog | Repository is private; no DOI; no ORCID; no GitHub topics |
| Accessible | Private GitHub repository | Unchanged | Make public and archive a release |
| Interoperable | Markdown, Python, SVG | Data as CSV with a JSON record of units and columns; references as BibTeX with DOIs; metadata in CFF and CodeMeta | Registry is cited by a URL without a version |
| Reusable | No licence, no provenance | MIT (code) and CC BY 4.0 (text, figure, data); provenance and AI assistance recorded; tests; tested software versions stated | Licence choice to be confirmed by the author |

## Open points for the author

1. **Licences.** MIT for code and CC BY 4.0 for text, figure and data are a proposal. Confirm or replace before merging.
2. **Closing pulse.** Decide which convention the proposal means (item 1) and, if it is the inverse pulse, switch the default and the headline numbers.
3. **Registry statements.** Re-check the registry-based sentences, and cite the registry with a commit or date so the reference stays stable.
4. **First use of “twirl”.** Confirm against the v1 PDF of 23 April 1996, since the claim is specific to that version.
5. **Evert et al.** Confirm the figure number against the version you intend to cite.
6. **Identifier and visibility.** Make the repository public, add your ORCID to `CITATION.cff` and `codemeta.json`, tag `v0.2.0`, archive the release (for example through the Zenodo–GitHub link) and add the DOI to `CITATION.cff` and the README. Add GitHub topics matching the keywords.
7. **Tool use in 0.1.0.** If tools assisted the initial release, record it in `CONTRIBUTORS.md`.
