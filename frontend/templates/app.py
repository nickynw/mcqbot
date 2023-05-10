from flask import Flask, render_template, jsonify
import requests
import random

app = Flask(__name__)
app.debug = True

@app.route('/')
def hello():
    response = requests.get("http://127.0.0.1:8000/")
    if response.status_code == 200:
        data = response.json()
        return render_template('home.html',  **data)
    return render_template('error.html',)