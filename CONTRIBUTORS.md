# Contributors and AI assistance

## Author

**Ulrich Warring**, Physikalisches Institut, Albert-Ludwigs-Universität Freiburg. Author of the initial release (commit `3f2e268`, version 0.1.0): scientific question, experimental context and direction. The author is responsible for all content of this repository, including the parts changed with AI assistance described below.

OpenAI Codex assisted the initial release by drafting the summary and perspective, preparing and running the numerical model, generating the figure, and locating primary references. For the follow-up on PR #1, Codex checked the versioned Bennett and Evert texts, the Freiburg registry and the Clos paper, reran the eight numerical checks, and edited the documentation. The study reports simulations.

The follow-up review in [issue #5](https://github.com/uwarring82/from-hahn-to-twirling-in-60-seconds/issues/5) identified conditional Y as the experimentally discriminating statistic and proposed the new figure. OpenAI Codex implemented the branch-resolved plot, parameter flags and regression checks, and drafted the corresponding changes to the team page and perspective. After the branch review, Codex updated the development version, regenerated the default outputs, and aligned the team page with the contribution issues.

## AI assistance

| | |
|---|---|
| Tool | Claude (Anthropic), model Claude Fable 5.2, identifier `claude-fable-5-2` |
| Date | 26 November 2026 |
| Mode | Agentic session on a separate branch, at the author's request to review the repository, fix the issues found, document the AI contribution and make the repository FAIR |
| Result | Version 0.2.0, delivered as a pull request for the author's review; see [`CHANGELOG.md`](CHANGELOG.md) |

Claude is a tool and not an author. It cannot take responsibility for the work, and it is therefore not listed in `CITATION.cff` or `codemeta.json`. Commits made in the session are authored as `Claude <noreply@anthropic.com>` and carry a `Co-Authored-By` trailer, so the provenance is visible in the history.

### What Claude did

- **Review.** Read all four files of version 0.1.0, ran the simulation, and recomputed every number quoted in the README and the perspective. Checked the algebra of the channel twirl (phase-flip probability sin²(φ/2)), the null position, the projection-noise estimate and the order-reversal scaling εδT²/4, the last one numerically with the model propagator.
- **Source verification.** Checked the cited sources by web search against arXiv listings, publisher pages and institutional records. The outcome for each source, including what could not be checked, is tabulated in [`REVIEW.md`](REVIEW.md).
- **Code.** Restructured `echo_twirl.py` (explicit parameter record, data and metadata export, reproducible figure, shot-noise estimate, closing-pulse option) without changing the default numerical results, and wrote `test_echo_twirl.py`.
- **Text.** Made the corrections listed under “Fixed” and “Changed” in the changelog. The argument, structure and wording of the summary and the perspective are otherwise the author's and were left as they were.
- **Metadata and documentation.** Wrote `CITATION.cff`, `codemeta.json`, `references.bib`, `requirements.txt`, `CHANGELOG.md`, `REVIEW.md`, this file and the new README sections, and added the licence files.

### What Claude did not do

- It did not open the Freiburg parameter registry or the first arXiv version of Bennett, DiVincenzo, Smolin and Wootters; statements resting on these two sources are the author's and were not re-verified.
- It did not read the full text of the cited papers. Claims were checked against abstracts, listings and the excerpts returned by web search.
- It did not choose the licences with any authority. MIT and CC BY 4.0 are a proposal that the author confirms or replaces by merging or editing.
- It produced no measured data, and the repository contains none.

### Follow-up after 0.2.0

- **Review of the entry page and issues #2–#4** ([issue #5](https://github.com/uwarring82/from-hahn-to-twirling-in-60-seconds/issues/5)). Found that both branches share the same X quadrature, so the X comparison quoted in 0.2.0 is a refocusing control, and that conditional Y carries the claim. The 0.2.0 review had confirmed the X numbers without noticing this. Proposed the branch-resolved figure, the run budget, the parameter flags and the three questions on the entry page, and checked the randomized-order contrast loss θ²/2 numerically.
- **Edits to pull request #6.** Reviewed the implementation by OpenAI Codex, ran it in a fresh environment, fixed the detuning labels of scans at other T, added a check for them, and added the finite-pulse numbers for the 40 µs example.
- **An error.** In 0.2.0 Claude changed the Evert et al. figure reference from Fig. 7 to Fig. 4 on the basis of an excerpt from an unversioned copy. The author restored Fig. 7 after checking the versioned full text.

### Suggested disclosure

If material from this repository enters a manuscript, a statement along these lines covers the assistance recorded here:

> OpenAI Codex assisted with drafting, simulation, figure generation and source verification. Claude (Anthropic) assisted with code review, tests, numerical checks and software metadata.
