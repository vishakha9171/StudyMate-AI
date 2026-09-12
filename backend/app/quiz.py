import json
from google import genai

from .config import GEMINI_API_KEY, GEMINI_MODEL


client = genai.Client(api_key=GEMINI_API_KEY)


def generate_quiz(results, num_questions=5):
    if not results:
        return {
            "questions": [],
            "message": "I cannot generate a quiz because the uploaded materials do not contain enough relevant information."
        }

    context_parts = []

    for i, result in enumerate(results, start=1):
        context_parts.append(
            f"""
SOURCE {i}
File: {result['source']}
Page: {result['page']}
Content:
{result['text']}
"""
        )

    context = "\n".join(context_parts)

    prompt = f"""
You are StudyMate AI, a study assistant that must use ONLY the provided course materials.

Create exactly {num_questions} multiple-choice questions from the material below.

Rules:
1. Use only information explicitly present in the material.
2. Do not use outside knowledge.
3. Each question must have exactly 4 options.
4. Provide exactly one correct answer.
5. Include the source filename and page number.
6. Do not create questions from information that is unclear or unsupported.
7. Make questions useful for university exam preparation.
8. Return ONLY valid JSON.
9. Do not use markdown.

Required JSON format:

{{
  "questions": [
    {{
      "question": "Question text",
      "options": [
        "Option A",
        "Option B",
        "Option C",
        "Option D"
      ],
      "answer": "Option A",
      "source": "filename.pdf",
      "page": 5
    }}
  ]
}}

COURSE MATERIAL:
{context}
"""

    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )

        text = response.text.strip()

        if text.startswith("```"):
            text = text.replace("```json", "")
            text = text.replace("```", "")
            text = text.strip()

        quiz = json.loads(text)

        if "questions" not in quiz:
            raise ValueError("Invalid quiz response.")

        return quiz

    except json.JSONDecodeError:
        raise RuntimeError(
            "Gemini returned an invalid quiz response. Please try again."
        )

    except Exception as error:
        error_text = str(error)

        if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:
            return {
                "questions": [],
                "message": (
                    "Gemini's free API quota has been reached. "
                    "Quiz generation will work again after the quota resets."
                )
            }

        raise RuntimeError(
            f"Quiz generation failed: {error}"
        )