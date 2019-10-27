import os

import requests
from flask import Flask, send_file, Response
from bs4 import BeautifulSoup

app = Flask(__name__)


def get_fact():

    response = requests.get("http://unkno.com")

    soup = BeautifulSoup(response.content, "html.parser")
    facts = soup.find_all("div", id="content")

    return facts[0].getText()

def get_piglatin(text_to_translate):
    # text_to_translate should be the value returned from get_fact()
    response = requests.post("https://hidden-journey-62459.herokuapp.com/piglatinize/", data = {"input_text": text_to_translate})
    soup = BeautifulSoup(response.content, "html.parser")
    url = response.url
    return soup, url



@app.route('/')
def home():
    text_to_translate = get_fact()
    results = get_piglatin(text_to_translate)
    return "{}<br><br><a href='{}'>{}</a>".format(results[0], results[1], results[1])
    # return "FILL ME!"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6787))
    app.run(host='0.0.0.0', port=port, debug=True)

