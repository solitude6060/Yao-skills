# 交接

工作日期：2026-09-13。

## 本次完成

依目前 research-toolkit 來源及剛整合的 wait-what 分支，將公開社群版從 0.3.0
更新至 0.8.0，內容修改前已提交計畫。來源及調整依據見
[同步紀錄](docs/2026-09-13-community-sync.zh.md)。

## 接續方式

先讀 status.md、tracker.md、README.md 與同步紀錄。內容雜湊及檢查結果在
`docs/2026-09-13-community-validation.json`。套件修改後執行
`claude plugin validate .claude-plugin/plugin.json`、`claude plugin validate .`
及 `git diff --check`。修改指引前讀對應技能與繁體中文對照檔。

原有未追蹤的 `.omc/` 未修改，選用 hook 程式也保持不變。本次社群更新未安裝
執行環境設定；來源 repository 另有 wait-what 正典來源切換紀錄。

## README 改寫交接

目前 README 先說明技能選擇與實際開發方式，再提供 agent 本體與技能安裝：
Claude marketplace，以及 Codex、Grok Build、本機 Cursor、Pi Agent 共用的
使用者技能目錄。套件維持 0.8.0。後續應保留 wait-what 明確呼叫與其他情境選用
的區別，詳細設定另放專門文件。
