# 📘 完整設定指南

本指南將帶你一步步完成 LeetCode Daily AI Tutor 的完整設定。

## 📋 目錄

1. [前置需求](#前置需求)
2. [Google Sheets 設定](#google-sheets-設定)
3. [Google Service Account 設定](#google-service-account-設定)
4. [Telegram Bot 設定](#telegram-bot-設定)
5. [Gemini API 設定](#gemini-api-設定)
6. [GitHub Actions 部署](#github-actions-部署)
7. [本機測試](#本機測試)
8. [常見問題](#常見問題)

---

## 前置需求

- Google 帳號
- Telegram 帳號
- GitHub 帳號
- Python 3.11+ (僅本機測試需要)

---

## Google Sheets 設定

### 步驟 1: 建立試算表

1. 前往 [Google Sheets](https://sheets.google.com)
2. 點擊 **「空白」** 建立新試算表
3. **重要**: 將試算表重新命名為 `LeetCode_Daily_Tutor`
   - 點擊左上角「無標題的試算表」
   - 輸入 `LeetCode_Daily_Tutor`
   - 按 Enter 確認

### 步驟 2: 建立 Settings 工作表

1. 點擊左下角「工作表1」旁的 **+** 號
2. 右鍵點擊新工作表，選擇「重新命名」
3. 輸入 `Settings`
4. 在 Settings 工作表中輸入以下內容：

   | A | B |
   |---|---|
   | Target_Rating | 1500 |

   - A1 儲存格: `Target_Rating`
   - B1 儲存格: `1500`

### 步驟 3: 建立 History 工作表

1. 再次點擊左下角 **+** 號建立新工作表
2. 重新命名為 `History`
3. 在 A1 儲存格輸入: `Problem_ID`

### 完成結果

你的試算表應該有以下結構：

```
LeetCode_Daily_Tutor (試算表名稱)
├── Settings (工作表)
│   └── A1: Target_Rating | B1: 1500
└── History (工作表)
    └── A1: Problem_ID
```

📌 **重要**: 先不要關閉這個試算表，待會需要分享給 Service Account

---

## Google Service Account 設定

### 步驟 1: 建立 Google Cloud 專案

1. 前往 [Google Cloud Console](https://console.cloud.google.com/)
2. 點擊左上角專案選擇器
3. 點擊 **「新增專案」**
4. 輸入專案名稱（例如：`leetcode-tutor`）
5. 點擊 **「建立」**
6. 等待專案建立完成後，確認已切換到新專案

### 步驟 2: 啟用必要的 API

1. 在左側選單找到 **「API 和服務」** > **「程式庫」**
2. 搜尋並啟用以下 API：
   - **Google Sheets API**
     - 搜尋 "Google Sheets API"
     - 點擊進入
     - 點擊 **「啟用」**
   - **Google Drive API**
     - 搜尋 "Google Drive API"
     - 點擊進入
     - 點擊 **「啟用」**

### 步驟 3: 建立 Service Account

1. 前往 **「API 和服務」** > **「憑證」**
2. 點擊頂部 **「建立憑證」** > **「服務帳戶」**
3. 填寫資訊：
   - 服務帳戶名稱: `leetcode-tutor-bot`
   - 服務帳戶 ID: 自動產生（例如：`leetcode-tutor-bot@...`）
   - 描述: `Service account for LeetCode Daily Tutor`
4. 點擊 **「建立並繼續」**
5. 角色選擇: 選擇 **「編輯者」** 或跳過（我們會在 Sheets 中單獨授權）
6. 點擊 **「繼續」** 然後 **「完成」**

### 步驟 4: 建立並下載金鑰

1. 在「憑證」頁面，找到剛建立的服務帳戶
2. 點擊服務帳戶進入詳細資訊頁面
3. 切換到 **「金鑰」** 分頁
4. 點擊 **「新增金鑰」** > **「建立新的金鑰」**
5. 選擇金鑰類型: **JSON**
6. 點擊 **「建立」**
7. JSON 金鑰檔案會自動下載到你的電腦
8. **重要**: 妥善保管此檔案，不要分享給任何人

### 步驟 5: 複製 Service Account Email

1. 在服務帳戶詳細資訊頁面
2. 找到 **「電子郵件」** 欄位
3. 複製完整的 Email（格式類似：`leetcode-tutor-bot@xxx.iam.gserviceaccount.com`）

### 步驟 6: 分享 Google Sheets 給 Service Account

1. 回到你的 Google Sheets 試算表（`LeetCode_Daily_Tutor`）
2. 點擊右上角 **「共用」** 按鈕
3. 在「新增使用者和群組」欄位貼上剛複製的 Service Account Email
4. 權限設定為 **「編輯者」**
5. **取消勾選** "通知使用者"（這是機器人帳號，不需要通知）
6. 點擊 **「傳送」**

✅ 完成！Service Account 現在可以存取你的試算表了

---

## Telegram Bot 設定

### 步驟 1: 建立 Telegram Bot

1. 在 Telegram 中搜尋 `@BotFather`
2. 開始對話，發送指令: `/newbot`
3. BotFather 會詢問 Bot 名稱
   - 輸入: `LeetCode Daily Tutor` (或任何你喜歡的名稱)
4. 接著詢問 Bot 的 username
   - 輸入: `leetcode_daily_tutor_bot` (必須以 `bot` 結尾)
   - 如果名稱已被使用，嘗試其他名稱
5. 建立成功後，BotFather 會回傳 **Bot Token**
   - 格式: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`
   - **重要**: 複製並保存這個 Token

### 步驟 2: 取得 Chat ID

有兩種方式可以取得 Chat ID：

#### 方法 A: 發送到個人（私聊）

1. 在 Telegram 搜尋你剛建立的 Bot
2. 點擊 **「開始」** 或發送任意訊息給 Bot
3. 在瀏覽器開啟以下網址（替換 `YOUR_BOT_TOKEN`）:
   ```
   https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
   ```
4. 在回傳的 JSON 中找到 `"chat":{"id": 123456789}`
5. 複製這個數字（你的個人 Chat ID）

#### 方法 B: 發送到群組

1. 建立一個新的 Telegram 群組
2. 將你的 Bot 加入群組
   - 點擊群組名稱 > 新增成員 > 搜尋你的 Bot
3. 在群組中發送任意訊息（例如: `Hello`）
4. 在瀏覽器開啟以下網址:
   ```
   https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates
   ```
5. 在 JSON 中找到 `"chat":{"id": -1001234567890}`
   - 群組 Chat ID 通常是負數且較長
6. 複製這個數字

#### 快速方法: 使用 @userinfobot

1. 在 Telegram 搜尋 `@userinfobot`
2. 開始對話
3. Bot 會回傳你的個人 Chat ID

📝 **記錄以下資訊**:
- Bot Token: `1234567890:ABCdefGHI...`
- Chat ID: `123456789` 或 `-1001234567890`

---

## Gemini API 設定

### 步驟 1: 前往 Google AI Studio

1. 開啟 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. 使用你的 Google 帳號登入

### 步驟 2: 建立 API Key

1. 點擊 **「Get API Key」** 或 **「建立 API 金鑰」**
2. 選擇或建立一個 Google Cloud 專案
   - 可以使用之前建立的專案，或建立新的
3. 點擊 **「Create API Key」**
4. 複製顯示的 API Key
   - 格式: `AIzaSyXXXXXXXXXXXXXXXXXXXXXXXX`
   - **重要**: 保存這個 Key

### Gemini API 免費額度

- 每分鐘 15 次請求
- 每天 1500 次請求
- 每分鐘 100 萬 tokens
- **完全免費**，足夠每日使用

✅ Gemini API 設定完成！

---

## GitHub Actions 部署

### 步驟 1: 準備專案

1. Fork 或 Clone 此專案到你的 GitHub 帳號
2. 如果是本機開發，確保所有檔案都已提交:
   ```bash
   cd "LeetCode Daily AI Tutor (C++)"
   git add .
   git commit -m "Initial setup"
   git push origin main
   ```

### 步驟 2: 設定 GitHub Secrets

1. 前往你的 GitHub Repository 頁面
2. 點擊 **Settings** (設定)
3. 左側選單選擇 **Secrets and variables** > **Actions**
4. 點擊 **New repository secret**

依序新增以下 4 個 Secrets:

#### Secret 1: TELEGRAM_BOT_TOKEN

- Name: `TELEGRAM_BOT_TOKEN`
- Secret: 貼上你的 Telegram Bot Token
- 點擊 **Add secret**

#### Secret 2: TELEGRAM_CHAT_ID

- Name: `TELEGRAM_CHAT_ID`
- Secret: 貼上你的 Chat ID（個人或群組）
- 點擊 **Add secret**

#### Secret 3: GEMINI_API_KEY

- Name: `GEMINI_API_KEY`
- Secret: 貼上你的 Gemini API Key
- 點擊 **Add secret**

#### Secret 4: GOOGLE_SHEETS_JSON

- Name: `GOOGLE_SHEETS_JSON`
- Secret: 開啟之前下載的 JSON 金鑰檔案
  - 複製 **完整的 JSON 內容**（包含大括號 `{}`）
  - 貼上到 Secret 欄位
  - **重要**: 確保是完整的 JSON，不要遺漏任何字元
- 點擊 **Add secret**

### 步驟 3: 啟用 GitHub Actions

1. 前往 **Actions** 分頁
2. 如果看到提示，點擊 **I understand my workflows, go ahead and enable them**
3. 你會看到 **LeetCode Daily AI Tutor** workflow

### 步驟 4: 測試執行

1. 點擊 **LeetCode Daily AI Tutor** workflow
2. 點擊右側 **Run workflow** 按鈕
3. 選擇 `main` branch
4. 點擊 **Run workflow**
5. 等待執行完成（約 30-60 秒）
6. 檢查你的 Telegram，應該會收到訊息！

### 步驟 5: 確認自動排程

- Workflow 會在每天 **UTC 01:00**（台北時間 09:00）自動執行
- 你可以在 `.github/workflows/daily_job.yml` 中修改時間
- Cron 語法範例:
  - `0 1 * * *` - 每天 01:00 UTC
  - `0 0 * * *` - 每天 00:00 UTC（台北時間 08:00）
  - `30 2 * * *` - 每天 02:30 UTC（台北時間 10:30）

✅ GitHub Actions 部署完成！

---

## 本機測試

如果你想在本機測試程式:

### 步驟 1: 安裝 Python 環境

```bash
# 確認 Python 版本
python --version  # 需要 3.11+

# 建立虛擬環境
python -m venv venv

# 啟用虛擬環境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 步驟 2: 安裝相依套件

```bash
pip install -r requirements.txt
```

### 步驟 3: 設定環境變數

建立 `.env` 檔案（可參考 `.env.example`）:

```bash
# 複製範例檔案
cp .env.example .env

# 編輯 .env 檔案，填入你的資訊
nano .env  # 或使用其他編輯器
```

`.env` 檔案內容:

```bash
TELEGRAM_BOT_TOKEN=你的Bot Token
TELEGRAM_CHAT_ID=你的Chat ID
GEMINI_API_KEY=你的Gemini API Key
GOOGLE_SHEETS_JSON={"type":"service_account",...}  # 完整 JSON
```

### 步驟 4: 載入環境變數

```bash
# macOS/Linux:
export $(cat .env | xargs)

# Windows (PowerShell):
Get-Content .env | ForEach-Object { $var = $_.Split('='); [Environment]::SetEnvironmentVariable($var[0], $var[1]) }
```

### 步驟 5: 測試連線

```bash
python scripts/test_connection.py
```

應該看到所有服務都通過測試:

```
✅ Google Sheets: PASS
✅ Gemini API: PASS
✅ Telegram Bot: PASS
```

### 步驟 6: 執行主程式

```bash
python main.py
```

檢查 Telegram 是否收到訊息！

---

## 常見問題

### Q1: Google Sheets 連線失敗

**錯誤**: `SpreadsheetNotFound`

**解決方法**:
1. 確認試算表名稱是 `LeetCode_Daily_Tutor`（大小寫需完全相同）
2. 確認 Service Account Email 已加入試算表權限
3. 檢查 `GOOGLE_SHEETS_JSON` 是否包含完整 JSON 內容

### Q2: Telegram 沒收到訊息

**可能原因**:
1. Bot Token 錯誤 → 重新確認從 BotFather 取得的 Token
2. Chat ID 錯誤 → 使用 `getUpdates` API 重新取得
3. Bot 未加入群組 → 確認 Bot 在群組中
4. Bot 被靜音 → 檢查群組設定

### Q3: Gemini API 額度用完

**解決方法**:
- 免費額度: 每天 1500 次請求
- 每日執行一次不會超過額度
- 如果需要更多，考慮升級到付費方案

### Q4: GitHub Actions 執行失敗

**檢查事項**:
1. 所有 4 個 Secrets 都已正確設定
2. Secret 名稱拼寫正確（大小寫需相同）
3. JSON 格式正確（使用 JSON validator 檢查）
4. 查看 Actions 的執行紀錄 (logs) 找出具體錯誤

### Q5: 找不到符合條件的題目

**解決方法**:
1. 調整 Google Sheets 中的 `Target_Rating`
2. 清空 History 工作表（保留標題列）
3. 檢查 Rating 資料源是否正常

### Q6: 程式顯示權限錯誤

**解決方法**:
1. 確認 Service Account 有試算表的「編輯者」權限
2. 確認已啟用 Google Sheets API 和 Google Drive API
3. 重新建立並下載 Service Account 金鑰

---

## 🎉 設定完成！

恭喜！如果你完成了以上所有步驟，你的 LeetCode Daily AI Tutor 已經準備就緒。

### 下一步

1. ⏰ 等待每天自動執行，或手動觸發 workflow
2. 📊 隨時調整 Google Sheets 的 Target_Rating
3. 📈 定期檢查 History，追蹤你的進度
4. 💪 持續練習，提升演算法能力！

### 獲取幫助

- 查看 [README.md](../README.md) 了解更多資訊
- 遇到問題？請開啟 [GitHub Issue](../../issues)
- 想貢獻代碼？請參考 [CONTRIBUTING.md](../CONTRIBUTING.md)

祝你學習順利！🚀
