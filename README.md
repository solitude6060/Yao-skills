# Yao-skills

English | [繁體中文](README.zh.md)

Reusable skills for working with coding agents. This is the community edition of
my Yao-Garyu toolkit, organized so you can adopt individual workflows in your own projects.

A skill is a set of instructions an agent can load for a particular task. These
skills grew out of my software development and research work: deciding how to
approach a task, checking assumptions, reviewing changes, explaining decisions, and
evaluating and writing up recommender-system research.
Start with the situation you recognize below, then [install for your agent](#installation).

## When I use each skill

### workflow-routing — decide how to organize the work

I use [workflow-routing](skills/workflow-routing/SKILL.md) before substantial
implementation or research work, when I need to decide whether to work directly,
write a plan first, delegate independent parts, or arrange a separate review.
It uses the project's model and tool policy to assign responsibilities.
A typo or a small, clear edit usually needs only a direct change and a check.

For example, a feature may touch an interface, its implementation and several
independent tests. Routing decides which work must happen in sequence, what can
run in parallel, who integrates the changes, and how completion will be checked.

> Use workflow-routing for this feature: identify the dependencies, implementation
> ownership and required checks before starting.

### first-principles — check the assumption behind the next action

I use [first-principles](skills/first-principles/SKILL.md) when a proposed fix or
important conclusion depends on something we have not verified. Typical moments
are repeated failures, a result that looks unexpectedly good, a review finding,
or a suggestion to lower a threshold or skip a check.

For example, if a test passes on one machine and fails on another, I first inspect
the actual inputs, environment and configuration it reads. That evidence determines
what needs fixing. In research, I check data identity and metric calculation before
interpreting a surprising score.

> Use first-principles to check why this test fails. Identify the assumption and
> the smallest observation that can confirm or reject it.

### recsys-evaluation — check what a recommender score means

I use [recsys-evaluation](skills/recsys-evaluation/SKILL.md) before designing, auditing or
writing up an offline recommender evaluation, and when a result changes sign between two
protocols. It derives the split, candidate set, preprocessing and baselines from the
research question instead of inheriting them, and states what each method may read.
A quick sanity check in a notebook does not need it.

For example, a frozen LLM ranker scores close to a trained sequential model on a sampled
candidate list. Before I write that down, I check the split and what each method sees, the
number of negatives against the random-ranking expectation, whether every method gets the
same candidates and history, and how failed queries are counted.

> Use recsys-evaluation on this evaluation plan: check the split, candidate protocol and
> baselines against the research question, and list what each method may read.

### paper-argument — turn results into an argument

I use [paper-argument](skills/paper-argument/SKILL.md) when results exist but the paper does
not yet explain why the method works: before an advisor meeting or a submission, or after a
reviewer asks what a component adds. It organizes motivation, highlights, method and proof,
and plans the mechanism evidence behind the proof.

For example, a method combines a few simple terms in a weighted sum and beats its baselines.
For each term I write what it represents, why it was chosen and why it works. Then I plan
the analyses that test each claim, such as removing a term, swapping a user's history for
another user's, or decomposing a score margin, and I write down before computing which
outcome would contradict the claim.

> Use paper-argument on this draft: write the four parts, an argument map from claim to
> evidence, and a plan for the analyses that explain why the method works.

### paper-writing — keep the body on one argument

I use [paper-writing](skills/paper-writing/SKILL.md) when I draft, cut or restructure a
paper's prose, tables and figures: a draft is over the page limit, reads like an experiment
log, or a dataset or result changed and the text has to follow. It keeps one question running
from the introduction to the conclusion, puts numbers in tables, and decides what stays in the
body and what moves to the appendix.

For example, a draft is two pages over the limit and three tables repeat the same numbers.
I map each paragraph and table to the question it serves, merge the tables, move settings and
secondary results to the appendix, and recheck every quantified claim against the result files.

> Use paper-writing on this draft: map each paragraph and table to the question it serves,
> propose what to cut, merge or move to the appendix, and list the quantified claims to re-verify.

### wait-what — explain the missing context

I explicitly invoke [wait-what](skills/wait-what/SKILL.md) when I cannot follow
an explanation: a term appeared without a definition, a conclusion skipped its
premise, or the answer got shorter than the reasoning requires.

This Taiwan adaptation rebuilds the explanation in Traditional Chinese, introduces
technical terms with their original names and short explanations, and uses a concrete
example before adding formal detail. It preserves evidence and uncertainty, and
then returns to the ongoing task. It applies to the current explanation.

> wait-what: Explain why these two results cannot be compared directly. Start with
> what each result measures and the assumption that makes the comparison valid.

Use the explicit command for your agent in the installation table below.
`workflow-routing`, `first-principles`, `recsys-evaluation`, `paper-argument` and
`paper-writing` can also be selected by the agent when the task calls for them;
`wait-what` requires my request.

## What I let the agent select

Once installed, I let the agent choose the following skills when their descriptions
match the work. Selection depends on the agent and the available tools.

| Skill | When it fits my workflow |
|---|---|
| [karpathy-guidelines](skills/karpathy-guidelines/SKILL.md) | During coding and review: make assumptions visible, keep changes focused, and define how to verify completion. |
| [triple-review](skills/triple-review/SKILL.md) | When a project requires independent multi-model review before merge. Verify findings against the actual change, then fix accepted issues. Ordinary documentation uses validators. |
| [worktree-hygiene](skills/worktree-hygiene/SKILL.md) | When creating, checking or retiring a Git worktree: track ownership and preserve unfinished work and results. |
| [context-hygiene](skills/context-hygiene/SKILL.md) | When a session grows long or work moves to another session: preserve the decisions, open questions and next action. |
| [tc-review](skills/tc-review/SKILL.md) | Before sending or publishing Traditional Chinese: check Taiwan vocabulary and technical terminology. |

Two more are driven by what I ask for:

| Skill | When I request it |
|---|---|
| [project-status-review](skills/project-status-review/SKILL.md) | I explicitly request a status review to reconcile completed work, blockers and the next decision against repository evidence. |
| [distilled-caveman-lite-accuracy](skills/distilled-caveman-lite-accuracy/SKILL.md) | I want a shorter answer while retaining necessary conditions, identifiers and uncertainty. |

## How this fits my development workflow

I start by reading the project specification and its current state. For substantial
work, I record the scope and acceptance checks, then use routing if the work needs
coordination. Bug fixes start with a failing regression test; implementation stays
as small as the verified behavior allows. Changes go through the project's checks
and review requirements before a pull request is merged.

For research, I aim for the smallest valid experiment on real data that can change
the decision to continue, adjust or stop. I inspect that result before expanding
the implementation or experiment matrix. First-principles becomes useful whenever
an assumption starts determining what we build or claim. For a recommender evaluation,
recsys-evaluation checks the protocol first; once results exist, paper-argument organizes
the case for why the method works and paper-writing fits that argument into the page limit.

At milestones, I keep `status.md` for current state and evidence, `tracker.md` for
remaining work, and `handover.md` for where the next session should resume.
`wait-what` is available at any point when I need the reasoning explained again.

## Other skills I pair with these

| Companion | How I use it |
|---|---|
| [ponytail](https://github.com/DietrichGebert/ponytail) | During implementation and review, favor existing code, standard libraries and native features; question unnecessary abstractions and keep the solution small. |
| [i-have-adhd](https://github.com/ayghri/i-have-adhd) | Put the next action first, break work into manageable steps, and make the current state easy to follow. |

These are separate projects with their own installation instructions. When a concise
reply leaves out context I need, I use `wait-what` to expand that explanation.

## Installation

### Install a coding agent

Choose the agent you use. These terminal commands are for macOS or Linux; the linked
official guides cover prerequisites, sign-in and other supported platforms.
Pi's npm command requires Node.js and npm. Cursor's command installs its terminal agent.

| Agent and official guide | Install command | Start |
|---|---|---|
| [Claude Code](https://code.claude.com/docs/en/setup) | `curl -fsSL https://claude.ai/install.sh \| bash` | `claude` |
| [Codex](https://learn.chatgpt.com/docs/codex/cli) | `curl -fsSL https://chatgpt.com/codex/install.sh \| sh` | `codex` |
| [Grok Build](https://docs.x.ai/build/overview) | `curl -fsSL https://x.ai/cli/install.sh \| bash` | `grok` |
| [Cursor](https://prod.cursor.com/docs/cli/installation) | `curl https://cursor.com/install -fsS \| bash` | `agent` |
| [Pi Agent](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/quickstart.md) | `npm install -g --ignore-scripts @earendil-works/pi-coding-agent` | `pi` |

### Add the skills to Claude Code

Run these inside Claude Code:

```text
/plugin marketplace add solitude6060/Yao-skills
/plugin install yao-skills@yao-skills
```

Run `/reload-plugins` or start a new session. Invoke a skill as
`/yao-skills:wait-what`, `/yao-skills:workflow-routing` or
`/yao-skills:first-principles`. See the [plugin guide](https://code.claude.com/docs/en/discover-plugins).

### Add the skills to Codex, Grok Build, Cursor or Pi Agent

All four read local user skills from `~/.agents/skills`. With Git installed, run
this once to make the collection available to those agents on this machine:

```bash
mkdir -p "$HOME/Research" "$HOME/.agents/skills"
git clone https://github.com/solitude6060/Yao-skills.git "$HOME/Research/Yao-skills"

for skill in "$HOME/Research/Yao-skills/skills"/*; do
  destination="$HOME/.agents/skills/${skill##*/}"
  if [ ! -e "$destination" ] && [ ! -L "$destination" ]; then
    ln -s "$skill" "$destination"
  fi
done
```

If you already have the checkout, skip the clone command. Existing skill entries
are kept. To install only selected skills, link those folders instead of running
the loop. Start a new agent session, then select the skill:

| Agent and skill guide | Explicit invocation example |
|---|---|
| [Codex](https://learn.chatgpt.com/docs/build-skills) | `$wait-what`; browse with `/skills`. |
| [Grok Build](https://docs.x.ai/build/features/skills-plugins-marketplaces) | `/wait-what`; browse with `/skills`. |
| [Cursor](https://prod.cursor.com/docs/skills) | Type `/` in Agent chat and select `wait-what`. |
| [Pi Agent](https://github.com/badlogic/pi-mono/blob/main/packages/coding-agent/docs/skills.md) | `/skill:wait-what`. |

Use the same syntax with any other skill, such as `workflow-routing`,
`first-principles` or `recsys-evaluation`. Cursor's shared
user directory applies to local sessions; remote agents need skills installed in
their own environment.

### Update

For the Claude Code plugin, refresh the marketplace and update through `/plugin`.
For the linked checkout:

```bash
git -C "$HOME/Research/Yao-skills" pull --ff-only
```

The links follow the updated files. Start a new session if changes have not appeared.

## Further reading

- [All skills](skills): instructions and references for each workflow.
- [Project instruction template](templates/CLAUDE.md): a starting point to adapt to your project.
- [Optional Traditional Chinese quality hook](hooks/tc-quality-hook/README.md): Claude Code integration.

## License

MIT. See [LICENSE](LICENSE) and [NOTICE.md](NOTICE.md) for authorship and upstream attribution.
