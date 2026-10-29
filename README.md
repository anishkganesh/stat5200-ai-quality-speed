# STAT 5200: AI Quality and Speed

This project asks whether access to ChatGPT helps professionals meet both a writing-quality benchmark and a time limit.

## Progress

HW4 covers the proposal and data preparation. The data have been downloaded, the participant dataset prepared, and descriptive statistics calculated in R. The replication and original analysis are planned next.

## Paper and data

Noy, Shakked, and Whitney Zhang. 2023. "Experimental evidence on the productivity effects of generative artificial intelligence." *Science* 381(6654):187–192. [Paper](https://doi.org/10.1126/science.adh2586) · [Public data and code](https://osf.io/xd7qw/).

The prepared dataset has one row per participant: 453 participants overall and 359 in the paper's main linear/convex incentive sample. Of those 359, 352 have both second-task time and quality recorded. Variable definitions, cleaning steps, and missingness are documented in the [codebook](data/codebook.md). The [source manifest](sources/manifest.json) records the download locations and checksums.

## Planned analyses

**Replication:** reproduce the completion-time result in Figure 1A. Compare changes in task time between the randomized groups using the authors' occupation-by-task-order and incentive controls, robust standard errors, and their standardization. The paired-time sample has 346 participants. Compare the estimate and standard error with the published result.

**Original project:** define success as an average evaluator score of at least 5 out of 7 on the second task, completed within 20 minutes. Compare success rates by randomized assignment using a linear probability model with robust standard errors. These benchmarks were chosen after inspecting the descriptive statistics; they are project choices, not an official passing standard.

Check how the conclusions depend on the chosen targets and the seven missing joint outcomes.

The study concerns professional writing tasks in 2023. Its results may not carry over directly to other AI tools or workplace settings.

## Files

- `code/`: data download, preparation, and R descriptive statistics.
- `data/raw/`: original downloads, stored locally and excluded from Git.
- `data/derived/participants.csv`: prepared variables used for analysis.
- `data/codebook.md`: variable and sample definitions.
- `results/`: generated statistics and calculation checks.
- `sources/`: download manifest and locally stored original code.
- `proposal.tex`: the one-page project proposal.

## Reproduce

From the repository root, using Python 3.12 and R:

```sh
python -m pip install -r requirements.txt
python code/fetch_sources.py
python code/build_data.py
Rscript code/descriptives.R
```

Data preparation follows the authors' July 21, 2023 cleaning revision. The downloader verifies input checksums. The prepared file omits participant identifiers and written responses. The R script exports summary statistics and the numbers used in the proposal to `results/tables/`.

To compile the proposal after running the scripts:

```sh
pdflatex proposal.tex
```

