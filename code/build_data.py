"""Reconstruct the authors' sample and participant grades; calculate descriptives only.

Original code is read to identify its documented exclusions, never executed.
All downloaded inputs are checked against sources/manifest.json first.
"""
from pathlib import Path
import hashlib
import itertools
import json
import re

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / 'data/raw'
SOURCE = ROOT / 'sources/code'
OUT = ROOT / 'results'
DERIVED = ROOT / 'data/derived'
OUT.mkdir(exist_ok=True)
TABLES = OUT / 'tables'
TABLES.mkdir(exist_ok=True)
DERIVED.mkdir(parents=True, exist_ok=True)

manifest = json.loads((ROOT / 'sources/manifest.json').read_text(encoding='utf-8'))
for item in manifest['files']:
    path = (ROOT / item['path']).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError('Input path must remain inside this repository')
    if not path.exists():
        raise FileNotFoundError('Missing input; run code/fetch_sources.py: ' + item['path'])
    if hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
        raise ValueError('Input hash differs from pinned source: ' + item['path'])


def read_csv(name, columns=None):
    wanted = None if columns is None else lambda c: c.lower() in columns
    data = pd.read_csv(RAW / name, encoding='latin1', low_memory=False, usecols=wanted)
    data.columns = data.columns.str.lower()
    return data


def day_only(values):
    return pd.to_datetime(values.str[:10], format='%Y-%m-%d', errors='raise')


flow = []


def record(name, data, before=None):
    entry = {'step': name, 'rows': len(data),
             'unique_participants': int(data.prolific_pid.nunique())}
    if before is not None:
        entry['removed'] = before - len(data)
    flow.append(entry)


def exclude(data, mask, reason):
    kept = data.loc[~mask].copy()
    record(reason, kept, len(data))
    return kept


fields = ['prolific_pid', 'startdate', 'finished', 'consent', 'consent_exact',
          'treatment', 'a_first', 'occupation', 'incentive_arm']
fields += [f'time{task}_{part}' for task in (1, 2) for part in (4, 5, 6, 7)]
data = read_csv('fullsurvey.csv', fields)
record('Raw survey rows', data)
data = exclude(data, data.finished.eq(0), 'Exclude unfinished surveys')
data = exclude(data, data.consent.eq(2) | data.consent_exact.eq(2),
               'Exclude explicit nonconsent')

# Save task dates at the same stage as the source pipeline, before other exclusions.
task_dates = pd.DataFrame({'grader_id': data.prolific_pid,
                           'datetasked': day_only(data.startdate)})
task_dates = task_dates.groupby('grader_id', as_index=False).datetasked.min()
before = len(data)
data = data.sort_values(['prolific_pid', 'startdate'], kind='stable')
data = data.drop_duplicates('prolific_pid', keep='first').copy()
record('Retain earliest response per participant', data, before)

clean_source = (SOURCE / '2 - clean.do').read_text(encoding='utf-8')
flag_lines = [line for line in clean_source.splitlines()
              if line.startswith(('gen plagiarism', 'gen empty', 'gen gradedfirst',
                                  'replace multiplesurveys'))]
flagged = set(re.findall(r'prolific_pid=="([0-9a-f]+)"', '\n'.join(flag_lines)))
assert len(flagged) == 6, 'Unexpected source exclusion constants'
data = exclude(data, data.prolific_pid.isin(flagged), 'Authors manual exclusion flags')

quality_tables = []
for filename in ['grading.xlsx', 'grading_retry.xlsx']:
    quality = pd.read_excel(RAW / filename, usecols=['prolific_pid', 'qcheck'])
    quality['qcheck'] = quality.qcheck.replace(3, 1)
    quality = quality.groupby('prolific_pid', as_index=False).qcheck.agg(
        minqcheck='min', maxqcheck='max')
    quality = quality.loc[~quality.prolific_pid.isin(['', '1', '2', '3', '4'])]
    quality_tables.append(quality)
