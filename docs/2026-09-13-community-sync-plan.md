# Community release synchronization plan

## Outcome and sources

Update the public community edition from Yao-Garyu research-toolkit 0.8.0,
including the Taiwan wait-what adaptation, and document the author's development
workflow using verified recent project records. Yao-Garyu remains the source of
the personal workflow; this edition provides portable instructions and examples.

Source baseline: Yao-Garyu `66d32ad13410e534370c95f156f84a5e41a3fd9f` plus
the pushed wait-what branch `e7385d253e2befa6553508a9e34bc88a0dbe620e`.
Community baseline: `ee0e5ae00e452a26d8b9972f3c4094094eff34f6`.
Both origin refs were fetched on 2026-09-13. The wait-what branch exists remotely;
its earlier delivery stopped before pull-request creation. Finish that integration
through a pull request before recording the final source revision here.

## Scope and decisions

- Align the shipped inventory: eight author-original skills, karpathy-guidelines,
  and wait-what. Remove the fourteen vendored OMC skills, following source 0.7.0;
  direct users to their upstream distribution and preserve historical attribution.
- Copy the current bilingual skills and required supporting resources. Preserve
  licenses, evidence gates and wait-what's explicit invocation metadata.
- Adapt personal absolute paths, private incidents and account/model assumptions
  to documented local policy files and anonymous examples. Do not publish private
  project records, credentials, personal runtime backups or model-routing tables.
- Refresh both READMEs, plugin metadata, attribution and the behavioral template.
  Explain direct execution, durable plans, regression tests, bounded delegation,
  independent review, project memory, minimal research evidence and skill selection.
- Preserve the existing untracked `.omc/` directory. Do not install into or replace
  any user's runtime configuration as part of the community release.

## Sequence and acceptance

1. Commit this plan on the feature branch before content changes.
2. Verify and integrate the existing wait-what branch in its source repository.
3. Synchronize the community content and document any portability adaptations.
4. Check skill inventory, metadata, translation companions, local links, attribution,
   private-path leakage, explicit invocation, and `git diff --check`.
5. Update status.md, tracker.md and handover.md with actual delivery evidence;
   commit, push, and integrate through a pull request.

This release changes instruction documents and packaging metadata; it defines no
experimental metric or formal result and adds no executable feature. Documentation
validators apply; no new test framework or multi-model review ceremony is required.
If executable behavior changes become necessary, add a focused failing check and
apply the code review gate before implementation and merge.


## Reader-facing README revision

The user requested README text for people discovering the project. Rewrite both
languages around purpose, first use, workflow and skill selection. Remove release
audit narration, anonymization notes, internal routing/account details and runtime
maintenance recipes from the README. Keep necessary installation instructions and
links to focused guides. This is an editorial change; skills and executable files
remain unchanged. Check local links, bilingual coverage and whitespace, then deliver
through a documentation pull request.
