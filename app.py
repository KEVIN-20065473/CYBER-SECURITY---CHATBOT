from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_question = request.json.get("question", "")
    prompt = f"You are a cybersecurity expert. Provide clear, concise answers.\n\nQuestion: {user_question}"

    try:
        # Set num_predict lower to make it faster
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": "mistral",           # Use fastest model
            "prompt": prompt,
            "num_predict": 50,            # Reduce number of tokens
            "stream": False               # No streaming needed
        })

        if response.status_code == 200:
            answer = response.json().get("response", "").strip()
            return jsonify({"answer": answer})
        else:
            return jsonify({"answer": f"Error from Ollama: {response.status_code} - {response.text}"})

    except Exception as e:
        return jsonify({"answer": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
