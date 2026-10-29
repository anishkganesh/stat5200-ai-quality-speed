# Data dictionary and sample definitions

`derived/participants.csv` has one row per retained participant, 453 rows and 8 fields. Participant and evaluator identifiers, survey dates, essays, and free-text answers are omitted. The full sample includes 94 exact-time participants; the main flexible-time sample contains 359 participants in the linear and convex arms.

| Field | Definition | Values / units |
|---|---|---|
| `treatment` | Randomized assignment to ChatGPT access | 0 = control, 1 = treatment |
| `a_first` | Randomized order of the occupation's two tasks | 1 = task A first, 0 = task B first |
| `occupation` | Occupational task category | manager; grant writer; consultant; data analyst; marketer; HR professional |
| `incentive_arm` | Experimental payment/time condition | linear; convex; exact |
| `time1` | Self-reported time on the first, pre-treatment task | minutes; sum of brainstorming, drafting, editing and other time |
| `time2` | Self-reported time on the second, post-treatment task | minutes; same construction |
| `overall1` | Mean retained-evaluator overall score for the first task | 1-7; mapped from task A/B using `a_first` |
| `overall2` | Mean retained-evaluator overall score for the second task | 1-7; mapped from task A/B using `a_first` |

Blank CSV entries mean missing. A reported zero is retained as zero. In particular, one main-sample participant reports zero post-task minutes; its exclusion is a planned sensitivity check, not an automatic data change. A time total is missing if any of its four components is missing, matching Stata's arithmetic behavior.

## Restrictions and grading

The source survey export has 786 rows. The authors' sequential restrictions leave: 539 after excluding unfinished surveys; 523 after excluding explicit nonconsent; 505 after retaining each participant's earliest response; 499 after manually flagged responses; 457 after submission-quality checks; and 453 after excluding participants who graded before completing the writing task. The resulting dataset contains unique participants.

Grade preparation follows the July 21, 2023 source revision: exclude retry submissions, evaluators who previously completed the writing task, missing overall grades, and 23 evaluators whose own-score-on-other-score reliability slope is below 0.1. The last calculation reproduces the implementation in the authors' code. Repeated participant-evaluator-essay rows are retained as in that code. Remaining overall scores are averaged within participant and task.

## Main-sample availability

| Requirement | Available participants |
|---|---:|
| Assigned linear/convex sample | 359 |
| Pre-task time | 347 |
| Post-task time | 356 |
| Pre-task grade | 352 |
| Post-task grade | 353 |
| Both pre/post times | 346 |
| Both pre/post grades | 352 |
| Post-task time and grade | 352 |
| All four pre/post time and grade fields | 341 |

For the new post-task joint outcome, the observed sample is 186 control and 166 treatment. One control and six treatment participants lack a required post-task outcome. Availability counts are separate from sample exclusions; no additional participants are dropped from the 453-row stored dataset.

The published grade regression uses participant-evaluator observations and additional fixed effects. Participant mean grades support the descriptive summaries and proposed course extension. The planned replication instead targets the paper's completion-time result.


# Source provenance

The files in [sources/manifest.json](../sources/manifest.json) are pinned copies from the authors' public OSF node `xd7qw`, retrieved on October 29, 2026. Each entry records a relative destination, download URL, byte size, and SHA-256 digest.

`fullsurvey.csv` supplies assignment, task order, occupation, incentives, and times. The two grading workbooks supply the authors' manual submission-quality flags. `grading_long_complete.csv` supplies evaluator scores and dates. The July 21 grade-cleaning revision and main survey-cleaning source identify the authors' exclusions; the main-figure source documents the intended replication model.

The raw CSV uses non-UTF-8 text bytes; the preparation script reads it as Latin-1 and exports only selected numeric/categorical variables. Anonymized participant and grader hashes are used only internally for joins and are omitted from the tracked dataset.

The authors' updated readme specifically directs users to `3 - grade cleaning_jul21.do`. Relevant supplementary-material locations: sample restrictions and models, printed page 7; grading instructions and examples, printed pages 49-52. The rubric asks evaluators to use the full 1-7 scale and place roughly as many grades below 4 as above 4. It does not assign a validated acceptance label to a score of 5.

The scripts do not execute downloaded Stata or Python source code. Copyright and any reuse conditions for the original files remain with their authors and source repository. Raw data and third-party source copies are excluded from version control.
