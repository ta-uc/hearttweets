import requests
import json
import os
from requests_oauthlib import OAuth1
from flask import Flask, render_template
from flask_sockets import Sockets

app = Flask(__name__)
sockets = Sockets(app)

api_key = os.environ['API_KEY']
api_secret = os.environ['API_SEC']
access_key = os.environ['AC_KEY']
access_secret = os.environ['AC_SEC']

url = "https://stream.twitter.com/1.1/statuses/sample.json"
auth = OAuth1(api_key, api_secret, access_key, access_secret)
lo = ('♥','♡','❤','❥','❦','❧','💖','💕','💓','💗','💘','💙','💛','💝','💜',\
'💟','💞','💑','😍','💌','ღ','💚','<3','はぁと','ハート')

@sockets.route('/echo')
def echo_socket(ws):
    r = requests.post(url, auth=auth, stream=True)
    for line in r.iter_lines():
        if line:
            l=line.decode('utf-8')
            ld = json.loads(l)
        if "text" in ld:
            for t in lo:
                if t in ld['text']:
                    message = ld['user']['profile_image_url']
                    ws.send(message)
                    break

        if ws.closed:
            break

@app.route('/')
def hello():
    return render_template('htw.html')

@app.route('/favicon.ico')
def nof():
    return ''
