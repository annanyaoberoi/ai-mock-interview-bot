import json
import os
from typing import Any

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, static_folder=BASE_DIR, static_url_path="")
CORS(app)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "").strip()
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def call_model(messages: list[dict[str, str]], temperature: float = 0.7) -> str:
    """Send a chat completion request to OpenRouter."""
    if not OPENROUTER_API_KEY:
        raise RuntimeError(
            "OPENROUTER_API_KEY is missing. Add it to your local .env file."
        )

    response = requests.post(
        OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": os.getenv("APP_URL", "http://localhost:5000"),
            "X-Title": "InterviewAI",
        },
        json={
            "model": OPENROUTER_MODEL,
            "messages": messages,
            "temperature": temperature,
        },
        timeout=60,
    )

    if not response.ok:
        try:
            detail = response.json().get("error", {}).get("message", response.text)
        except ValueError:
            detail = response.text
        raise RuntimeError(f"AI provider error ({response.status_code}): {detail}")

    payload = response.json()
    choices = payload.get("choices", [])
    if not choices:
        raise RuntimeError("The AI provider returned an empty response.")
    return choices[0]["message"]["content"].strip()


def build_interview_prompt(config: dict[str, Any]) -> str:
    role = str(config.get("role", "Software Engineer"))[:120]
    level = str(config.get("level", "Entry level"))[:60]
    focus = str(config.get("focus", "Mixed interview"))[:100]
    company = str(config.get("company", "")).strip()[:100]

    return f"""
You are InterviewAI, a thoughtful and realistic mock interviewer.

Interview setup:
- Target role: {role}
- Candidate level: {level}
- Interview focus: {focus}
- Target company (if provided): {company or "Not specified"}

How to conduct the interview:
1. Ask exactly one clear question at a time.
2. Wait for the candidate's answer before asking the next question.
3. Ask relevant follow-up questions when an answer is vague or interesting.
4. Keep the difficulty appropriate for the candidate level.
5. Do not invent facts about the candidate or claim to measure facial expressions,
   vocal confidence, eye contact, or body language.
6. Be professional, encouraging, and specific. Avoid giving away the ideal answer
   before the candidate has attempted the question.
7. If the candidate asks for a hint, give a small hint rather than the full answer.
8. Start by briefly introducing the interview and asking the first question.
"""


@app.get("/")
def home():
    return send_from_directory(BASE_DIR, "index.html")


@app.get("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "provider_configured": bool(OPENROUTER_API_KEY),
        "model": OPENROUTER_MODEL,
    })


@app.post("/api/chat")
def chat():
    data = request.get_json(silent=True) or {}
    messages = data.get("messages", [])
    config = data.get("config", {})

    if not isinstance(messages, list) or not messages:
        return jsonify({"error": "Send a non-empty messages array."}), 400

    safe_messages = []
    for item in messages[-24:]:
        if not isinstance(item, dict):
            continue
        role = item.get("role")
        content = item.get("content")
        if role not in ("user", "assistant") or not isinstance(content, str):
            continue
        content = content.strip()
        if content:
            safe_messages.append({"role": role, "content": content[:6000]})

    if not safe_messages or safe_messages[-1]["role"] != "user":
        return jsonify({"error": "The latest message must be from the candidate."}), 400

    try:
        system_prompt = build_interview_prompt(config if isinstance(config, dict) else {})
        reply = call_model([{"role": "system", "content": system_prompt}, *safe_messages])
        return jsonify({"reply": reply})
    except requests.Timeout:
        return jsonify({"error": "The AI request timed out. Please try again."}), 504
    except requests.RequestException:
        app.logger.exception("Network error while contacting AI provider")
        return jsonify({"error": "Could not reach the AI provider. Check your connection."}), 502
    except Exception as exc:
        app.logger.exception("Interview chat failed")
        return jsonify({"error": str(exc)}), 502


@app.post("/api/evaluate")
def evaluate():
    data = request.get_json(silent=True) or {}
    transcript = data.get("transcript", [])
    config = data.get("config", {})

    if not isinstance(transcript, list) or not transcript:
        return jsonify({"error": "There is no interview transcript to evaluate."}), 400

    transcript_text = []
    for item in transcript[-40:]:
        if isinstance(item, dict) and item.get("role") in ("user", "assistant"):
            content = str(item.get("content", "")).strip()[:4000]
            if content:
                label = "Candidate" if item["role"] == "user" else "Interviewer"
                transcript_text.append(f"{label}: {content}")

    if not any(line.startswith("Candidate:") for line in transcript_text):
        return jsonify({"error": "Answer at least one question before requesting feedback."}), 400

    config = config if isinstance(config, dict) else {}
    prompt = f"""
Evaluate this completed mock interview fairly and constructively.

Role: {str(config.get("role", "Not specified"))[:120]}
Level: {str(config.get("level", "Not specified"))[:60]}
Focus: {str(config.get("focus", "Mixed"))[:100]}

Use only evidence in the transcript. Do not claim to assess voice, body language,
confidence from facial expressions, or facts not present in the answers.
Return ONLY valid JSON with this exact shape:
{{
  "overall_score": integer from 0 to 100,
  "summary": "2-3 sentence overall assessment",
  "strengths": ["specific strength", "specific strength"],
  "improvements": ["specific actionable improvement", "specific actionable improvement"],
  "communication": "brief evidence-based observation about clarity and structure",
  "technical_depth": "brief evidence-based observation about correctness and depth",
  "next_steps": ["practice task", "practice task", "practice task"]
}}

If the transcript is short, say that the evaluation is based on limited evidence and
avoid overstating precision.

TRANSCRIPT:
{chr(10).join(transcript_text)}
"""
    try:
        raw = call_model([{"role": "user", "content": prompt}], temperature=0.2)
        cleaned = raw.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[-1].rsplit("```", 1)[0].strip()
        result = json.loads(cleaned)
        score = max(0, min(100, int(result.get("overall_score", 0))))
        result["overall_score"] = score
        return jsonify({"evaluation": result})
    except json.JSONDecodeError:
        app.logger.exception("Evaluation response was not valid JSON")
        return jsonify({"error": "The evaluator returned an unreadable result. Please try again."}), 502
    except Exception as exc:
        app.logger.exception("Interview evaluation failed")
        return jsonify({"error": str(exc)}), 502


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.getenv("PORT", "5000")), debug=False)
