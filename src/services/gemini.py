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
    SOLUTION_PROMPT = """你是一位資深的演算法面試教練。請針對以下 LeetCode 題目，提供 C++ 標準面試解法。

題目名稱: {title}
題目連結: {url}
Rating: {rating}

請提供以下內容（使用繁體中文回答）：

1. **解題思路**：簡述核心演算法與解題邏輯（2-3 句話）
2. **C++ 程式碼**：提供乾淨、符合面試標準的完整程式碼
3. **複雜度分析**：
   - Time Complexity:
   - Space Complexity:

請確保程式碼：
- 包含必要的註釋
- 變數命名清晰
- 符合 C++ 最佳實踐
- 可以直接在 LeetCode 上執行

請直接開始回答，不需要額外的開場白。"""

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
