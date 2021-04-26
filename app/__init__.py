from sqlite3.dbapi2 import Error
from flask import (Flask, render_template, request, session, Response, redirect, jsonify, url_for, flash, get_flashed_messages)
from .database import Database
import json
import threading
lock = threading.Lock()

## Initialize app 
app = Flask(__name__)
app.secret_key = 'icEfhHZVc2rVpSCEZHd4'

## Initialize database
db = Database('app/tweets_sentiment.db')


## routes

# home page
@app.route('/')
def index():
    return render_template('index.html')


# keyword search 
@app.route('/search', methods=['POST'])
def search():
    obj = request.get_json()
    lock.acquire(True)
    try:
        res = db.search(obj['type'], obj['keyword'])
        return {'data': json.dumps(res)}
    except Error as e:
        print(e)
    finally:
        lock.release()


# analysis
@app.route('/analysis')
def analysis():
    res = {'tweets': [], 'counts': [], 'meta': []}
    obj = request.args
    lock.acquire(True)
    try:
        tags = obj['tags'].split(',')
        res = db.get_data(tags, obj['location'], obj['from'], obj['to'])

        hashtags = ', '.join(['#'+val for val in obj['tags'].split(',')])
        res['meta'] = {'tags': hashtags, 'location': obj['location'], 'from': obj['from'], 'to': obj['to']}
    except Error as e:
        print(e)
    finally:
        lock.release()
    return render_template('analysis.html', tweets=res['tweets'], counts=res['counts'], meta=res['meta'])
