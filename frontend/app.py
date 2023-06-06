"""Basic frontend to serve the Graph Data into an MCQ format"""
import requests
from flask import Flask, render_template
from dotenv import load_dotenv
import os 

load_dotenv()
app = Flask(__name__)


@app.route('/')
def home() -> str:
    """
    Renders and displays the homepage.

    Returns:
        flask.Response: A Flask HTML template
    """
    try:
        response = requests.get(os.environ['API_URL'], timeout=1)
        if response.status_code == 200:
            data = response.json()
            return render_template('home.html', **data)
    except Exception as e:
        print(str(e))
        pass
    return render_template(
        'error.html',
    )


app.run(host='127.0.0.1', port=5000)
