from flask import Flask, request, jsonify
from flask_cors import CORS
from waitress import serve
import os
from text_summarizer.paragraph_summarizer import ParagraphSummarizer
from text_summarizer.keyword_extractor import KeywordExtractor

app = Flask(__name__)
CORS(app)

model = ParagraphSummarizer()
keywordExtractor = KeywordExtractor()


@app.route("/", methods=["GET", "POST"])
def hello():
    return "Health check: OK"


@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    text_seq = data["input"]
    out = model.execute(text_seq=text_seq)

    return jsonify({"out": out})


@app.route("/keywords", methods=["POST"])
def keywords():
    data = request.get_json()
    text_seq = data["input"]
    top_n = data["top_n"]
    out = keywordExtractor.execute(docs=text_seq, top_n=5, keyphrase_ngram_range=[1, 2])
    keywords = []
    if len(out) < top_n:
        top_n = len(out)
    for i in range(top_n):
        keywords.append(out[i][0])

    return jsonify({"keywords": keywords})


if __name__ == "__main__":
    try:
        port = int(os.environ.get("PORT", 5000))
    except:
        port = 5000

    print("Starting server on port {}".format(port))
    serve(app, host="0.0.0.0", port=port)
