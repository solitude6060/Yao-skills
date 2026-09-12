# Karpathy 風格編碼準則（繁體中文）

> 對應英文原文：[`SKILL.md`](SKILL.md)
> `SKILL.md` 仍是 agent/runtime 讀取的權威檔；此繁中版用於人類閱讀與維護，不改變 skill 行為。

## 用途
降低 LLM 寫程式常見錯誤：過度設計、改太多、沒有驗證成功條件、沒有揭露假設。適合寫 code、review 或 refactor 前閱讀。

## 使用時機
當使用者明確提到此 skill 名稱、相關關鍵字，或任務形態符合英文 `description` 時使用。實際執行前仍必須讀取並遵守原始 `SKILL.md`。

## 執行重點
- 保留原文中的命令、路徑、檔名、旗標、環境變數與工具名稱。
- 依原文定義的階段、品質門檻與停止條件執行，不用本繁中版取代權威指令。
- 若原文有狀態檔、review artifact、測試或驗證要求，完成前都要保留證據。

## 原文章節對照
- `# Karpathy Guidelines`
- `## 1. Think Before Coding`
- `## 2. Simplicity First`
- `## 3. Surgical Changes`
- `## 4. Goal-Driven Execution`

## 維護規則
更新 `SKILL.md` 時，請同步更新本檔的用途、使用時機與章節對照，避免繁中說明落後於實際 workflow。
