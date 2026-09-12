import json
import re
import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent)
)

from app.vector_store import VectorStore

from app.rag import (
    answer_question,
    REFUSAL_THRESHOLD,
    has_meaningful_overlap
)


BASE_DIR = Path(__file__).resolve().parent

QUESTIONS_FILE = (
    BASE_DIR / "questions.json"
)

REPORT_FILE = (
    BASE_DIR / "evaluation_report.json"
)


def load_questions():

    with open(
        QUESTIONS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def extract_citations(answer):

    pattern = (
        r"\[Source:\s*([^,\]]+),\s*Page\s*(\d+)\]"
    )

    matches = re.findall(
        pattern,
        answer or ""
    )

    return [
        {
            "source": source.strip(),
            "page": int(page)
        }
        for source, page in matches
    ]


def check_retrieval(
    results,
    expected_sources
):

    retrieved = {
        (
            result["source"],
            result["page"]
        )
        for result in results
    }

    expected = {
        (
            item["source"],
            item["page"]
        )
        for item in expected_sources
    }

    return expected.issubset(
        retrieved
    )


def check_citations(
    answer,
    expected_sources
):

    citations = extract_citations(
        answer
    )

    cited = {
        (
            item["source"],
            item["page"]
        )
        for item in citations
    }

    expected = {
        (
            item["source"],
            item["page"]
        )
        for item in expected_sources
    }

    return expected.issubset(
        cited
    )


def evaluate_question(
    vector_store,
    question_data,
    run_generation=False
):

    question = question_data[
        "question"
    ]

    question_type = question_data[
        "type"
    ]

    expected_sources = (
        question_data.get(
            "expected_sources",
            []
        )
    )

    results = vector_store.search(
        question,
        top_k=12
    )

    best_score = (
        results[0]["score"]
        if results
        else 0.0
    )

    meaningful_overlap = (
        has_meaningful_overlap(
            question,
            results
        )
    )

    predicted_refusal = (
        not results
        or best_score < REFUSAL_THRESHOLD
        or not meaningful_overlap
    )

    if question_type == "unanswerable":

        retrieval_correct = True

    else:

        retrieval_correct = (
            check_retrieval(
                results,
                expected_sources
            )
        )

    result = {

        "id": question_data["id"],

        "question": question,

        "type": question_type,

        "expected_sources": (
            expected_sources
        ),

        "retrieved_sources": [

            {
                "source": item["source"],
                "page": item["page"],
                "score": round(
                    item["score"],
                    4
                ),
                "semantic_score": round(
                    item.get(
                        "semantic_score",
                        item["score"]
                    ),
                    4
                ),
                "lexical_score": round(
                    item.get(
                        "lexical_score",
                        0.0
                    ),
                    4
                )
            }

            for item in results
        ],

        "best_score": round(
            best_score,
            4
        ),

        "meaningful_overlap": (
            meaningful_overlap
        ),

        "predicted_refusal": (
            predicted_refusal
        ),

        "retrieval_correct": (
            retrieval_correct
        )

    }

    if run_generation:

        try:

            rag_result = answer_question(
                question=question,
                results=results,
                history=[]
            )

            answer = rag_result[
                "answer"
            ]

            result["answer"] = answer

            result["actual_refusal"] = (
                rag_result["refused"]
            )

            if question_type == "unanswerable":

                result[
                    "refusal_correct"
                ] = (
                    rag_result["refused"]
                    is True
                )

            else:

                result[
                    "refusal_correct"
                ] = (
                    rag_result["refused"]
                    is False
                )

                result[
                    "citation_correct"
                ] = check_citations(
                    answer,
                    expected_sources
                )

        except Exception as error:

            result[
                "generation_error"
            ] = str(error)

    return result


def print_summary(
    results,
    run_generation
):

    answerable = [
        item
        for item in results
        if item.get("type")
        != "unanswerable"
    ]

    unanswerable = [
        item
        for item in results
        if item.get("type")
        == "unanswerable"
    ]

    retrieval_correct = sum(
        item.get(
            "retrieval_correct",
            False
        )
        for item in answerable
    )

    predicted_refusals = sum(
        item.get(
            "predicted_refusal",
            False
        )
        for item in unanswerable
    )

    print()
    print("=" * 70)
    print("STUDYMATE AI EVALUATION")
    print("=" * 70)

    print()

    print(
        f"Total questions: "
        f"{len(results)}"
    )

    print(
        f"Answerable questions: "
        f"{len(answerable)}"
    )

    print(
        f"Unanswerable questions: "
        f"{len(unanswerable)}"
    )

    print()

    print(
        f"Correct source-page retrieval: "
        f"{retrieval_correct}/"
        f"{len(answerable)}"
    )

    print(
        f"Correct predicted refusals: "
        f"{predicted_refusals}/"
        f"{len(unanswerable)}"
    )

    print()
    print("=" * 70)
    print(
        "ANSWERABLE QUESTIONS WITH "
        "RETRIEVAL FAILURES"
    )
    print("=" * 70)

    failures = [
        item
        for item in answerable
        if not item.get(
            "retrieval_correct",
            False
        )
    ]

    if not failures:

        print("None.")

    else:

        for item in failures:

            print()

            print(
                f"Q{item['id']}: "
                f"{item['question']}"
            )

            print(
                f"Expected: "
                f"{item['expected_sources']}"
            )

            print(
                f"Best score: "
                f"{item['best_score']}"
            )

            print(
                "Retrieved:"
            )

            for source in item[
                "retrieved_sources"
            ]:

                print(
                    f"  {source['source']} | "
                    f"Page {source['page']} | "
                    f"Combined {source['score']} | "
                    f"Semantic {source['semantic_score']} | "
                    f"Lexical {source['lexical_score']}"
                )

    print()
    print("=" * 70)
    print(
        "UNANSWERABLE QUESTIONS"
    )
    print("=" * 70)

    for item in unanswerable:

        print()

        print(
            f"Q{item['id']}: "
            f"{item['question']}"
        )

        print(
            f"Best score: "
            f"{item['best_score']}"
        )

        print(
            f"Meaningful overlap: "
            f"{item['meaningful_overlap']}"
        )

        print(
            f"Predicted refusal: "
            f"{item['predicted_refusal']}"
        )

        print(
            "Top retrieved results:"
        )

        for source in item[
            "retrieved_sources"
        ][:3]:

            print(
                f"  {source['source']} | "
                f"Page {source['page']} | "
                f"Combined {source['score']} | "
                f"Semantic {source['semantic_score']} | "
                f"Lexical {source['lexical_score']}"
            )

    if run_generation:

        generated = [
            item
            for item in results
            if "actual_refusal" in item
        ]

        refusal_correct = sum(
            item.get(
                "refusal_correct",
                False
            )
            for item in generated
        )

        citation_results = [
            item
            for item in generated
            if item.get("type")
            != "unanswerable"
            and "citation_correct"
            in item
        ]

        citation_correct = sum(
            item.get(
                "citation_correct",
                False
            )
            for item in citation_results
        )

        print()
        print("=" * 70)
        print(
            "END-TO-END GEMINI EVALUATION"
        )
        print("=" * 70)

        print()

        print(
            f"Correct answer/refusal behavior: "
            f"{refusal_correct}/"
            f"{len(generated)}"
        )

        if citation_results:

            print(
                f"Correct source citations: "
                f"{citation_correct}/"
                f"{len(citation_results)}"
            )


def main():

    run_generation = (
        "--full"
        in sys.argv
    )

    questions = load_questions()

    vector_store = VectorStore()

    print(
        f"Loaded "
        f"{len(vector_store.items)} "
        f"indexed chunks."
    )

    if not vector_store.items:

        print()

        print(
            "ERROR: Vector store is empty."
        )

        print(
            "Upload study materials first."
        )

        return

    print()

    if run_generation:

        print(
            "FULL EVALUATION MODE"
        )

        print(
            "Gemini generation is enabled."
        )

    else:

        print(
            "RETRIEVAL EVALUATION MODE"
        )

        print(
            "Gemini answer generation "
            "is disabled."
        )

        print(
            "Use --full for end-to-end testing."
        )

    results = []

    for index, question_data in enumerate(
        questions,
        start=1
    ):

        print(
            f"[{index}/{len(questions)}] "
            f"{question_data['question']}"
        )

        try:

            result = evaluate_question(
                vector_store,
                question_data,
                run_generation
            )

            results.append(
                result
            )

        except Exception as error:

            print(
                f"ERROR while evaluating "
                f"Q{question_data['id']}: "
                f"{error}"
            )

            results.append(
                {
                    "id": question_data["id"],
                    "question": question_data[
                        "question"
                    ],
                    "type": question_data[
                        "type"
                    ],
                    "evaluation_error": (
                        str(error)
                    )
                }
            )

    report = {

        "total_questions": len(
            results
        ),

        "answerable_questions": sum(
            item.get("type")
            != "unanswerable"
            for item in results
        ),

        "unanswerable_questions": sum(
            item.get("type")
            == "unanswerable"
            for item in results
        ),

        "refusal_threshold": (
            REFUSAL_THRESHOLD
        ),

        "retrieval_top_k": 12,

        "generation_enabled": (
            run_generation
        ),

        "results": results

    }

    with open(
        REPORT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            report,
            file,
            indent=2,
            ensure_ascii=False
        )

    print_summary(
        results,
        run_generation
    )

    print()

    print(
        "Detailed report saved to:"
    )

    print(
        REPORT_FILE
    )


if __name__ == "__main__":

    main()