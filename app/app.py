from flask import Flask, request
from logging.config import dictConfig
import openai
import os

dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] [%(process)d] [%(levelname)s] in %(module)s: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S %z"
            }
        },
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "DEBUG", "handlers": ["wsgi"]},
    }
)

app = Flask(__name__)

@app.route('/healthz/liveness')
def liveness():
    return "OK"

@app.route('/healthz/readiness')
def readiness():
    return "OK"

@app.route('/ask', methods=['POST'])
def ask():
    content = request.json
    question = content['question']

    # return a HTTP 400 if question is not set or empty
    if not question:
        return ('', 400)

    openai.api_type = "azure"
    openai.key = os.getenv("OPENAI_API_KEY") 
    openai.api_base = os.getenv('OPENAI_API_URL')
    deployment_name = os.getenv('DEPLOYMENT_NAME')
    openai.api_version = os.getenv('OPENAI_API_VERSION')

    response = openai.ChatCompletion.create(
                engine=deployment_name,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant called John Wick. Always introduce yourself. You may only answer questions related to software development and software engineering. Always answer in Markdown. You can use emojis and links if appropriate."},
                    {"role": "user", "content": question}
                ]
            )
    print(response)
    return response
