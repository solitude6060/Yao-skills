# Community synchronization — 0.8.0

Date: 2026-09-13. Plan: [community synchronization plan](2026-09-13-community-sync-plan.md).

## Source and scope

Community baseline: `ee0e5ae00e452a26d8b9972f3c4094094eff34f6` (0.3.0).
Source: Yao-Garyu research-toolkit 0.8.0, merged at
`38719bebcf2b5f67e7ce6dbdb14041a6b2495975`. The wait-what feature branch had
already been pushed; source PR #1 completed its main-branch integration on this date.
Source content was read from the local maintained checkout. Community readers do
not need access to the author's private source repository.

The package now distributes eight author-original skills, karpathy-guidelines and
the Taiwan wait-what adaptation. It removes the fourteen historical OMC copies:
`ralph`, `plan`, `deep-interview`, `deep-dive`, `learner`, `skillify`, `sciomc`,
`autoresearch`, `ralplan`, `ai-slop-cleaner`, `team`, `release`, `autopilot`,
`ultrawork`. Their attribution remains in NOTICE.md; upstream installations and
existing untracked runtime state are preserved.

## Community adaptations

| Area | Adaptation |
|---|---|
| Routing | Read the policy named in project instructions, with docs/MODEL_ROUTING.md as an example default; no personal model/account table is distributed |
| Triple review | Require three independent contexts, family diversity or explicitly authorized overlap, immutable targets and observed-failure-specific fallbacks |
| Context management | Label pricing as illustrative, state the arithmetic assumptions and preserve authorization before stopping a process |
| First-principles cases | Omit private incidents; verify public examples against SEC, NASA/JPL and OpenSSL sources, correcting the inherited deployment description |
| Status reports | Report secret names and configuration status only; remove personal policy references |
| Wait-what | Preserve manual invocation, Codex explicit-only metadata, evidence limits and the complete upstream MIT notice |
| Documentation | Explain actual workflow and skill selection, use persistent installation paths, replace the outdated behavioral template and retain bilingual companions |
| Hook | Preserve executable bytes; document the optional hash-based self-review behavior and its limits |

README examples summarize inspected development records about isolated test
configuration, evidence-based rejection of a review false positive, and separately
tracked implementation and operator acceptance. Research guidance follows the
current evidence-first policy and the projects' existing validity rules. These
examples report workflow practice; no private project identities, results, strategy,
account configuration or raw records are included. No claim is made that the named
skills were invoked in every historical case.

## Verification

Validation results and the independent instruction-scenario check are recorded
below before delivery. The deliverable set is the ten skill directories, both
READMEs, the two packaging manifests, NOTICE.md, bilingual template and hook
README. No executable feature or experimental-validity definition changed.

The bundled skill-creator quick validator has a narrower metadata allowlist than
the target runtime: it rejects existing argument-hint and disable-model-invocation
fields. Preserve those supported fields and check them with runtime-aware metadata
validation; do not modify the validator or weaken wait-what's invocation policy.

Checks establish packaging and instruction consistency. They do not measure
comprehension improvements, test every model, or prove installation on every host.


### Completed validation

- `claude plugin validate .claude-plugin/plugin.json`: passed without warnings.
- `claude plugin validate .`: marketplace passed without warnings.
- Source/community inventory: ten skill names match; all have Traditional Chinese companions.
- Runtime-aware YAML checks: name/description, wait-what manual-only frontmatter
  and `allow_implicit_invocation: false` passed; upstream wait-what license and
  Codex metadata bytes match the source.
- Local Markdown links, private absolute paths, README/template/hook heading
  alignment, unchanged hook bytes and `git diff --check`: passed.
- Generic skill-creator validator: three passed; seven rejected only existing
  runtime-supported metadata fields. Exact messages and 34 content hashes are in
  [the validation receipt](2026-09-13-community-validation.json).

### Independent instruction scenarios

A separate native verifier was requested as Research Medium, GPT-5.6 Sol, high.
The spawn surface recorded that selection; no separate backend identity was
exposed. This was a read-only instruction assessment, not a live agent-host test.

| Scenario | Observed assessment |
|---|---|
| A spelling fix with no routing or task-guidance file | PASS: direct authorized work can proceed |
| Re-explain a synthetic-only result with wait-what | PASS: preserve the evidence limit and ongoing authorized work; no new execution permission |
| One configured reviewer returns empty output with exit zero | PASS: no approval or unauthorized fallback; the required review remains incomplete |
| Installation prose mentions ralph and wait-what | PASS: update the prose without invoking either workflow |
| Illustrative 180k cached context calculation | PASS: 34,000 units under the stated weights; no authority to stop an unrelated process |

The verifier found a MEDIUM documentation gap: the release record referred to
scenario results before they had been appended. This section and the JSON receipt
resolve it. No skill behavior finding was reported. A remaining untranslated
personal-policy label in the status skill's Chinese companion was replaced with
"project management records" during final consistency validation; the reviewed
scenario inputs were unchanged. Records-only completion does not require another
instruction review.
