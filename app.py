from flask import Flask, jsonify
from flask_cors import CORS
from scraper import get_all_technical_fresher_jobs

app = Flask(__name__)
CORS(app)  # ✅ CORS now applied to the correct app

@app.route("/")
def home():
    return jsonify({"message": "Welcome to Fresher Jobs Scraper API"})

@app.route("/scrape-jobs", methods=["GET"])
def scrape_jobs():
    jobs = get_all_technical_fresher_jobs()
    return jsonify(jobs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
