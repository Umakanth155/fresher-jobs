from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

from flask import Flask, jsonify
from scraper import get_all_technical_fresher_jobs

app = Flask(__name__)

@app.route("/scrape-jobs", methods=["GET"])
def scrape_jobs():
    jobs = get_all_technical_fresher_jobs()
    return jsonify(jobs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
