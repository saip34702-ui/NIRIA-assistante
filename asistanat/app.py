from flask import Flask, render_template, request, jsonify
import requests
import webbrowser
import threading
import os
import time

app = Flask(__name__)

# ===== NIRIA Personality =====
niria_personality = """
you are NIRIA, sai's personal AI.
be condfident, witty, and helpful.
always address sai as "Sai" in your responses.
respond in a concise manner, but feel free to add a touch of humor when appropriate.
"""

# ===== Auto Browser Open =====
def open_browser():
    time.sleep(1)
    webbrowser.open("http://127.0.0.1:5000")

# ===== Home Route =====
@app.route("/")
def home():
    return render_template("index.html")

# ===== Chat Route =====
@app.route("/ask", methods=["POST"])
def ask():
    user_message = request.json.get("message").lower()

    # ===== SYSTEM COMMANDS =====
    if "open chrome" in user_message:
        os.system("start chrome")
        return jsonify({"response": "Opening Chrome, Sai."})

    if "open whatsapp" in user_message:
        webbrowser.open("https://web.whatsapp.com")
        return jsonify({"response": "Opening WhatsApp Web, Sai."})

    if "open youtube" in user_message:
        webbrowser.open("https://youtube.com")
        return jsonify({"response": "Opening YouTube, Sai."})

    # ===== AI BRAIN =====
    full_prompt = niria_personality + "\nUser: " + user_message + "\nNIRIA:"

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "tinyllama",
                "prompt": full_prompt,
                "stream": False
            }
        )

        result = response.json()
        reply = result.get("response", "Sai, something went wrong.")

    except:
        reply = "Sai, AI brain connection failed. Check Ollama server."

    return jsonify({"response": reply})


if __name__ == "__main__":
    threading.Thread(target=open_browser).start()
    app.run(debug=True)