#!/usr/bin/env python3
"""
PreToolUse hook for AskUserQuestion.
Blocks the call once to force Claude to self-review Chinese text quality.
Uses hash tracking so the same (or corrected) text passes on resubmission.
No external detection libraries — the LLM does the review.
"""

import sys
import json
import hashlib
import os
import re
import time

REVIEW_FILE = "/tmp/.claude-tc-reviewed"
MAX_AGE = 3600


def extract_strings(obj):
    if isinstance(obj, str):
        return [obj]
    if isinstance(obj, list):
        return [s for item in obj for s in extract_strings(item)]
    if isinstance(obj, dict):
        return [s for v in obj.values() for s in extract_strings(v)]
    return []


def has_cjk(text):
    return bool(re.search(r"[一-鿿]", text))


def load_reviewed():
    entries = {}
    if os.path.exists(REVIEW_FILE):
        try:
            with open(REVIEW_FILE, "r") as f:
                for line in f:
                    parts = line.strip().split("|", 1)
                    if len(parts) == 2:
                        entries[parts[0]] = float(parts[1])
        except Exception:
            pass
    now = time.time()
    return {h: ts for h, ts in entries.items() if now - ts < MAX_AGE}


def save_reviewed(entries):
    try:
        with open(REVIEW_FILE, "w") as f:
            for h, ts in entries.items():
                f.write(f"{h}|{ts}\n")
    except Exception:
        pass


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    tool_input = data.get("tool_input", {})
    strings = extract_strings(tool_input)
    cjk_parts = [s for s in strings if has_cjk(s)]

    if not cjk_parts:
        sys.exit(0)

    text_hash = hashlib.md5("\n".join(cjk_parts).encode()).hexdigest()[:16]
    entries = load_reviewed()

    if text_hash in entries:
        sys.exit(0)

    entries[text_hash] = time.time()
    save_reviewed(entries)

    print("⚠ 繁中品質自檢 ── AskUserQuestion 包含中文，請逐項檢視：")
    print("  1. 有無簡體字（专/办/设/执/资/软/网/关/单/进/异/处 等）")
    print("  2. 有無模型幻覺產生的錯字或罕用字（如 廩/裰 等語意不通的字）")
    print("  3. 用語是否為台灣工程師慣用（非大陸用語）")
    print("  4. 語句是否通順自然、沒有自創詞彙")
    print()
    print("待檢文字：")
    for p in cjk_parts:
        print(f"  │ {p}")
    print()
    print("修正後重新呼叫 AskUserQuestion。若確認無誤則直接重送相同內容。")
    sys.exit(2)


if __name__ == "__main__":
    main()
