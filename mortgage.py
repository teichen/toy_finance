from flask import Flask

app = Flask(__name__)

@app.route("/")

def track_equity():

    return "calculating..."
