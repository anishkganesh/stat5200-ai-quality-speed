# STAT 5200: AI Quality and Speed

This course project asks whether access to ChatGPT helps people finish professional writing tasks quickly while reaching a chosen quality benchmark. It uses the public experiment by Shakked Noy and Whitney Zhang (2023).

## Current stage

The original data are available locally, the published final sample of 453 participants has been reconstructed, and descriptive statistics have been calculated in Python and R. The main flexible-time sample contains 359 participants; 352 have both post-task time and quality observed. No replication treatment effect or new project outcome has been estimated in this repository.

The [replication plan](replication/README.md) targets the paper's main completion-time result in Figure 1A. The [original-project plan](project/README.md) defines the proposed joint quality-and-speed outcome and sensitivity checks. The topic has been selected for the course proposal; instructor approval is not recorded here.

## Source

Noy, Shakked, and Whitney Zhang. 2023. "Experimental evidence on the productivity effects of generative artificial intelligence." *Science* 381(6654):187-192. https://doi.org/10.1126/science.adh2586

- Public replication package: https://osf.io/xd7qw/
- Author-hosted supplementary materials: https://shakkednoy.com/ChatGPT_SM.pdf
- [Pinned input sources](sources/manifest.json)
- [Data dictionary and sample definitions](data/README.md)

The authors' July 21, 2023 grade-cleaning revision is used. Original downloaded code is inspected as source material; none of it is executed. The new Python script implements the needed sample restrictions and grade aggregation. Source code and raw survey files remain in ignored local folders; the tracked derived file contains only eight numeric/categorical analysis fields, with no participant identifiers, essays, or free-text answers.

## Reproduce the descriptive preparation

Use Python 3.12 and R with its standard packages. Run these commands from the repository root:

```sh
python -m pip install -r requirements.txt
python code/fetch_sources.py
python code/build_data.py
Rscript code/descriptives.R
```

The source downloader verifies SHA-256 hashes and skips files already verified locally. It requires internet access for missing inputs. Raw files have already been placed in the ignored folders in this local checkout. `build_data.py` writes `data/derived/participants.csv`, sample counts, and independent Python descriptive checks. The R script writes `results/tables/descriptive_statistics.csv`, `results/tables/proposal_stats.tex`, and session information. The TeX macros are generated from the data for use in the proposal; do not manually copy numeric results. It accepts an optional input CSV path and output folder as its first two arguments.

## Scope and interpretation

The measured outcomes are self-reported task minutes and independent evaluator ratings. They describe this 2023 writing experiment. The project does not measure company-specific agent performance or cloud costs. The proposed thresholds were chosen for this course analysis after reviewing the dataset and its descriptive statistics; they are not a preregistration or validated workplace acceptance standard. Missing outcomes and a reported zero time will receive explicit sensitivity checks before causal conclusions are drawn.

## Repository organization

- `code/`: source retrieval, data preparation, and R descriptives.
- `sources/`: source URLs, hashes, and provenance notes.
- `data/derived/`: participant-level analysis fields; `data/README.md` defines them.
- `results/`: descriptive statistics, sample flow, and verification records.
- `replication/`: planned replication of Figure 1A.
- `project/`: the original course extension and planned checks.

Repository: https://github.com/anishkganesh/stat5200-ai-quality-speed (private). Provide the instructor/TA access for assessment. The proposal source is in project/proposal.tex and directly includes the R-generated macros. From the repository root, compile it with: pdflatex -output-directory=project project/proposal.tex.
