# Changelog

All notable changes to this repository are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and versions follow [Semantic Versioning](https://semver.org/).

## [0.2.0] – 2026-11-26

Review and FAIR pass. Details, evidence and open items are in [`REVIEW.md`](REVIEW.md); who did what is in [`CONTRIBUTORS.md`](CONTRIBUTORS.md).

### Added

- `echo_twirl.csv` and `echo_twirl.json`: the figure data (echo, pooled twirl and both twirl branches, all three Bloch components) with parameters, units, column definitions, derived numbers and software versions.
- `test_echo_twirl.py`: checks of the ideal limit, every number quoted in the text, the analytic jitter average, the branch-resolved fringes and the order-reversal scaling εδT²/4.
- `CITATION.cff`, `codemeta.json`, `references.bib`, `requirements.txt`, `LICENSE` (MIT, code), `LICENSE-CC-BY-4.0.txt` (text, figure, data), `CONTRIBUTORS.md`, `REVIEW.md`, `CHANGELOG.md`, `.gitignore`.
- README sections listing the files, how to cite, and the licences.

### Changed

- `echo_twirl.py`: parameters moved into an explicit `Params` record passed to every function (the ideal-limit check no longer rebinds module globals); outputs are written next to the script or to `--outdir`; the projection-noise estimate quoted in the perspective is now computed by the script (the shot number was defined but unused); a `closing` parameter selects whether the frame is closed with the same π pulse or a phase-reversed one. Default numerical results are unchanged.
- `echo_twirl.svg`: regenerated without a timestamp and with fixed element identifiers, so identical inputs give identical bytes; title, description, creator and licence are embedded.
- Links to arXiv PDFs and a publisher landing page replaced by arXiv abstract pages and DOIs; journal references added for the two 1996 Bennett et al. papers, Wang et al. and Yi et al.

### Fixed

- The text described the closing operation as the inverse of the opening one, while the model applies the same π pulse twice, so the two pulse-area errors add. The text now states the convention and gives the values for both.
- “Visibility” (0.25%) and the tabulated signed X quadrature (0.002) at the null referred to different quantities without saying so; both are now named.
- Evert et al.: the figure reference is now tied to a specific arXiv version (v2, Fig. 4); the previous “Fig. 7” could not be confirmed.
- Biercuk et al.: the system (⁹Be⁺ crystals in a Penning trap) is now stated, since the row sits beside single-ion work.

## [0.1.0] – 2026-11-26

Initial release (commit `3f2e268`): 60-second summary, perspective and experimental proposal, simulation script and figure.
