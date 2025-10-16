from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import openai, os

# Load environment variables from .env
load_dotenv()

# Initialize Flask app
app = Flask(__name__, static_folder="static")  # Keep static folder
CORS(app)

# Get your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Serve index.html from static
@app.route("/")
def home():
    return send_from_directory(app.static_folder, "index.html")

# AI Code Review route
@app.route("/review", methods=["POST"])
def review_code():
    data = request.get_json()
    code_snippet = data.get("code", "")

    if not code_snippet:
        return jsonify({"error": "No code provided"}), 400

    try:
        # Call OpenAI API to review code
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an expert AI code reviewer. Review the following code for bugs, improvements, and efficiency issues."},
                {"role": "user", "content": code_snippet}
            ]
        )

        feedback = response.choices[0].message.content
        return jsonify({"review": feedback})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Keyword generation route for recent searches
@app.route("/keyword", methods=["POST"])
def generate_keyword():
    data = request.get_json()
    code_snippet = data.get("code", "")

    if not code_snippet:
        return jsonify({"keyword": "Untitled snippet"})

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are an AI assistant that generates a short descriptive keyword for a code snippet."},
                {"role": "user", "content": f"Summarize this code into a short descriptive keyword (3-5 words max):\n{code_snippet}"}
            ]
        )
        keyword = response.choices[0].message.content.strip()
        return jsonify({"keyword": keyword})
    except Exception as e:
        return jsonify({"keyword": "Untitled snippet"})

if __name__ == "__main__":
    app.run(debug=True)
