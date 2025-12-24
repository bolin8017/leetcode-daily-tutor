# 🤝 Contributing to LeetCode Daily AI Tutor

首先，感謝你願意為這個專案做出貢獻！

## 📋 貢獻指南

### 報告 Bug

如果你發現 bug，請：

1. 檢查 [Issues](../../issues) 確認問題尚未被回報
2. 建立新的 Issue，包含：
   - 清楚的標題
   - 詳細的問題描述
   - 重現步驟
   - 預期行為 vs 實際行為
   - 環境資訊（Python 版本、作業系統等）
   - 相關的錯誤訊息或截圖

### 建議新功能

我們歡迎新功能建議！請：

1. 先在 Issues 中討論你的想法
2. 說明功能的用途和價值
3. 等待維護者回應後再開始實作

### 提交 Pull Request

#### 開發流程

1. **Fork 這個專案**

2. **Clone 你的 Fork**
   ```bash
   git clone https://github.com/你的使用者名稱/leetcode-daily-tutor.git
   cd leetcode-daily-tutor
   ```

3. **建立開發分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/bug-description
   ```

4. **設定開發環境**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

5. **進行修改**
   - 遵循現有的程式碼風格
   - 新增必要的測試
   - 更新文檔

6. **測試你的修改**
   ```bash
   # 執行連線測試
   python scripts/test_connection.py

   # 測試主程式
   python main.py
   ```

7. **Commit 你的修改**
   ```bash
   git add .
   git commit -m "feat: add new feature description"
   ```

   Commit 訊息格式：
   - `feat:` 新功能
   - `fix:` Bug 修復
   - `docs:` 文檔更新
   - `style:` 程式碼格式調整
   - `refactor:` 程式碼重構
   - `test:` 測試相關
   - `chore:` 建置或輔助工具修改

8. **Push 到你的 Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

9. **建立 Pull Request**
   - 前往原專案的 GitHub 頁面
   - 點擊 "New Pull Request"
   - 選擇你的分支
   - 填寫 PR 描述：
     - 修改了什麼
     - 為什麼需要這個修改
     - 如何測試
   - 提交 PR

#### PR 審核標準

你的 PR 需要：
- [ ] 程式碼遵循專案風格
- [ ] 包含必要的註釋和文檔
- [ ] 通過所有測試
- [ ] 沒有引入新的警告或錯誤
- [ ] Commit 訊息清晰明確

## 💻 程式碼風格

### Python 風格指南

- 遵循 [PEP 8](https://pep8.org/)
- 使用 4 個空格縮排
- 函式和變數使用 snake_case
- 類別使用 PascalCase
- 常數使用 UPPER_CASE
- 每個函式都應該有 docstring

範例：

```python
def calculate_rating_range(target: int, tolerance: int = 50) -> tuple:
    """
    Calculate the rating range based on target and tolerance.

    Args:
        target: Target rating value
        tolerance: Allowed deviation from target (default: 50)

    Returns:
        Tuple of (min_rating, max_rating)
    """
    return (target - tolerance, target + tolerance)
```

### 模組組織

- 一個檔案對應一個主要類別或功能模組
- 相關功能放在同一個目錄
- 避免循環依賴

### 錯誤處理

- 使用適當的 Exception 類型
- 記錄錯誤到 logger
- 提供有意義的錯誤訊息

```python
try:
    result = risky_operation()
except SpecificException as e:
    logger.error(f"Operation failed: {e}")
    raise
```

## 🧪 測試

### 手動測試

```bash
# 測試所有服務連線
python scripts/test_connection.py

# 測試主程式流程
python main.py
```

### 測試清單

在提交 PR 前，請確認：
- [ ] Google Sheets 連線正常
- [ ] Gemini API 呼叫成功
- [ ] Telegram 訊息發送成功
- [ ] 錯誤處理正確
- [ ] Logging 資訊完整

## 📚 文檔

### 更新文檔

如果你的 PR 包含：
- 新功能 → 更新 README.md
- 設定變更 → 更新 docs/SETUP_GUIDE.md
- API 修改 → 更新相關的 docstring

### 文檔風格

- 使用繁體中文（用戶導向文檔）
- 使用英文（程式碼註釋和 docstring）
- 提供清楚的範例
- 包含必要的截圖或圖表

## 🏗️ 專案結構

```
LeetCode Daily AI Tutor (C++)/
├── src/                      # 原始碼
│   ├── config.py            # 配置管理
│   ├── services/            # 服務模組
│   │   ├── leetcode.py     # LeetCode 資料服務
│   │   ├── sheets.py       # Google Sheets 服務
│   │   ├── gemini.py       # Gemini AI 服務
│   │   └── telegram.py     # Telegram Bot 服務
│   └── utils/              # 工具模組
│       └── logger.py       # 日誌系統
├── scripts/                # 工具腳本
│   ├── setup_sheets.py    # Sheets 初始化
│   └── test_connection.py # 連線測試
├── docs/                   # 文檔
│   └── SETUP_GUIDE.md     # 設定指南
├── .github/
│   └── workflows/
│       └── daily_job.yml  # GitHub Actions
├── main.py                # 主程式入口
├── requirements.txt       # Python 依賴
└── README.md             # 專案說明
```

## 🎯 開發優先級

我們歡迎以下類型的貢獻：

### 高優先級
- Bug 修復
- 效能改善
- 文檔改進
- 錯誤處理增強

### 中優先級
- 新功能（需先討論）
- 程式碼重構
- 測試覆蓋率提升

### 低優先級
- 程式碼風格調整
- 註釋改善

## 💬 溝通管道

- **Bug 回報和功能建議**: [GitHub Issues](../../issues)
- **討論和提問**: [GitHub Discussions](../../discussions)
- **程式碼審核**: Pull Request 留言

## 📜 行為準則

### 我們的承諾

為了營造開放且友善的環境，我們承諾：

- 使用友善和包容的語言
- 尊重不同的觀點和經驗
- 優雅地接受建設性批評
- 專注於對社群最有利的事情
- 對其他社群成員展現同理心

### 不被接受的行為

- 使用性暗示的語言或圖像
- 人身攻擊或侮辱性評論
- 騷擾（公開或私下）
- 未經許可發布他人隱私資訊
- 其他不專業或不適當的行為

## ⚖️ 授權

提交貢獻即表示你同意你的作品將以專案的 [MIT License](LICENSE) 授權。

---

## 🙏 感謝

感謝所有為這個專案做出貢獻的人！

每一個貢獻，無論大小，都讓這個專案變得更好。❤️

---

有任何問題嗎？請隨時開啟 Issue 詢問！
