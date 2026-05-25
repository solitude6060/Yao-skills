# tc-quality-hook

A Claude Code [PreToolUse hook](https://docs.anthropic.com/en/docs/claude-code/hooks) that forces the model to self-review Traditional Chinese text quality before presenting it to the user.

## Problem

When Claude Code outputs Traditional Chinese (繁體中文) in interactive UI elements like `AskUserQuestion`, three categories of text quality issues frequently appear:

1. **Simplified Chinese character leakage** — The model's training data is predominantly Simplified Chinese. Characters like 专 (should be 專), 设 (should be 設), 执 (should be 執) slip through even with strong system prompts.

2. **Hallucinated rare characters** — The model sometimes generates visually similar but semantically wrong characters. For example, 廩 (granary) or 裰 (to patch) appearing where 併入 (merge into) or 讓 (let) was intended.

3. **Mainland Chinese vocabulary** — Characters are technically Traditional but the phrasing follows Mainland conventions rather than Taiwan usage. For example, 用戶 instead of 使用者, 界面 instead of 介面, 調用 instead of 呼叫.

These issues are especially prevalent in tool call parameters (`AskUserQuestion` options, `TaskCreate` descriptions) because the model tends to relax attention when constructing JSON payloads rather than composing direct chat replies.

### Why not OpenCC or mapping tables?

- **OpenCC** produces false positives on ambiguous characters (回→迴, 台→臺) that are valid in both systems, and cannot detect vocabulary-level issues (用戶 vs 使用者) or hallucinated characters.
- **Mapping tables** can only catch a predefined set of known simplified characters. They miss hallucinated rare characters entirely and require ongoing maintenance.
- **LLM self-review** covers all three categories in a single pass — the same model that generated the text can evaluate whether it reads naturally to a Taiwan engineer.

## How it works

```
Claude generates AskUserQuestion with Chinese text
         │
         ▼
  ┌──────────────┐
  │ PreToolUse   │  Hook detects CJK characters in parameters
  │ hook fires   │  and blocks the tool call (exit 2)
  └──────┬───────┘
         │
         ▼
  ┌──────────────┐
  │ Claude sees  │  The blocked text is shown back to Claude
  │ the block    │  with a review checklist
  └──────┬───────┘
         │
         ▼
  ┌──────────────┐
  │ Claude self- │  Claude reviews for: simplified chars,
  │ reviews text │  hallucinated chars, mainland vocabulary,
  └──────┬───────┘  unnatural phrasing
         │
         ▼
  ┌──────────────┐
  │ Resubmit     │  Same content → hash match → allowed through
  │ (fixed or    │  Changed content → blocked once more for
  │  confirmed)  │  another review pass
  └──────────────┘
```

**Key design choice:** No automated character detection (no OpenCC, no mapping tables). The LLM itself performs the review. This catches all three issue categories — including vocabulary-level problems and hallucinated characters that no character mapping can detect.

**Hash tracking** prevents infinite loops: the first submission is always blocked for review; a resubmission with identical content passes through. Hashes are stored in `/tmp/.claude-tc-reviewed` and expire after 1 hour.

## Install

### 1. Copy the hook script

```bash
mkdir -p ~/.claude/hooks
cp tc-quality-review.py ~/.claude/hooks/tc-quality-review.py
chmod +x ~/.claude/hooks/tc-quality-review.py
```

### 2. Add the hook to settings

Add the following to `~/.claude/settings.json` (or `<project>/.claude/settings.json` for project-scope):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "AskUserQuestion",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/tc-quality-review.py"
          }
        ]
      }
    ]
  }
}
```

If you already have a `hooks` section, merge the `PreToolUse` entry into it.

### 3. (Optional) Add CLAUDE.md rule

Add this to your `CLAUDE.md` to reinforce the behavior at the prompt level:

```markdown
- **Tool call parameters follow the same TC quality rules as chat.**
  `AskUserQuestion` fields (`question`, `label`, `description`), `TaskCreate`
  descriptions, and any tool parameter visible to the user must pass the same
  Traditional Chinese quality checks as chat replies. A PreToolUse hook will
  block `AskUserQuestion` calls containing Chinese text for self-review, but
  do not rely on the hook as the first line of defense — review before sending.
```

### 4. Restart Claude Code

Existing sessions do not pick up `settings.json` changes. Start a new session for the hook to take effect.

## Extending to other tools

To apply the same review to `TaskCreate`, `TaskUpdate`, or other tools, add more matchers:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "AskUserQuestion",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/tc-quality-review.py"
          }
        ]
      },
      {
        "matcher": "TaskCreate",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/tc-quality-review.py"
          }
        ]
      }
    ]
  }
}
```

## Token cost

Each Chinese `AskUserQuestion` adds one extra round trip (~650–1,350 output tokens). If the text needed correction, the corrected version triggers one more review pass (~500–1,000 additional tokens). Input tokens are largely covered by Anthropic's prompt cache (within the 5-minute TTL).

For a typical conversation with 1–3 Chinese questions, the overhead is ~1,000–3,000 tokens — negligible relative to total session usage.

## Companion skill

This hook pairs with the [`tc-review`](../../skills/tc-review/) skill, which provides the full review methodology for chat replies, documentation, and code comments. The hook handles the automated interception layer; the skill handles the review guidelines.

| Layer | Mechanism | Scope |
|---|---|---|
| `tc-review` skill | Prompt-level guidance for the LLM | Chat replies, docs, code comments, plan files |
| `tc-quality-hook` | Infrastructure-level PreToolUse gate | Tool call parameters (`AskUserQuestion`, optionally `TaskCreate` etc.) |

Both layers reinforce each other. The skill shapes how the model _generates_ Chinese text; the hook catches what slips through before the user sees it.

## Requirements

- Python 3.6+
- Claude Code with hooks support
- No external dependencies
