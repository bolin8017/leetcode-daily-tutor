# ⚡ 快速入門指南

這份文件將引導你在 **30 分鐘內**完成 LeetCode Daily AI Tutor 的設定。

---

## 📝 設定檢查清單

使用這個檢查清單追蹤你的進度：

- [ ] **步驟 1**: 建立 Google Sheets 試算表
- [ ] **步驟 2**: 設定 Google Service Account
- [ ] **步驟 3**: 建立 Telegram Bot
- [ ] **步驟 4**: 取得 Gemini API Key
- [ ] **步驟 5**: 部署到 GitHub Actions
- [ ] **步驟 6**: 測試執行

---

## 🎯 步驟 1: 建立 Google Sheets (5 分鐘)

### 1.1 建立試算表

1. 前往 https://sheets.google.com
2. 建立新試算表
3. **重要**: 命名為 `LeetCode_Daily_Tutor`

### 1.2 建立 Settings 工作表

1. 重新命名「工作表1」為 `Settings`
2. 在儲存格輸入：
   - A1: `Target_Rating`
   - B1: `1500`

### 1.3 建立 History 工作表

1. 新增工作表，命名為 `History`
2. 在 A1 輸入: `Problem_ID`

✅ **完成！** 先不要關閉這個試算表

---

## 🔑 步驟 2: 設定 Google Service Account (10 分鐘)

### 2.1 建立 Google Cloud 專案

1. 前往 https://console.cloud.google.com/
2. 建立新專案，名稱: `leetcode-tutor`

### 2.2 啟用 API

在「API 和服務」>「程式庫」啟用：
- Google Sheets API
- Google Drive API

### 2.3 建立 Service Account

1. 前往「API 和服務」>「憑證」
2. 建立憑證 > 服務帳戶
3. 名稱: `leetcode-tutor-bot`
4. 角色: 編輯者（或跳過）

### 2.4 建立金鑰

1. 點擊剛建立的服務帳戶
2. 「金鑰」分頁 > 新增金鑰 > JSON
3. **下載金鑰檔案並妥善保管**

### 2.5 分享試算表

1. 複製 Service Account Email (格式: `xxx@xxx.iam.gserviceaccount.com`)
2. 回到 Google Sheets
3. 點擊「共用」，貼上 Email
4. 權限: 編輯者
5. 取消勾選「通知使用者」

✅ **完成！** 記下 Service Account Email

---

## 🤖 步驟 3: 建立 Telegram Bot (5 分鐘)

### 3.1 建立 Bot

1. 在 Telegram 搜尋 `@BotFather`
2. 發送: `/newbot`
3. 輸入 Bot 名稱: `LeetCode Daily Tutor`
4. 輸入 Username: `leetcode_daily_tutor_bot` (必須以 bot 結尾)
5. **複製 Bot Token** (格式: `123456789:ABCdef...`)

### 3.2 取得 Chat ID

**方法 A: 個人訊息**
1. 搜尋你的 Bot，發送任意訊息
2. 開啟: `https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates`
   (替換 YOUR_BOT_TOKEN)
3. 找到 `"chat":{"id": 數字}`
4. 複製這個數字

**方法 B: 群組訊息**
1. 建立群組，加入你的 Bot
2. 在群組發送訊息
3. 同樣使用上面的網址查看
4. 群組 ID 通常是負數

✅ **完成！** 記下 Bot Token 和 Chat ID

---

## ✨ 步驟 4: 取得 Gemini API Key (2 分鐘)

1. 前往 https://aistudio.google.com/app/apikey
2. 點擊「建立 API 金鑰」
3. 選擇專案（可使用之前建立的）
4. **複製 API Key** (格式: `AIzaSy...`)

✅ **完成！** 記下 API Key

---

## 🚀 步驟 5: 部署到 GitHub Actions (8 分鐘)

### 5.1 上傳專案到 GitHub

如果你還沒有上傳：

```bash
cd "LeetCode Daily AI Tutor (C++)"
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 5.2 設定 Secrets

1. 前往 GitHub Repository
2. Settings > Secrets and variables > Actions
3. 點擊「New repository secret」

依序新增這 4 個 Secrets：

| Secret 名稱 | 值 |
|------------|---|
| `TELEGRAM_BOT_TOKEN` | 你的 Bot Token |
| `TELEGRAM_CHAT_ID` | 你的 Chat ID |
| `GEMINI_API_KEY` | 你的 Gemini API Key |
| `GOOGLE_SHEETS_JSON` | **完整的 JSON 檔案內容** |

⚠️ **重點**:
- `GOOGLE_SHEETS_JSON` 要貼上整個 JSON 檔案內容
- 包含大括號 `{...}`
- 不要修改任何內容

### 5.3 啟用 GitHub Actions

1. 前往 Actions 分頁
2. 如果看到提示，點擊啟用

✅ **完成！** 準備測試

---

## ✅ 步驟 6: 測試執行 (5 分鐘)

### 6.1 手動觸發 Workflow

1. 前往 Actions 分頁
2. 點擊「LeetCode Daily AI Tutor」
3. 點擊「Run workflow」
4. 選擇 `main` branch
5. 點擊綠色的「Run workflow」

### 6.2 查看執行結果

1. 等待約 30-60 秒
2. 查看執行狀態（應該是綠色勾勾）
3. **檢查 Telegram** 是否收到訊息！

### 6.3 如果失敗了

點擊失敗的執行，查看 logs：

- **Google Sheets 錯誤**: 檢查試算表名稱、Service Account 權限
- **Telegram 錯誤**: 檢查 Bot Token、Chat ID
- **Gemini 錯誤**: 檢查 API Key
- **JSON 錯誤**: 檢查 GOOGLE_SHEETS_JSON 是否完整

---

## 🎉 恭喜！設定完成

如果你收到 Telegram 訊息，代表設定成功！

### 下一步

1. ⏰ **自動執行**: 每天台北時間 09:00 自動推送
2. 📊 **調整難度**: 修改 Google Sheets 的 Target_Rating
3. 📈 **追蹤進度**: 查看 History 工作表

### 進階設定

- 📖 [完整設定指南](docs/SETUP_GUIDE.md) - 詳細說明和常見問題
- 🔧 [修改執行時間](#修改執行時間)
- 💡 [自訂 AI Prompt](#自訂-prompt)

---

## 🛠️ 修改執行時間

預設每天 UTC 01:00（台北 09:00）執行。

要修改時間，編輯 `.github/workflows/daily_job.yml`:

```yaml
on:
  schedule:
    - cron: '0 1 * * *'  # 修改這裡
```

常用時間：
- `0 0 * * *` - 每天 08:00 台北
- `0 2 * * *` - 每天 10:00 台北
- `0 12 * * *` - 每天 20:00 台北

---

## 🆘 需要幫助？

- 📖 [完整設定指南](docs/SETUP_GUIDE.md)
- 🐛 [回報問題](../../issues)
- 💬 [討論區](../../discussions)

---

## 📊 設定時間預估

| 步驟 | 預估時間 |
|-----|---------|
| Google Sheets | 5 分鐘 |
| Service Account | 10 分鐘 |
| Telegram Bot | 5 分鐘 |
| Gemini API | 2 分鐘 |
| GitHub Actions | 8 分鐘 |
| 測試執行 | 5 分鐘 |
| **總計** | **~30 分鐘** |

---

**祝你學習順利！** 🚀

有問題隨時在 Issues 提問！
