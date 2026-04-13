from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("landing_page.html")

@app.route("/ping")
def ping():
    return {"status": "ok", "message": "pong"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
