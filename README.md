# 峻爸 AI Transcriber v3.1（Adaptive Hardware Edition）

Windows 10/11 離線 Whisper × Google Gemini 語音轉文字工具。介面顯示作者為「峻爸」；技術性檔名、EXE、快取與 GitHub Artifact 仍保留 `Junba` 英文名稱，避免舊版設定失效。

## v3.1 核心升級

- 跨電腦自適應：NVIDIA CUDA、Intel GPU/NPU、Intel/AMD CPU。
- 自動自適應 / 效能優先 / 省電優先。
- 本機成功/失敗學習紀錄，下一次自動調整路徑。
- 加速器失敗時盡量在同一音訊區段降級繼續。
- Whisper 模型可選自動，依硬體與記憶體保守選型。
- Intel/AMD CPU 永遠保底。
- AMD GPU 尚未整合專用 GPU 後端時不強行啟動，安全改走 CPU。
- 完成視窗顯示總耗時與最終裝置。
- 保留切割、Gemini、混合模式、繁體中文、Word/TXT/SRT/VTT、立即停止輸出目前結果。

## GitHub Actions

Workflow 必須位於 Repository 根目錄：

`.github/workflows/build-windows-v3.1.yml`

Actions → **Build Windows EXE v3.1** → Run workflow。

優先下載 Portable Artifact：

`Junba-AI-Transcriber-v3.1-Portable-Windows-x64`

Single EXE：

`Junba-AI-Transcriber-v3.1-Single-EXE-Windows-x64`

OpenVINO / Intel NPU/GPU 建議優先使用 Portable 版。

## 建議預設

硬體加速：`自動自適應（建議）`

Whisper 模型：`自動（依硬體／記憶體）`
