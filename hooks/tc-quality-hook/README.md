# tc-quality-hook

English | [繁體中文](README.zh.md)

Optional Claude Code `PreToolUse` hook for `AskUserQuestion`. The unchanged
[Python script](tc-quality-review.py) extracts strings from `tool_input`, selects
strings containing CJK characters, and hashes them. An unseen hash produces a
review checklist and exit code 2; an identical resubmission within the cache
lifetime exits 0. Changed Chinese text has a new hash and is checked again.

The checklist asks the model to inspect character choice, Taiwan vocabulary and
sentence clarity. The hook cannot prove that a review occurred or that the text
is correct. Invalid JSON or input without CJK characters exits 0. Its disposable
hash cache is `/tmp/.claude-tc-reviewed`, with a one-hour expiry; this is not a
review record or a place to store project evidence.

## Install

From this directory, copy the script to your existing Claude hook directory:

```bash
mkdir -p "$HOME/.claude/hooks"
cp tc-quality-review.py "$HOME/.claude/hooks/tc-quality-review.py"
```

Inspect an existing destination before replacing it. Merge the following entry
into `~/.claude/settings.json`, preserving other settings and hook entries:

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

Reload the configuration as required by your Claude Code version. Python 3 is
required; the script uses only the standard library. Installing the marketplace
skills does not register this hook. See the official
[hook reference](https://code.claude.com/docs/en/hooks) for runtime behavior.

## Companion skill

[tc-review](../../skills/tc-review/SKILL.md) provides the corresponding instruction
for reviewing prose. The hook requests an additional self-check at the configured
tool boundary; neither mechanism is a measured guarantee of language quality.
