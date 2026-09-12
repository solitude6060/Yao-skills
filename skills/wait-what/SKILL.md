---
name: wait-what
description: Use when the user explicitly invokes wait-what to re-explain confusing content for Taiwanese researchers and engineers, restoring missing context and precise terminology.
disable-model-invocation: true
license: MIT
---

# Wait What

The explanation was unclear. Re-explain the relevant discussion from its question
and missing premise, going back further than the last message when needed.
Apply this to the current explanation only; preserve the ongoing task and other
session preferences. Discussing or installing this skill does not activate it.

Write in Traditional Chinese with Taiwan vocabulary unless the user requests
another language. Assume a capable colleague who lacks this specific context.
State the answer, supply the necessary background, then explain the mechanism and
practical consequence. Use a concrete project example before formulas or internal
identifiers. Keep natural, complete sentences; expand as needed for understanding.

Use the project's established terms from CONTEXT.md; follow CONTEXT-MAP.md when
multiple contexts exist. If absent, use available project documents and standard
terminology without creating files. On first use, pair each technical term in its
original language with a short Chinese explanation. Explain acronyms and internal
codes; preserve exact commands, identifiers, paths, numbers and units. Avoid
invented terms, metaphor, personification and unexplained shorthand.

For research, connect the question, data, method, observed result and supported
claim. Distinguish observations, inference and unknowns; retain sources, comparison
conditions, uncertainty and claim limits. For engineering, connect the symptom or
requirement, relevant input, mechanism, proposed change and verification; retain
preconditions and risks. Include only the parts relevant to the explanation.
Never invent evidence or a cause to make the account sound complete. If the earlier
answer was wrong, identify and correct it explicitly.

Existing ADHD or brevity modes may organize the response, but must not remove the
premises needed to understand it. Do not impose a word limit or force an action
before its rationale. If invoked again, change the explanation's structure or
example. Ask one focused question only if the missing context cannot be recovered.
Re-explanation alone authorizes no edits, commands, experiments or new workflow.

Adapted for the Yao-skills community edition from [Matt Pocock's wait-what](https://github.com/mattpocock/skills/tree/main/skills/productivity/wait-what).
Upstream copyright and permission notice: [LICENSE](LICENSE).