quality = pd.concat(quality_tables, ignore_index=True)
conflicts = quality.groupby('prolific_pid')[['minqcheck', 'maxqcheck']].nunique()
assert not conflicts.gt(1).any().any(), 'Conflicting quality-check files need review'
quality = quality.drop_duplicates('prolific_pid', keep='first')
data = data.merge(quality, on='prolific_pid', how='left', validate='1:1')
data = exclude(data, data.maxqcheck.gt(1) | data.minqcheck.lt(1),
               'Authors submission-quality exclusions')

grade_fields = ['grader_id', 'prolific_pid', 'startdate', 'essaynum', 'retry', 'overall']
grades = read_csv('grading_long_complete.csv', grade_fields)
grades['dategraded'] = day_only(grades.startdate)
first_grade = grades.groupby('grader_id', as_index=False).dategraded.min()
first_grade = first_grade.rename(columns={'grader_id': 'prolific_pid'})
data = data.merge(first_grade, on='prolific_pid', how='left', validate='1:1')
data['datetasked'] = day_only(data.startdate)
data = exclude(data, data.datetasked.gt(data.dategraded) & data.dategraded.notna(),
               'Exclude participants who graded before writing')
assert len(data) == 453 and data.prolific_pid.is_unique
assert data.treatment.isin([0, 1]).all() and data.a_first.isin([0, 1]).all()

for task in (1, 2):
    # Stata addition returns missing if any component is missing; pandas normally skips them.
    data[f'time{task}'] = data[[f'time{task}_{part}' for part in (4, 5, 6, 7)]].sum(
        axis=1, min_count=4)

# Reproduce the revised grade cleaning, including its own-on-other reliability slope.
grade_flow = []


def exclude_grades(mask, reason):
    global grades
    before = len(grades)
    grades = grades.loc[~mask].copy()
    grade_flow.append({'step': reason, 'remaining_rows': len(grades),
                       'removed_rows': before - len(grades)})


grade_source = (SOURCE / '3 - grade cleaning_jul21.do').read_text(encoding='utf-8')
test_line = next(line for line in grade_source.splitlines()
                 if line.startswith('drop if grader_id=='))
test_id = re.search(r'grader_id=="([0-9a-f]+)"', test_line).group(1)
exclude_grades(grades.grader_id.eq(test_id), 'Exclude author test grader')
exclude_grades(grades.retry.eq(1), 'Exclude retry-task grades')
grades = grades.merge(task_dates, on='grader_id', how='left', validate='m:1')
exclude_grades(grades.dategraded.gt(grades.datetasked) & grades.datetasked.notna(),
               'Exclude evaluators who previously completed writing task')
exclude_grades(grades.overall.isna(), 'Exclude missing overall ratings')
validation = grades.loc[~grades.prolific_pid.str.lower().eq('chatgpt')].copy()
assert validation.grader_id.str[:15].nunique() == validation.grader_id.nunique()
pairs = []
for _, essay in validation.sort_values(['prolific_pid', 'essaynum', 'grader_id'],
                                      kind='stable').groupby(['prolific_pid', 'essaynum']):
    entries = list(essay[['grader_id', 'overall']].itertuples(index=False, name=None))
    for (first_id, first_score), (second_id, second_score) in itertools.combinations(entries, 2):
        pairs.append((first_id, second_id, first_score, second_score))

slopes = {}
for grader in validation.grader_id.unique():
    own, other = [], []
    for first_id, second_id, first_score, second_score in pairs:
        if grader != first_id and grader != second_id:
            continue
        # These choices also reproduce the source's handling of repeated grader rows.
        own.append(first_score if grader == first_id else second_score)
        other.append(first_score if grader == second_id else second_score)
    x, y = np.asarray(other), np.asarray(own)
    if len(x) < 2 or np.var(x) == 0:
        raise ValueError('Undefined evaluator-reliability slope requires source review')
    slopes[grader] = float(np.cov(x, y, ddof=0)[0, 1] / np.var(x))
excluded_graders = {grader for grader, slope in slopes.items() if slope < 0.1}
assert len(excluded_graders) == 23, 'Evaluator exclusions differ from revised source'
exclude_grades(grades.grader_id.isin(excluded_graders), 'Exclude low-reliability evaluators')

