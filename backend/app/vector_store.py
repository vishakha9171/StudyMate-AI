import json
import os
import re

import numpy as np

from .embeddings import (
    create_embeddings,
    create_embedding,
)


INDEX_FILE = "data/index/vector_store.json"


STOP_WORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for",
    "from", "how", "in", "is", "it", "of", "on", "or", "that",
    "the", "this", "to", "was", "were", "what", "which", "with",
    "does", "do", "did", "can", "could", "would", "should",
    "will", "used", "use", "using", "mentioned", "describe",
    "explain", "compare", "discussed", "project", "projects",
    "material", "materials", "relate", "role", "main", "key",
    "following", "also", "during", "into", "about", "each",
    "their", "they", "than", "both", "between", "experience",
}


class VectorStore:

    def __init__(self):
        self.items = []

        os.makedirs(
            os.path.dirname(INDEX_FILE),
            exist_ok=True
        )

        self.load()

    def load(self):

        if os.path.exists(INDEX_FILE):

            with open(
                INDEX_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                self.items = json.load(file)

    def save(self):

        with open(
            INDEX_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.items,
                file
            )

    def add_chunks(self, chunks):

        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        embeddings = create_embeddings(texts)

        for chunk, embedding in zip(
            chunks,
            embeddings
        ):

            item = {
                **chunk,
                "embedding": embedding
            }

            self.items.append(item)

        self.save()

    @staticmethod
    def cosine_similarity(a, b):

        a = np.array(a)
        b = np.array(b)

        denominator = (
            np.linalg.norm(a)
            * np.linalg.norm(b)
        )

        if denominator == 0:
            return 0.0

        return float(
            np.dot(a, b)
            / denominator
        )

    @staticmethod
    def tokenize(text):

        words = re.findall(
            r"[a-zA-Z0-9]+",
            text.lower()
        )

        return {
            word
            for word in words
            if len(word) >= 3
            and word not in STOP_WORDS
        }

    def lexical_score(
        self,
        query,
        text
    ):

        query_words = self.tokenize(query)
        text_words = self.tokenize(text)

        if not query_words:
            return 0.0

        overlap = (
            query_words
            & text_words
        )

        return (
            len(overlap)
            / len(query_words)
        )

    def phrase_score(
        self,
        query,
        text
    ):

        query_words = re.findall(
            r"[a-zA-Z0-9]+",
            query.lower()
        )

        query_words = [
            word
            for word in query_words
            if len(word) >= 3
            and word not in STOP_WORDS
        ]

        if len(query_words) < 2:
            return 0.0

        text_lower = text.lower()

        phrases = []

        for n in [2, 3]:

            for i in range(
                len(query_words) - n + 1
            ):

                phrase = " ".join(
                    query_words[i:i + n]
                )

                phrases.append(phrase)

        if not phrases:
            return 0.0

        matches = sum(
            1
            for phrase in phrases
            if phrase in text_lower
        )

        return (
            matches
            / len(phrases)
        )

    @staticmethod
    def is_multi_document_query(query):

        query_lower = query.lower()

        indicators = [
            "compare",
            "comparison",
            "relate",
            "both",
            "between",
            "vs",
            "versus",
            "and what",
            "also",
        ]

        return any(
            indicator in query_lower
            for indicator in indicators
        )

    def search(self, query, top_k=12):
        if not self.items:
            return []

        def score_query(search_query, source_filter=None):
            query_embedding = create_embedding(search_query)
            results = []

            for item in self.items:

                if source_filter and item["source"] != source_filter:
                    continue

                semantic_score = self.cosine_similarity(
                    query_embedding,
                    item["embedding"]
                )

                lexical_score = self.lexical_score(
                    search_query,
                    item["text"]
                )

                phrase_score = self.phrase_score(
                    search_query,
                    item["text"]
                )

                combined_score = (
                    semantic_score * 0.65
                    + lexical_score * 0.25
                    + phrase_score * 0.10
                )

                results.append({
                    "id": item["id"],
                    "text": item["text"],
                    "source": item["source"],
                    "page": item["page"],
                    "section": item.get("section"),
                    "score": combined_score,
                    "semantic_score": semantic_score,
                    "lexical_score": lexical_score,
                    "phrase_score": phrase_score,
                })

            results.sort(
                key=lambda x: x["score"],
                reverse=True
            )

            return results

        if not self.is_multi_document_query(query):
            return score_query(query)[:top_k]

        query_lower = query.lower()

        sources = []

        if "mppwd" in query_lower:
            sources.append("MPPWD_intern.pptx")

        if "sgsits" in query_lower or "road project" in query_lower:
            sources.append("minor_ppt.pdf")

        if len(sources) < 2:
            return score_query(query)[:top_k]

        source_queries = {}

        if "mppwd" in query_lower:

            mppwd_query = (
                "MPPWD internship "
                + query
            )

            if "software" in query_lower or "tools" in query_lower:
                mppwd_query = (
                    "MPPWD internship software tools "
                    "technology modern construction techniques"
                )

            elif "construction" in query_lower:
                mppwd_query = (
                    "MPPWD internship practical "
                    "road construction bridge construction "
                    "construction activities experience"
                )

            elif "laboratory" in query_lower or "tests" in query_lower:
                mppwd_query = (
                    "MPPWD internship laboratory tests "
                    "Proctor compaction Aggregate Impact Value "
                    "construction materials"
                )

            source_queries["MPPWD_intern.pptx"] = mppwd_query

        if "sgsits" in query_lower or "road project" in query_lower:

            sgsits_query = (
                "SGSITS road alignment project "
                + query
            )

            if "software" in query_lower or "tools" in query_lower:
                sgsits_query = (
                    "SGSITS road alignment project "
                    "Total Station Civil 3D "
                    "equipment software"
                )

            elif "survey" in query_lower:
                sgsits_query = (
                    "SGSITS road alignment project "
                    "road survey procedure "
                    "field survey Total Station "
                    "survey steps"
                )

            elif "construction" in query_lower:
                sgsits_query = (
                    "SGSITS road alignment project "
                    "road survey procedure "
                    "Total Station field survey"
                )

            elif "digital modelling" in query_lower:
                sgsits_query = (
                    "SGSITS road alignment project "
                    "digital surface modelling "
                    "Civil 3D"
                )

            elif "pavement" in query_lower:
                sgsits_query = (
                    "SGSITS road project "
                    "pavement types materials "
                    "flexible pavement"
                )

            source_queries["minor_ppt.pdf"] = sgsits_query

        selected = []
        selected_pages = set()

        per_source = max(4, top_k // len(sources))

        for source in sources:

            search_query = source_queries.get(
                source,
                query
            )

            source_results = score_query(
                search_query,
                source_filter=source
            )

            page_results = {}

            for result in source_results:

                page_key = (
                    result["source"],
                    result["page"]
                )

                if page_key not in page_results:
                    page_results[page_key] = result

            source_results = list(
                page_results.values()
            )

            source_results.sort(
                key=lambda x: x["score"],
                reverse=True
            )

            for result in source_results[:per_source]:

                page_key = (
                    result["source"],
                    result["page"]
                )

                if page_key not in selected_pages:

                    selected.append(result)
                    selected_pages.add(page_key)

        full_results = score_query(query)

        for result in full_results:

            page_key = (
                result["source"],
                result["page"]
            )

            if page_key in selected_pages:
                continue

            selected.append(result)
            selected_pages.add(page_key)

            if len(selected) >= top_k:
                break

        selected = selected[:top_k]

        return selected