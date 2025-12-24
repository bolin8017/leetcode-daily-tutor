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

    # Prompt for code generation (first call)
    CODE_PROMPT = """請為以下 LeetCode 題目提供 C++ 解法程式碼。

題目名稱: {title}
題目連結: {url}

只需要提供完整的 C++ 程式碼，不需要任何說明。
程式碼必須可以直接在 LeetCode 上執行。

直接輸出程式碼，不要加任何其他文字："""

    # Prompt for explanation generation (second call)
    EXPLANATION_PROMPT = """你是一位資深的演算法面試教練。請針對以下 LeetCode 題目提供解題分析。

題目名稱: {title}
Rating: {rating}

請按照以下格式提供內容（使用繁體中文）：

## 題目描述
[用 2-3 句話簡潔描述這道題目在問什麼，包含輸入輸出格式]

## 解題思路
[簡述核心演算法與解題邏輯，2-3 句話]

## 複雜度分析
- **Time Complexity**: O(?)
- **Space Complexity**: O(?)

請直接開始，使用 ## 作為章節標題。保持簡潔專業。"""

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
        Generate complete solution by calling AI twice:
        1. Get C++ code
        2. Get explanation and analysis
        Then combine them into a formatted response.

        Args:
            problem_info: Dictionary containing problem information
                         (title, url, rating)

        Returns:
            Complete solution text with code and explanation

        Raises:
            Exception: If API call fails
        """
        try:
            logger.info(f"Generating solution for: {problem_info.get('title')}")

            # Step 1: Generate C++ code
            code = self._generate_code(problem_info)

            # Step 2: Generate explanation
            explanation = self._generate_explanation(problem_info)

            # Step 3: Combine them
            combined = f"""{explanation}

## C++ 程式碼
```cpp
{code}
```"""

            logger.info("Solution generated successfully")
            return combined

        except Exception as e:
            logger.error(f"Failed to generate solution: {e}")
            return self._get_fallback_message()

    def _generate_code(self, problem_info: Dict[str, str]) -> str:
        """Generate C++ code only."""
        try:
            prompt = self.CODE_PROMPT.format(
                title=problem_info.get('title', 'Unknown'),
                url=problem_info.get('url', '')
            )

            response = self.client.models.generate_content(
                model=config.GEMINI_MODEL,
                contents=prompt,
                config={
                    'temperature': config.GEMINI_TEMPERATURE,
                    'max_output_tokens': config.GEMINI_MAX_TOKENS,
                }
            )

            if not response.text:
                return "// Code generation failed"

            code = response.text.strip()

            # Check if response was truncated
            if hasattr(response, 'candidates') and response.candidates:
                finish_reason = response.candidates[0].finish_reason
                if finish_reason != 'STOP':
                    logger.warning(f"Code generation may be incomplete. Finish reason: {finish_reason}")

            # Remove ``` markers if AI added them
            code = code.replace('```cpp', '').replace('```c++', '').replace('```', '').strip()

            logger.info(f"Code generated: {len(code)} characters")
            return code

        except Exception as e:
            logger.error(f"Code generation failed: {e}")
            return "// Code generation failed"

    def _generate_explanation(self, problem_info: Dict[str, str]) -> str:
        """Generate problem explanation and analysis."""
        try:
            prompt = self.EXPLANATION_PROMPT.format(
                title=problem_info.get('title', 'Unknown'),
                rating=problem_info.get('rating', '0')
            )

            response = self.client.models.generate_content(
                model=config.GEMINI_MODEL,
                contents=prompt,
                config={
                    'temperature': config.GEMINI_TEMPERATURE,
                    'max_output_tokens': config.GEMINI_MAX_TOKENS,
                }
            )

            if not response.text:
                return "## 題目描述\n無法生成說明"

            # Check if response was truncated
            if hasattr(response, 'candidates') and response.candidates:
                finish_reason = response.candidates[0].finish_reason
                if finish_reason != 'STOP':
                    logger.warning(f"Explanation may be incomplete. Finish reason: {finish_reason}")

            logger.info(f"Explanation generated: {len(response.text)} characters")
            return response.text.strip()

        except Exception as e:
            logger.error(f"Explanation generation failed: {e}")
            return "## 題目描述\n無法生成說明"

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
