# 📚 LeetCode Daily AI Tutor (C++)

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-automated-success.svg)
![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)

**自動化 LeetCode 每日練習系統**

每天定時推送精選題目與 AI 生成的 C++ 標準面試解法到 Telegram

[功能特色](#-功能特色) •
[快速開始](#-快速開始) •
[完整文檔](#-文檔) •
[專案架構](#-專案架構) •
[貢獻指南](#-貢獻)

</div>

---

## 🎯 專案簡介

LeetCode Daily AI Tutor 是一個全自動化的演算法學習助手，透過 GitHub Actions 每日定時執行，智慧選題並由 Google Gemini AI 生成專業的 C++ 面試解法，直接推送到你的 Telegram。

### 為什麼選擇這個專案？

- ✅ **完全免費**: 使用免費的 GitHub Actions、Gemini API 和 Telegram
- ✅ **零維護成本**: 一次設定，永久自動執行
- ✅ **智慧難度控管**: 透過 Google Sheets 遠端調整題目難度
- ✅ **專業解法**: AI 生成的 C++ 代碼符合面試標準
- ✅ **不重複出題**: 自動記錄已推送題目
- ✅ **模組化設計**: 易於擴展和客製化

---

## ✨ 功能特色

### 🎲 智慧選題系統

- 從 [LeetCode Problem Rating](https://zerotrac.github.io/leetcode_problem_rating/data.json) 獲取最新題目評分
- 根據目標 Rating ± 50 分自動篩選
- 排除已推送題目，確保不重複
- 隨機選擇，保持練習多樣性

### 🤖 AI 解法生成

- 使用 Google Gemini 1.5 Flash 模型
- 提供完整的 C++ 實作代碼
- 包含解題思路與複雜度分析
- 符合 LeetCode 和面試標準

### 📊 遠端配置管理

- Google Sheets 作為配置後台
- 即時調整目標難度，無需修改代碼
- 自動記錄推送歷史
- 可視化進度追蹤

### ⏰ 全自動執行

- GitHub Actions 定時任務
- 預設每天台北時間 09:00 執行
- 可自訂執行時間
- 支援手動觸發測試

### 📱 Telegram 推送

- 精美的 Markdown 格式訊息
- 包含題目連結、Rating、解法
- 支援個人或群組推送
- 即時接收，隨時隨地學習

---

## 🚀 快速開始

### 前置需求

- GitHub 帳號
- Google 帳號（用於 Sheets 和 Gemini API）
- Telegram 帳號

### 30 分鐘完整設定

我們提供了詳細的圖文教學，跟著步驟走即可完成設定：

1. **[📘 完整設定指南](docs/SETUP_GUIDE.md)** ← 從這裡開始！

或快速瀏覽核心步驟：

#### 步驟 1: 建立 Google Sheets

1. 建立名為 `LeetCode_Daily_Tutor` 的試算表
2. 建立兩個工作表：
   - `Settings`: 儲存目標 Rating
   - `History`: 記錄已推送題目

#### 步驟 2: 設定 Google Service Account

1. 在 [Google Cloud Console](https://console.cloud.google.com/) 建立專案
2. 啟用 Google Sheets API 和 Drive API
3. 建立 Service Account 並下載 JSON 金鑰
4. 將 Service Account Email 加入試算表權限

#### 步驟 3: 建立 Telegram Bot

1. 透過 [@BotFather](https://t.me/BotFather) 建立 Bot
2. 取得 Bot Token 和 Chat ID

#### 步驟 4: 取得 Gemini API Key

1. 前往 [Google AI Studio](https://aistudio.google.com/app/apikey)
2. 建立免費的 API Key

#### 步驟 5: 部署到 GitHub

1. Fork 此專案
2. 在 Settings > Secrets 中新增 4 個環境變數：
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
   - `GEMINI_API_KEY`
   - `GOOGLE_SHEETS_JSON`
3. 啟用 GitHub Actions
4. 手動測試執行

### 本機測試（選用）

```bash
# Clone 專案
git clone https://github.com/your-username/leetcode-daily-tutor.git
cd leetcode-daily-tutor

# 建立虛擬環境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安裝依賴
pip install -r requirements.txt

# 設定環境變數（建立 .env 檔案）
cp .env.example .env
# 編輯 .env 填入你的設定

# 測試連線
python scripts/test_connection.py

# 執行程式
python main.py
```

---

## 📁 專案架構

```
LeetCode Daily AI Tutor (C++)/
│
├── src/                          # 原始碼目錄
│   ├── __init__.py              # 模組初始化
│   ├── config.py                # 配置管理（環境變數、常數）
│   │
│   ├── services/                # 服務層
│   │   ├── __init__.py
│   │   ├── leetcode.py         # LeetCode 資料服務
│   │   ├── sheets.py           # Google Sheets 服務
│   │   ├── gemini.py           # Gemini AI 服務
│   │   └── telegram.py         # Telegram Bot 服務
│   │
│   └── utils/                   # 工具模組
│       ├── __init__.py
│       └── logger.py           # 日誌系統
│
├── scripts/                     # 工具腳本
│   ├── __init__.py
│   ├── setup_sheets.py         # Google Sheets 初始化
│   └── test_connection.py      # 連線測試工具
│
├── docs/                        # 文檔目錄
│   └── SETUP_GUIDE.md          # 完整設定指南
│
├── .github/
│   └── workflows/
│       └── daily_job.yml       # GitHub Actions 工作流程
│
├── main.py                      # 主程式入口
├── requirements.txt             # Python 依賴清單
├── .env.example                # 環境變數範本
├── .gitignore                  # Git 忽略檔案
│
├── README.md                    # 專案說明（本檔案）
├── CONTRIBUTING.md             # 貢獻指南
└── LICENSE                     # MIT 授權條款
```

### 模組說明

#### 核心模組

- **`main.py`**: 應用程式入口，orchestrator 模式
- **`config.py`**: 統一管理所有配置和環境變數

#### 服務層 (`services/`)

每個服務都是獨立的模組，負責與外部 API 互動：

- **`leetcode.py`**:
  - 抓取 LeetCode 題目評分
  - 篩選符合條件的題目
  - 排除已推送題目

- **`sheets.py`**:
  - 連接 Google Sheets
  - 讀取目標 Rating
  - 管理推送歷史

- **`gemini.py`**:
  - 呼叫 Gemini API
  - 生成 C++ 解法
  - 錯誤處理與 fallback

- **`telegram.py`**:
  - 格式化訊息
  - 發送到 Telegram
  - 連線測試

#### 工具層 (`utils/`)

- **`logger.py`**: 彩色日誌系統，支援多層級輸出

#### 腳本 (`scripts/`)

- **`setup_sheets.py`**: 自動初始化 Google Sheets 工作表
- **`test_connection.py`**: 測試所有服務連線

---

## 🛠️ 技術棧

| 組件 | 技術選擇 | 理由 |
|------|---------|------|
| **執行環境** | GitHub Actions | 免費、穩定、零維護 |
| **程式語言** | Python 3.11+ | 豐富的生態系統、易於開發 |
| **資料存儲** | Google Sheets | 免費、視覺化、易於管理 |
| **AI 引擎** | Gemini 1.5 Flash | 免費額度充足、回應快速 |
| **通知系統** | Telegram Bot | 即時推送、跨平台 |
| **資料來源** | LeetCode Rating API | 權威的題目難度評分 |

---

## 📖 文檔

- **[完整設定指南](docs/SETUP_GUIDE.md)** - 詳細的圖文教學
- **[貢獻指南](CONTRIBUTING.md)** - 如何參與開發
- **[MIT 授權](LICENSE)** - 開源授權條款

---

## 💡 使用範例

### Telegram 訊息範例

```
📅 LeetCode Daily Challenge - 2025-12-24

🏆 題目: Two Sum
⭐ Rating: 1520
🔗 題目連結

---

解題思路：
使用 Hash Map 來存儲已遍歷過的數字及其索引。
遍歷陣列時，檢查 target - current 是否存在於 Hash Map 中。
時間複雜度可優化至 O(n)。

C++ 程式碼：

```cpp
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        unordered_map<int, int> hash;

        for (int i = 0; i < nums.size(); i++) {
            int complement = target - nums[i];

            // 檢查 complement 是否存在
            if (hash.find(complement) != hash.end()) {
                return {hash[complement], i};
            }

            // 將當前數字加入 hash map
            hash[nums[i]] = i;
        }

        return {};
    }
};
```

複雜度分析：
- Time Complexity: O(n)
- Space Complexity: O(n)

---
💬 祝你練習順利！加油！🚀
```

### 調整難度

直接在 Google Sheets 修改 `Settings` 工作表的 `B1` 儲存格：

| 難度等級 | 建議 Rating | 適合對象 |
|----------|-------------|----------|
| 入門 | 1000-1200 | 初學者 |
| 簡單 | 1200-1400 | 熟悉基礎語法 |
| 中等 | 1500-1700 | 準備面試 |
| 困難 | 1800-2000 | 進階演算法 |
| 極難 | 2100+ | 競賽選手 |

---

## 🔧 進階配置

### 修改執行時間

編輯 [.github/workflows/daily_job.yml](.github/workflows/daily_job.yml):

```yaml
on:
  schedule:
    # Cron 語法: 分 時 日 月 週
    - cron: '0 1 * * *'  # UTC 01:00 (台北時間 09:00)
```

常用時間範例：
- `0 0 * * *` - 每天 00:00 UTC（台北 08:00）
- `0 2 * * *` - 每天 02:00 UTC（台北 10:00）
- `0 12 * * *` - 每天 12:00 UTC（台北 20:00）
- `0 0 * * 1` - 每週一 00:00 UTC

### 自訂 Gemini Prompt

編輯 [src/services/gemini.py](src/services/gemini.py) 中的 `SOLUTION_PROMPT`:

```python
SOLUTION_PROMPT = """
你的自訂 Prompt...
"""
```

### 支援多語言解法

未來可擴展支援 Python、Java 等語言，只需：

1. 修改 Gemini prompt 模板
2. 調整 Telegram 訊息格式
3. 可使用設定檔選擇語言

---

## 🤝 貢獻

我們歡迎所有形式的貢獻！

### 如何貢獻

1. Fork 這個專案
2. 建立你的功能分支 (`git checkout -b feature/AmazingFeature`)
3. Commit 你的修改 (`git commit -m 'feat: add some feature'`)
4. Push 到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

詳細指南請參考 [CONTRIBUTING.md](CONTRIBUTING.md)

### 貢獻者

感謝所有為這個專案做出貢獻的人！

<!-- 如果有貢獻者，可以使用以下格式 -->
<!-- ALL-CONTRIBUTORS-LIST:START -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

---

## 📊 專案狀態

### 已完成功能 ✅

- [x] 自動抓取 LeetCode 題目評分
- [x] Google Sheets 配置管理
- [x] Gemini AI 解法生成
- [x] Telegram 推送系統
- [x] GitHub Actions 自動化
- [x] 模組化架構設計
- [x] 完整的文檔和設定指南
- [x] 連線測試工具

### 規劃中功能 🚧

- [ ] 支援多語言解法（Python、Java）
- [ ] Web Dashboard 管理介面
- [ ] 題目分類標籤（DP、Graph、Tree 等）
- [ ] 學習進度統計圖表
- [ ] Discord Bot 支援
- [ ] 自訂 Prompt 模板庫

---

## ❓ 常見問題

### Q: 為什麼選擇 Google Sheets 而不是資料庫？

A:
- ✅ 完全免費，無需額外服務
- ✅ 視覺化，可直接查看和修改
- ✅ 無需伺服器，降低維護成本
- ✅ 易於分享和協作

### Q: Gemini API 免費額度夠用嗎？

A:
- 免費額度：每天 1500 次請求
- 本專案使用：每天 1 次
- 結論：完全充足，可使用 4+ 年

### Q: 可以部署到其他平台嗎？

A: 可以！支援：
- GitHub Actions（推薦）
- GitLab CI/CD
- 本機 Cron Job
- 雲端函數（AWS Lambda、GCP Functions）

### Q: 如何重置歷史紀錄？

A: 直接清空 Google Sheets 的 `History` 工作表（保留標題列）

更多問題請查看 [完整設定指南](docs/SETUP_GUIDE.md#常見問題)

---

## 📜 授權條款

本專案採用 [MIT License](LICENSE) 授權。

你可以自由地：
- ✅ 商業使用
- ✅ 修改
- ✅ 發布
- ✅ 私人使用

唯一要求：保留原始授權聲明

---

## 🌟 Star History

如果這個專案對你有幫助，請給個 ⭐️ 支持一下！

---

## 📧 聯絡方式

- **問題回報**: [GitHub Issues](../../issues)
- **功能建議**: [GitHub Discussions](../../discussions)
- **安全問題**: 請透過 Issues 私密回報

---

<div align="center">

**用演算法點亮每一天！🚀**

Made with ❤️ by LeetCode Daily AI Tutor Team

[⬆ 回到頂部](#-leetcode-daily-ai-tutor-c)

</div>
