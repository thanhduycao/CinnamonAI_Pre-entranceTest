from flask import Flask, request, jsonify
from waitress import serve
import os

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello, World!'


if __name__ == '__main__':
    try:
        port = int(os.environ.get('PORT', 5000))
    except:
        port = 5000

    print("Starting server on port {}".format(port))
    serve(app, host='0.0.0.0', port=port)
