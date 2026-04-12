from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>Hello, Flask!</h1><p>Your app is running.</p>"

@app.route("/ping")
def ping():
    return {"status": "ok", "message": "pong"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
