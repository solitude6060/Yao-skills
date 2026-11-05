# Cohorts and exposure

A cohort's name does not say what it has been used for. Its exposure history does. Plan the roles before
the first result and keep the history with the cohort file.

## Roles

| Role | Used for | Rule |
|---|---|---|
| Development | Method design, variant comparison, debugging | Any use is allowed; results from it support no generalization claim |
| Selection or calibration | Choosing coefficients, checkpoints or settings on validation targets | Validation targets only (under leave-one-out these may belong to the reporting users); the selection rule is written before it runs |
| Reporting | Scoring the frozen configuration once on test targets | Reserved before the first result; never used to choose a variant; only its validation targets may select settings |
| Confirmation | Users added later to check that a result holds on users who shaped nothing | Drawn after the configuration is frozen; reported separately |

Write each cohort as a file of identifiers with a hash, the rule that drew it (for example a seeded random
draw) and its role. Give each cohort a neutral descriptive name at first use and keep the name throughout.

## Expanding a sample

- A larger sample contains the users already evaluated, so the earlier results remain a subset of the new
  ones and the study reports one population. Report the users that were added separately from the
  development users.
- When a baseline's official code selects on a sample of users (some sequential-recommender code samples a
  fixed number of users for validation on large datasets), draw that sample so it contains the evaluated
  users, and let every baseline read the same sample file.
- Expand in a ladder and stop at the size the decision needs; record which size each result used.

## Exposure history

Before calling a cohort held out or fresh, list every earlier contact with its targets:

| Contact | Example |
|---|---|
| Method design | Variants compared on these users' test targets |
| Selection | Coefficients or checkpoints chosen with their test targets (selection on their validation targets is not a contact) |
| Analysis | Mechanism analyses, case studies, error inspection that read their targets |
| Sibling projects | Another project that reused the same users or targets |
| Earlier protocols | Runs under a superseded split that used these events as targets |

A cohort with any contact is development data for the claims that contact could have shaped. State the
exposure in the paper's procedure description; it belongs on the must-keep disclosure list of
`paper-writing`.

## Repetitions

Name what varies across repetitions and what stays fixed: seeds vary; users, targets, candidates, model and
method stay fixed. A repetition that also changes the test set measures something else.

## Dataset pre-commitment

Before downloading datasets that will be added to a comparison, write a note naming them and stating that
every result enters the comparison, and record the note's hash. Remove a dataset later only for a reason that
holds independently of its results.

## Generic cases

- An early protocol allowed method selection on the first cohort's test targets. A later amendment
  reclassified that cohort as development data, and a holdout cohort plus a confirmation cohort were added.
- A follow-up project's cohort overlapped the users a sibling project had drawn for its own study; an
  exposure scan found the overlap, and those users were removed before any result.
- A "fresh" claim was withdrawn because every reused test target had already appeared in an earlier
  analysis.
- A larger sample was first drawn to exclude the users already evaluated, which would have made the
  reported population the sum of two separate samples; it was redrawn to contain them.
