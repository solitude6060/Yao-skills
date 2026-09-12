# Worktree 衛生管理

英文 [SKILL.md](SKILL.md) 是執行規範。

用在建立、稽核、退役或整批清理 git worktree，以及任何考慮 `git worktree remove` 的時候。
規則來自 2026-08 一次實際事件：52 個 worktree、23 GB gitignored 實驗資料差點遺失。

1. R1：實驗產物只放持久的 sibling 目錄，寫入前用 `realpath` 檢查不在任何 worktree 內。
2. R2：建立時登記到 `docs/worktree-registry.md`；退役前四道關卡全過——沒有行程占用、
   非快取 ignored 檔案都已進 archive 且 SHA-256 相符、bundle 在 manifest commit 之後重做並有
   離機備份、HEAD 可從 origin ref 到達。
3. R3：一個 checkout 一個寫者；外部 agent 要寫就用 full clone。
4. R4：非快取 ignored 掃描只讀不改；發現就搬到 archive，不 `git add`、不改 `.gitignore`。
5. 同時最多 5 個 worktree；逐棵移除，不批次 `rm -rf`；`--force` 只在四關全綠之後。
6. 沒有使用者明確授權不刪除任何 worktree。