mean_grades = grades.groupby(['prolific_pid', 'essaynum']).overall.mean().unstack('essaynum')
mean_grades = mean_grades.rename(columns={'A': 'overall_A', 'B': 'overall_B'})
data = data.merge(mean_grades.reset_index(), on='prolific_pid', how='left', validate='1:1')
data['overall1'] = np.where(data.a_first.eq(1), data.overall_A, data.overall_B)
data['overall2'] = np.where(data.a_first.eq(1), data.overall_B, data.overall_A)
for name in ['overall1', 'overall2']:
    assert data[name].dropna().between(1, 7).all()
for name in ['time1', 'time2']:
    assert data[name].dropna().ge(0).all()

kept_fields = ['treatment', 'a_first', 'occupation', 'incentive_arm',
               'time1', 'time2', 'overall1', 'overall2']
participants = data[kept_fields].copy()
participants.to_csv(DERIVED / 'participants.csv', index=False)
main = participants.loc[participants.incentive_arm.ne('exact')]
assert len(main) == 359
post_complete = main[['time2', 'overall2']].notna().all(axis=1)
summary = {
    'full_participants': len(participants),
    'full_assigned_counts': participants.treatment.value_counts().sort_index().astype(int).to_dict(),
    'main_participants': len(main),
    'main_assigned_counts': main.treatment.value_counts().sort_index().astype(int).to_dict(),
    'exact_time_participants': int(participants.incentive_arm.eq('exact').sum()),
    'main_pre_time_observed': int(main.time1.notna().sum()),
    'main_post_time_observed': int(main.time2.notna().sum()),
    'main_pre_grade_observed': int(main.overall1.notna().sum()),
    'main_post_grade_observed': int(main.overall2.notna().sum()),
    'main_complete_time_pair': int(main[['time1', 'time2']].notna().all(axis=1).sum()),
    'main_complete_grade_pair': int(main[['overall1', 'overall2']].notna().all(axis=1).sum()),
    'main_complete_post_time_grade': int(post_complete.sum()),
    'main_complete_post_assigned_counts': main.loc[post_complete].treatment.value_counts().sort_index().astype(int).to_dict(),
    'main_missing_post_assigned_counts': main.loc[~post_complete].treatment.value_counts().sort_index().astype(int).to_dict(),
    'main_complete_all_four': int(main[['time1','time2','overall1','overall2']].notna().all(axis=1).sum()),
    'main_reported_zero_post_time': int(main.time2.eq(0).sum()),
    'excluded_low_reliability_graders': len(excluded_graders),
    'grade_cleaning_flow': grade_flow,
    'joint_outcome_computed': False,
    'treatment_effect_models_estimated': False,
}
assert summary['main_complete_post_time_grade'] == 352
assert summary['main_complete_all_four'] == 341
pd.DataFrame(flow).to_csv(TABLES / 'sample_flow.csv', index=False)
(OUT / 'sample_summary.json').write_text(json.dumps(summary, indent=2) + '\n', encoding='utf-8')

rows = []
for sample_name, sample in [('all_clean', participants), ('main_linear_convex', main)]:
    for group_name, group in [('all', sample), ('control', sample.loc[sample.treatment.eq(0)]),
                              ('treatment', sample.loc[sample.treatment.eq(1)])]:
        for variable in ['time1', 'time2', 'overall1', 'overall2']:
            values = group[variable]
            rows.append({'sample': sample_name, 'group': group_name, 'variable': variable,
                         'group_n': len(group), 'nonmissing_n': int(values.notna().sum()),
                         'missing_n': int(values.isna().sum()), 'mean': values.mean(),
                         'sd': values.std(), 'min': values.min(), 'p25': values.quantile(.25),
                         'median': values.median(), 'p75': values.quantile(.75), 'max': values.max()})
pd.DataFrame(rows).to_csv(TABLES / 'descriptive_statistics_python.csv', index=False)
print('Prepared 453 participants; main sample 359; complete post-task time and grade 352.')
print('Descriptive preparation complete; no project outcome or treatment effect estimated.')
