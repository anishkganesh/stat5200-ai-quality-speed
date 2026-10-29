# Planned replication: completion time

Target: Noy and Zhang (2023), Figure 1A, the main completion-time result. This is a focused replication of one main result, not an attempt to reproduce every analysis in the paper.

Use participants in the linear or convex incentive arms (`incentive_arm != "exact"`). The reconstructed main sample is 359, with 346 observations having both self-reported task times. Time is the sum of reported minutes spent brainstorming, drafting, editing, and other activities. Missing components produce a missing total, matching the authors' Stata code.

Planned steps:

1. Reproduce the pre/post mean-time comparison by randomized treatment assignment.
2. Estimate the authors' first-difference specification:
   `time2 - time1 ~ treatment + occupation * task_order + incentive_arm`.
   Occupation, task order, and incentive arm are categorical; task order is the `a_first` indicator. The occupation-by-order term includes both main effects and their interaction.
3. Use heteroskedasticity-robust standard errors, matching Stata's robust finite-sample correction. To reproduce the standardized label, divide the coefficient and standard error by the pre-task standard deviation in the relevant incentive sample, as in the source code.
4. Compare the result with the published figure and explain any remaining discrepancy.

The source specification appears in `4 - main text figures.do`, in the section for non-grade outcomes, and in the supplementary materials equation S.1. Treatment-effect estimation is pending. Grade regressions are outside this minimum replication target because the authors estimate them at the participant-evaluator level with evaluator fixed effects and participant-clustered standard errors.
