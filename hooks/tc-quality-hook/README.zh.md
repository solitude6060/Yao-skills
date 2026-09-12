# tc-quality-hook

[English](README.md) | 繁體中文

選用的 Claude Code `PreToolUse` hook（工具執行前的檢查），對象為
`AskUserQuestion`。本次未修改的 [Python 程式](tc-quality-review.py) 從
`tool_input` 取出含 CJK（中日韓文字區段）字元的字串，再計算雜湊。
首次看到的雜湊會輸出自我檢查清單並回傳結束碼 2；快取有效期間重新提交相同
文字時回傳 0。中文內容改變會得到新的雜湊，重新進入檢查。

清單要求模型檢查字形、台灣用語與語句。這個機制無法證明模型確實檢查，或文字
已經正確。JSON 無法解析或沒有 CJK 字元時回傳 0。雜湊快取位於
`/tmp/.claude-tc-reviewed`，有效期一小時；它可拋棄，不作審查紀錄或專案證據。

## 安裝

從本目錄將程式複製至 Claude hook 目錄：

```bash
mkdir -p "$HOME/.claude/hooks"
cp tc-quality-review.py "$HOME/.claude/hooks/tc-quality-review.py"
```

取代既有目標前先檢查內容。將下列項目合併至 `~/.claude/settings.json`，保留
其他設定及 hook：

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

依 Claude Code 版本重新載入設定。需要 Python 3，程式只使用標準函式庫。
安裝技能套件本身不會註冊 hook；執行環境行為參考官方
[hook 文件](https://code.claude.com/docs/en/hooks)。

## 搭配技能

[tc-review](../../skills/tc-review/SKILL.zh.md) 提供文字檢查指引。此 hook 在設定
的工具呼叫前要求額外自我檢查；兩種方法均未提供經量測的語言品質保證。
