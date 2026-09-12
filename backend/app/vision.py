import base64
import mimetypes
import time

from google import genai

from .config import GEMINI_API_KEY, GEMINI_MODEL


client = genai.Client(api_key=GEMINI_API_KEY)

# Fallback models in case the primary model is temporarily busy
VISION_MODELS = [
    GEMINI_MODEL,
    "gemini-3.7-flash",
    "gemini-3.6-flash",
]


def image_bytes_to_text(image_bytes, mime_type="image/png"):

    if not image_bytes:
        raise ValueError("Image data is empty.")

    image_part = {
        "inline_data": {
            "mime_type": mime_type,
            "data": base64.b64encode(image_bytes).decode("utf-8"),
        }
    }

    prompt = """
You are reading a student's handwritten university study notes.

Carefully transcribe the text visible in the image.

Important instructions:

1. Preserve headings.
2. Preserve bullet points.
3. Preserve numbers and formulas.
4. Preserve mathematical expressions as accurately as possible.
5. Preserve technical terminology.
6. Do not invent words that cannot be read.
7. If a word or portion is genuinely unreadable, write [unclear].
8. Keep the original structure as much as possible.
9. Return ONLY the extracted/transcribed text.
"""

    last_error = None

    for model in VISION_MODELS:

        for attempt in range(2):

            try:

                print(
                    f"Trying Gemini vision model: {model} "
                    f"(attempt {attempt + 1})"
                )

                response = client.models.generate_content(
                    model=model,
                    contents=[
                        prompt,
                        image_part,
                    ],
                )

                extracted_text = response.text.strip()

                if extracted_text:
                    print(
                        f"Gemini OCR successful using {model}"
                    )

                    return extracted_text

            except Exception as error:

                last_error = error

                print(
                    f"Gemini model {model} failed: {error}"
                )

                # Wait briefly before retrying
                time.sleep(2)

    raise RuntimeError(
        "Gemini vision is temporarily unavailable. "
        f"Last error: {last_error}"
    )


def image_to_text(file_path):

    print(f"Reading image: {file_path}")

    with open(file_path, "rb") as image_file:
        image_bytes = image_file.read()

    if not image_bytes:
        raise ValueError("The uploaded image is empty.")

    mime_type, _ = mimetypes.guess_type(file_path)

    if mime_type not in {
        "image/jpeg",
        "image/png",
        "image/webp",
    }:
        raise ValueError(
            f"Unsupported image format: {mime_type}"
        )

    return image_bytes_to_text(
        image_bytes=image_bytes,
        mime_type=mime_type,
    )