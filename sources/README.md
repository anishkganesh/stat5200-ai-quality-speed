# Source provenance

The files in `manifest.json` are pinned copies from the authors' public OSF node `xd7qw`, retrieved on October 29, 2026. Each entry records a relative destination, download URL, byte size, and SHA-256 digest.

`fullsurvey.csv` supplies assignment, task order, occupation, incentives, and times. The two grading workbooks supply the authors' manual submission-quality flags. `grading_long_complete.csv` supplies evaluator scores and dates. The July 21 grade-cleaning revision and main survey-cleaning source identify the authors' exclusions; the main-figure source documents the intended replication model.

The raw CSV uses non-UTF-8 text bytes; the preparation script reads it as Latin-1 and exports only selected numeric/categorical variables. Anonymized participant and grader hashes are used only internally for joins and are omitted from the tracked dataset.

The authors' updated readme specifically directs users to `3 - grade cleaning_jul21.do`. Relevant supplementary-material locations: sample restrictions and models, printed page 7; grading instructions and examples, printed pages 49-52. The rubric asks evaluators to use the full 1-7 scale and place roughly as many grades below 4 as above 4. It does not assign a validated acceptance label to a score of 5.

The scripts do not execute downloaded Stata or Python source code. Copyright and any reuse conditions for the original files remain with their authors and source repository. Raw data and third-party source copies are excluded from version control.
