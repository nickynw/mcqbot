"Basic frontend to serve the Graph Data into an MCQ format"
import requests
from flask import Flask, render_template, Response

app = Flask(__name__)


@app.route('/')
def home() -> Response:
    """
    Renders and displays the homepage.

    Returns:
        flask.Response: A Flask HTML template
    """
    try:
        response = requests.get('http://127.0.0.1:8000/', timeout=1)
        if response.status_code == 200:
            data = response.json()
            return render_template('home.html', **data)
    except Exception:
        pass
    return render_template(
            'error.html',
    )


app.run(host='127.0.0.1', port=5000)
