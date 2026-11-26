# Contributors and AI assistance

## Author

**Ulrich Warring**, Physikalisches Institut, Albert-Ludwigs-Universität Freiburg. Author of the initial release (commit `3f2e268`, version 0.1.0): concept, summary, perspective and proposal, simulation and figure. The author is responsible for all content of this repository, including the parts changed with AI assistance described below.

Tool use for the initial release is not recorded in the repository. If any was involved, it should be added here by the author.

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

### Suggested disclosure

If material from this repository enters a manuscript, a statement along these lines covers the assistance recorded here:

> An AI system (Claude Fable 5.2, Anthropic) was used to review the simulation code and numerical statements, to check bibliographic references, and to prepare software metadata. The author verified the output and is responsible for the content.
