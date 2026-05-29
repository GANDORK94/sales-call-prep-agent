"""
Web server for the Sales Call Prep Agent.

Exposes two routes:
  GET  /           -- renders the input form
  POST /generate   -- runs the agent, saves the brief to output/, and
                      returns the briefing plus the saved filename as JSON

Run with: python app.py
Then open http://localhost:5001 in your browser.
"""

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

from agent import run_agent, save_output

load_dotenv()

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/generate", methods=["POST"])
def generate():
    company = request.form.get("company", "").strip()
    persona = request.form.get("persona", "").strip()
    notes = request.form.get("notes", "").strip()

    if not company or not persona:
        return jsonify({"error": "Company name and prospect role are both required."}), 400

    try:
        result = run_agent(company_name=company, persona_title=persona, notes=notes)
        saved_path = save_output(result, company)
        return jsonify({"result": result, "saved_as": str(saved_path)})
    except Exception as e:
        error_msg = str(e)
        if "401" in error_msg:
            return jsonify({"error": "Invalid API key. Check your ANTHROPIC_API_KEY."}), 500
        if "credit" in error_msg.lower():
            return jsonify({"error": "Insufficient API credits. Add credits at console.anthropic.com."}), 500
        return jsonify({"error": f"Something went wrong: {e}"}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5001)
