from flask import Flask, request, jsonify
from flask_cors import CORS
from waitress import serve
import os
from text_summarizer.paragraph_summarizer import ParagraphSummarizer

app = Flask(__name__)
CORS(app)

model = ParagraphSummarizer()


@app.route("/", methods=["GET", "POST"])
def hello():
    return "Hello, World!"


@app.route("/summarize", methods=["POST"])
def summarize():
    print(request.args.get("input"))
    text_seq = request.args.get("input")
    out = model.execute(text_seq=text_seq)

    return jsonify({"out": out})


if __name__ == "__main__":
    try:
        port = int(os.environ.get("PORT", 5000))
    except:
        port = 5000

    print("Starting server on port {}".format(port))
    serve(app, host="0.0.0.0", port=port)
