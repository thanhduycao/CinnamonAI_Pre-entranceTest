from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn import __version__ as sklearn_version
from underthesea import word_tokenize
import argparse
from packaging import version

MODEL_NAME = "sentence-transformers/distiluse-base-multilingual-cased-v2"
STOP_WORDS_PATH = "stopwords/vietnamese-stopwords.txt"


class KeywordExtractor:
    """Extract keywords from text"""

    def __init__(self) -> None:
        self.model = SentenceTransformer(MODEL_NAME)
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    def execute(
        self, docs, keyphrase_ngram_range, stop_words=[], top_n=5, vectorizer=None
    ):
        docs = word_tokenize(docs, format="text")
        if isinstance(docs, str):
            if docs:
                docs = [docs]
            else:
                return []

        # if stop_words.__len__() == 0:
        #     stop_words = self.get_stop_words(STOP_WORDS_PATH)

        if vectorizer is None:
            try:
                count = CountVectorizer(
                    ngram_range=keyphrase_ngram_range,
                    stop_words=stop_words,
                ).fit(docs)
            except ValueError:
                return []
        else:
            count = vectorizer.fit(docs)

        if version.parse(sklearn_version) >= version.parse("1.0.0"):
            words = count.get_feature_names_out()
        else:
            words = count.get_feature_names()

        doc_embeddings = self.model.encode(docs, convert_to_tensor=True)
        word_embeddings = self.model.encode(words, convert_to_tensor=True)
        df = count.transform(docs)
        keywords = []
        for index, _ in enumerate(docs):
            try:
                # Select embeddings
                candidate_indices = df[index].nonzero()[1]
                candidates = [words[index] for index in candidate_indices]
                candidate_embeddings = word_embeddings[candidate_indices]
                doc_embedding = doc_embeddings[index].reshape(1, -1)

                distances = cosine_similarity(
                    doc_embedding.cpu(), candidate_embeddings.cpu()
                )
                keywords = [
                    (candidates[index], round(float(distances[0][index]), 4))
                    for index in distances.argsort()[0][-top_n:]
                ][::-1]

                keywords.append(keywords)

            # Capturing empty keywords
            except ValueError:
                keywords.append([])

        return keywords

    def tokenize(self, text):
        return self.tokenizer(text, return_tensors="pt")

    def get_stop_words(self, stop_words_path):
        """load stop words"""
        with open(stop_words_path, "r", encoding="utf-8") as f:
            stopwords = f.readlines()
        stop_set = set(m.strip() for m in stopwords)
        return frozenset(stop_set)


def main():
    """Example runs:
    ```
    python text_summarizer/keyword_extractor.py
    ```
    """
    parser = argparse.ArgumentParser(
        description="Extract keywords from text",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--text",
        type=str,
        default="",
        help="Text to extract keywords",
    )
    parser.add_argument(
        "--top_n",
        type=int,
        default=5,
        help="Number of keywords to extract",
    )
    parser.add_argument(
        "--ngram_range",
        type=int,
        nargs="+",
        default=[1, 1],
        help="N-gram range for keyword extraction",
    )
    parser.add_argument(
        "--stop_words",
        type=str,
        nargs="+",
        default=[],
        help="Stop words for keyword extraction",
    )
    args = parser.parse_args()

    keyword_extractor = KeywordExtractor()
    keywords = keyword_extractor.execute(
        args.text, args.ngram_range, args.stop_words, args.top_n
    )
    print(keywords)


if __name__ == "__main__":
    main()
