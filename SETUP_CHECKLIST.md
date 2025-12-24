# ✅ 設定檢查清單

請依序完成以下步驟，並打勾標記完成項目。

---

## 📋 準備階段

- [ ] 我已經閱讀了 [README.md](README.md)
- [ ] 我已經準備好以下帳號：
  - [ ] Google 帳號
  - [ ] GitHub 帳號
  - [ ] Telegram 帳號

---

## 🔑 第一步：收集所有需要的金鑰和 Token

請先完成所有設定，再一次性填入 GitHub Secrets。

### 1.1 Google Sheets 設定

- [ ] 已建立試算表 `LeetCode_Daily_Tutor`
- [ ] 已建立 `Settings` 工作表（A1: Target_Rating, B1: 1500）
- [ ] 已建立 `History` 工作表（A1: Problem_ID）
- [ ] 試算表 URL: `______________________________`

### 1.2 Google Service Account

- [ ] 已建立 Google Cloud 專案
- [ ] 已啟用 Google Sheets API
- [ ] 已啟用 Google Drive API
- [ ] 已建立 Service Account
- [ ] 已下載 JSON 金鑰檔案
- [ ] Service Account Email: `______________________________`
- [ ] 已將 Service Account Email 加入試算表編輯權限

**📝 記錄**: JSON 金鑰檔案路徑: `______________________________`

### 1.3 Telegram Bot

- [ ] 已透過 @BotFather 建立 Bot
- [ ] Bot Username: `______________________________`
- [ ] Bot Token: `______________________________`
- [ ] 已取得 Chat ID（個人或群組）
- [ ] Chat ID: `______________________________`

### 1.4 Gemini API

- [ ] 已前往 Google AI Studio
- [ ] 已建立 API Key
- [ ] API Key: `______________________________`

---

## 🚀 第二步：部署到 GitHub

### 2.1 上傳專案

- [ ] 已建立 GitHub Repository
- [ ] Repository URL: `______________________________`
- [ ] 已上傳所有專案檔案到 Repository

### 2.2 設定 GitHub Secrets

前往 Settings > Secrets and variables > Actions，新增以下 4 個 Secrets：

- [ ] **TELEGRAM_BOT_TOKEN**
  - 值: `你的 Bot Token`

- [ ] **TELEGRAM_CHAT_ID**
  - 值: `你的 Chat ID`

- [ ] **GEMINI_API_KEY**
  - 值: `你的 Gemini API Key`

- [ ] **GOOGLE_SHEETS_JSON**
  - 值: `完整的 JSON 金鑰檔案內容（包含大括號）`

### 2.3 啟用 GitHub Actions

- [ ] 已前往 Actions 分頁
- [ ] 已啟用 Workflows
- [ ] 可以看到 "LeetCode Daily AI Tutor" workflow

---

## ✅ 第三步：測試執行

### 3.1 手動觸發測試

- [ ] 已在 Actions 中手動執行 workflow
- [ ] Workflow 執行成功（綠色勾勾）
- [ ] 已收到 Telegram 測試訊息

### 3.2 驗證設定

收到的 Telegram 訊息應包含：
- [ ] 📅 日期
- [ ] 🏆 題目名稱
- [ ] ⭐ Rating 分數
- [ ] 🔗 題目連結
- [ ] 💡 AI 生成的解法
- [ ] 💻 C++ 程式碼

### 3.3 檢查 Google Sheets

- [ ] History 工作表已新增一筆題目 ID
- [ ] Settings 中的 Target_Rating 可正常修改

---

## 🎯 第四步：確認自動排程

### 4.1 排程設定

- [ ] 已確認 `.github/workflows/daily_job.yml` 的 cron 設定
- [ ] 預設：每天 UTC 01:00（台北時間 09:00）
- [ ] 如需修改時間，已更新 cron 表達式

### 4.2 等待第一次自動執行

- [ ] 已等待到預定的自動執行時間
- [ ] 自動執行成功
- [ ] 收到自動推送的訊息

---

## 🎉 完成！

如果以上所有項目都打勾了，恭喜你已經完成設定！

---

## 🔧 進階設定（選用）

### 本機測試環境

- [ ] 已安裝 Python 3.11+
- [ ] 已建立虛擬環境
- [ ] 已安裝相依套件 `pip install -r requirements.txt`
- [ ] 已建立 `.env` 檔案
- [ ] 已執行 `python scripts/test_connection.py` 測試連線
- [ ] 已執行 `python main.py` 測試完整流程

### 客製化設定

- [ ] 已調整 Gemini Prompt（如需要）
- [ ] 已修改執行時間（如需要）
- [ ] 已自訂 Telegram 訊息格式（如需要）

---

## 🆘 遇到問題？

### 常見問題檢查

**Google Sheets 連線失敗**
- [ ] 試算表名稱是否為 `LeetCode_Daily_Tutor`（完全相同）
- [ ] Service Account Email 是否有編輯權限
- [ ] JSON 金鑰是否完整（包含 `{` 和 `}`）

**Telegram 沒收到訊息**
- [ ] Bot Token 是否正確
- [ ] Chat ID 是否正確
- [ ] Bot 是否已加入群組（如果是群組）

**Gemini API 錯誤**
- [ ] API Key 是否有效
- [ ] 是否超過免費額度（unlikely）

**GitHub Actions 失敗**
- [ ] 所有 4 個 Secrets 都已設定
- [ ] Secret 名稱拼寫正確（區分大小寫）
- [ ] 查看 Actions logs 找出具體錯誤

### 獲取幫助

- 📖 [完整設定指南](docs/SETUP_GUIDE.md)
- 💡 [快速開始](QUICKSTART.md)
- 🐛 [回報問題](../../issues)

---

## 📊 設定完成度

計算你的完成度：

- 準備階段: ___/3 項
- 收集金鑰: ___/4 組
- GitHub 部署: ___/3 步驟
- 測試執行: ___/3 項
- 自動排程: ___/2 項

**總完成度**: ___/15 項

---

**祝你設定順利！** 🚀

完成後記得給專案一個 ⭐ Star！
