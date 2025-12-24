"""
Google Gemini AI service module.
Handles AI-powered solution generation.
"""

from typing import Dict
from google import genai

from src.config import config
from src.utils.logger import logger


class GeminiService:
    """Service for interacting with Google Gemini API."""

    # Prompt template for solution generation
    SOLUTION_PROMPT = """你是一位資深的演算法面試教練。請針對以下 LeetCode 題目，提供完整的題目說明與 C++ 標準面試解法。

題目名稱: {title}
題目連結: {url}
Rating: {rating}

請嚴格按照以下格式提供內容（使用繁體中文回答）：

## 題目描述
[用 2-3 句話簡潔描述這道題目在問什麼，包含輸入輸出格式]

## 解題思路
[簡述核心演算法與解題邏輯，說明為什麼這樣解，2-4 句話]

## C++ 程式碼
```cpp
// 完整的 C++ 程式碼
class Solution {{
public:
    // 你的解法
}};
```

## 複雜度分析
- **Time Complexity**: O(?)
- **Space Complexity**: O(?)

重要提醒：
1. 程式碼區塊必須以 ```cpp 開頭，以 ``` 結尾
2. 不要使用其他程式碼標記或格式
3. 章節標題使用 ## 格式
4. 保持簡潔專業，避免冗長說明

請立即開始，直接從「## 題目描述」開始回答。"""

    def __init__(self):
        """Initialize Gemini service."""
        self._configure_api()
        logger.info(f"Gemini service initialized with model: {config.GEMINI_MODEL}")

    def _configure_api(self):
        """Configure Gemini API with credentials."""
        try:
            self.client = genai.Client(api_key=config.gemini_api_key)
            logger.info("Gemini API configured successfully")
        except Exception as e:
            logger.error(f"Failed to configure Gemini API: {e}")
            raise

    def generate_solution(self, problem_info: Dict[str, str]) -> str:
        """
        Generate C++ solution for a LeetCode problem.

        Args:
            problem_info: Dictionary containing problem information
                         (title, url, rating)

        Returns:
            Generated solution text

        Raises:
            Exception: If API call fails
        """
        try:
            logger.info(f"Generating solution for: {problem_info.get('title')}")

            # Format prompt
            prompt = self.SOLUTION_PROMPT.format(
                title=problem_info.get('title', 'Unknown'),
                url=problem_info.get('url', ''),
                rating=problem_info.get('rating', '0')
            )

            # Generate content using new API
            response = self.client.models.generate_content(
                model=config.GEMINI_MODEL,
                contents=prompt,
                config={
                    'temperature': config.GEMINI_TEMPERATURE,
                    'max_output_tokens': config.GEMINI_MAX_TOKENS,
                }
            )

            if not response.text:
                raise ValueError("Empty response from Gemini API")

            # Check if response was truncated
            if hasattr(response, 'candidates') and response.candidates:
                finish_reason = getattr(response.candidates[0], 'finish_reason', None)
                if finish_reason and 'MAX_TOKENS' in str(finish_reason):
                    logger.warning(f"⚠️ Response may be truncated (finish_reason: {finish_reason})")
                    logger.warning(f"Response length: {len(response.text)} characters")

            logger.info("Solution generated successfully")
            return response.text

        except Exception as e:
            logger.error(f"Failed to generate solution: {e}")
            # Return fallback message
            return self._get_fallback_message()

    def _get_fallback_message(self) -> str:
        """
        Get fallback message when AI generation fails.

        Returns:
            Fallback error message
        """
        return """⚠️ **AI 解法生成暫時失敗**

請直接參考題目連結進行練習。

建議手動解題步驟：
1. 仔細閱讀題目要求
2. 分析輸入輸出範例
3. 思考可能的演算法（暴力法 → 優化）
4. 實作並測試
5. 分析時間與空間複雜度

💡 常見演算法模式：
- Two Pointers
- Sliding Window
- Hash Map
- Binary Search
- Dynamic Programming
- DFS/BFS
"""

    def test_connection(self) -> bool:
        """
        Test Gemini API connection.

        Returns:
            True if connection is successful
        """
        try:
            test_prompt = "Please respond with 'OK'"
            response = self.client.models.generate_content(
                model=config.GEMINI_MODEL,
                contents=test_prompt
            )
            return bool(response.text)
        except Exception as e:
            logger.error(f"Gemini API test failed: {e}")
            return False
