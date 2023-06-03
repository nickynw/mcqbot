from flask import Flask, render_template, jsonify
import requests
import random

app = Flask(__name__)


@app.route('/')
def home():
    try:
        response = requests.get("http://127.0.0.1:8000/")
    except Exception:
        return render_template('error.html',)
    if response.status_code == 200:
        try:
            data = response.json()
            return render_template('home.html',  **data)
        except:
            return render_template('error.html',)
    return render_template('error.html',)

app.run(host='127.0.0.1', port=5000)