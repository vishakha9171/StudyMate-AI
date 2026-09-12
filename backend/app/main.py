import os
import shutil
from pathlib import Path
from .quiz import generate_quiz

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .ingestion import process_document
from .models import ChatRequest
from .rag import answer_question
from .vector_store import VectorStore
from .vision import image_to_text


app = FastAPI(
    title="StudyMate AI API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = os.path.abspath("data/uploads")

os.makedirs(UPLOAD_DIR, exist_ok=True)

vector_store = VectorStore()

ALLOWED_DOCUMENTS = {
    ".pdf",
    ".pptx",
    ".md",
    ".txt",
}

ALLOWED_IMAGES = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}


@app.get("/")
def root():
    return {
        "message": "StudyMate AI backend is running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...)
):

    filename = file.filename or ""
    extension = Path(filename).suffix.lower()

    if (
        extension not in ALLOWED_DOCUMENTS
        and extension not in ALLOWED_IMAGES
    ):
        raise HTTPException(
            status_code=400,
            detail=(
                "Unsupported file type. "
                "Supported files: PDF, PPTX, MD, TXT, "
                "JPG, JPEG, PNG and WEBP."
            )
        )

    safe_filename = Path(filename).name

    file_path = os.path.abspath(
        os.path.join(
            UPLOAD_DIR,
            safe_filename
        )
    )

    print("----------------------------------------")
    print("Uploading file...")
    print(f"Filename: {safe_filename}")
    print(f"Extension: {extension}")
    print(f"Save path: {file_path}")
    print("----------------------------------------")

    try:

        with open(
            file_path,
            "wb"
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer
            )

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Could not save uploaded file: {error}"
        )

    if not os.path.exists(file_path):

        raise HTTPException(
            status_code=500,
            detail=(
                "File was uploaded but could not be "
                "found after saving."
            )
        )

    print(f"File saved successfully: {file_path}")

    try:

        if extension in ALLOWED_IMAGES:

            print("Processing image using Gemini Vision...")

            extracted_text = image_to_text(
                file_path
            )

            chunks = [
                {
                    "id": safe_filename,
                    "text": extracted_text,
                    "source": safe_filename,
                    "page": 1,
                    "section": "Handwritten Notes",
                    "source_type": "handwritten_image",
                }
            ]

        else:

            print(
                f"Processing document: {extension}"
            )

            chunks = process_document(
                file_path
            )

        if not chunks:

            raise HTTPException(
                status_code=400,
                detail=(
                    "No readable text was found "
                    "in this file."
                )
            )

        print(
            f"Chunks created: {len(chunks)}"
        )

        print(
            "Creating embeddings and updating "
            "vector store..."
        )

        vector_store.add_chunks(
            chunks
        )

        print(
            "File processed successfully."
        )

        print("----------------------------------------")

        return {
            "message": "File processed successfully.",
            "filename": safe_filename,
            "chunks_created": len(chunks),
        }

    except HTTPException:
        raise

    except Exception as error:

        print(
            f"Processing error: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


@app.post("/chat")
def chat(
    request: ChatRequest
):

    try:

        print("----------------------------------------")
        print(
            f"Question: {request.question}"
        )

        results = vector_store.search(
            request.question,
            top_k=12
        )

        print(
            f"Retrieved sources: {len(results)}"
        )

        result = answer_question(
            question=request.question,
            results=results,
            history=request.history
        )

        if result["refused"]:
            sources = []
        else:
            sources = results

        print(
            f"Refused: {result['refused']}"
        )

        print("----------------------------------------")

        return {
            "answer": result["answer"],
            "refused": result["refused"],
            "sources": sources,
        }

    except Exception as error:

        print(
            f"Chat error: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )

@app.post("/quiz")
def quiz(
    request: ChatRequest
):
    try:
        results = vector_store.search(
            request.question,
            top_k=12
        )

        quiz_result = generate_quiz(
            results,
            num_questions=5
        )

        return quiz_result

    except Exception as error:
        print(f"Quiz error: {error}")

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )