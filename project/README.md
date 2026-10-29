# Proposed course extension: meeting quality and time targets

Question: Does randomized access to ChatGPT increase the probability that a professional writing task meets both a quality benchmark and a completion-time target?

## Outcome definition fixed before estimating the new outcome

Primary outcome: an indicator equal to 1 when the mean post-task overall grade is at least 5 out of 7 **and** reported post-task time is at most 20 minutes; otherwise 0. Both inputs must be observed. A missing input is not coded as failure.

The grade and time values are project benchmarks. The authors' rubric uses a 1-7 scale, with 4 intended as its approximate middle; it supplies example responses graded 2 and 6. It does not label 5 an official pass or an industry acceptance standard. The thresholds were selected after inspecting the original data and descriptive statistics, before constructing or estimating this joint outcome. This plan is not a preregistration.

Planned sensitivity definitions, evaluated alongside the primary result:

- Time limits of 15 and 25 minutes, retaining grade >= 5.
- Grade cutoffs of 4 and 6, retaining time <= 20 minutes.
- Excluding the one main-sample observation reporting zero post-task minutes.

## Sample and estimation plan

Use the 359 participants in the authors' linear/convex incentive arms. Assignment is randomized: 187 control and 172 treatment. Post-task time and grade are both observed for 352 participants (186 control and 166 treatment). A comparison by assigned group is an intention-to-treat comparison among these observed cases; interpretation for the full randomized main sample requires addressing the 7 missing outcomes.

Estimate the assigned-treatment effect on this binary joint outcome, with a simple linear probability model and robust standard errors. Occupation, task order, and incentive-arm controls may be included to match the experiment's structure. Report group counts and missingness before the estimate. Assess the possible impact of missing outcomes by showing bounds that assign success/failure to the 7 unobserved joint outcomes. Baseline-adjusted checks can use the 341 participants with both pre/post time and grade observed, with that additional sample restriction stated separately.

The purpose is to extend the paper's separate mean-time and mean-grade results to a practical joint target. No claim is made that the idea is new to the entire literature. Neither the joint indicator nor any treatment-effect model has been computed at this stage.
