from flask import Blueprint, request, jsonify, Response
from flask_jwt_extended import jwt_required
import requests
import os
import re
from dotenv import load_dotenv

load_dotenv()

voice_bp = Blueprint("voice", __name__)

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_URL = "https://api.elevenlabs.io/v1/text-to-speech"
VOICE_ID = "pNInz6obpgDQGcFmaJgB"  # Adam — deep male voice


def clean_text(text):
    """Remove emojis, symbols and clean text for natural speech."""

    # Remove emojis
    emoji_pattern = re.compile(
        "["
        u"\U0001F600-\U0001F64F"
        u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F9FF"
        u"\U0001FA00-\U0001FA9F"
        u"\U00002700-\U000027BF"
        u"\U0001F1E0-\U0001F1FF"
        u"\U00002500-\U00002BEF"
        u"\U00010000-\U0010FFFF"
        "]+",
        flags=re.UNICODE
    )
    text = emoji_pattern.sub("", text)

    # Remove markdown symbols
    text = re.sub(r"\*+", "", text)       # bold/italic asterisks
    text = re.sub(r"#+\s*", "", text)     # headings
    text = re.sub(r"`+", "", text)        # code backticks
    text = re.sub(r"_{2,}", "", text)     # underscores
    text = re.sub(r"\[|\]|\(|\)", "", text)  # brackets

    # Replace common symbols with words
    text = text.replace("%", " percent")
    text = text.replace("&", " and")
    text = text.replace("@", " at")
    text = text.replace("#", " number")
    text = text.replace("→", " to")
    text = text.replace("—", ", ")
    text = text.replace("·", ",")

    # Clean up extra whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Limit length to avoid burning credits
    if len(text) > 400:
        text = text[:400] + "."

    return text


@voice_bp.route("/speak", methods=["POST"])
@jwt_required()
def speak():
    data = request.get_json()
    raw_text = data.get("text", "").strip()

    if not raw_text:
        return jsonify({"error": "No text provided"}), 400

    if not ELEVENLABS_API_KEY:
        return jsonify({"error": "ElevenLabs API key not configured"}), 500

    text = clean_text(raw_text)

    if not text:
        return jsonify({"error": "Text was empty after cleaning"}), 400

    try:
        response = requests.post(
            f"{ELEVENLABS_URL}/{VOICE_ID}",
            headers={
                "xi-api-key": ELEVENLABS_API_KEY,
                "Content-Type": "application/json",
            },
            json={
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.4,          # lower = more expressive
                    "similarity_boost": 0.75,
                    "style": 0.5,              # adds emotion/expressiveness
                    "use_speaker_boost": True,
                },
            },
            timeout=15,
        )

        if response.status_code == 200:
            return Response(
                response.content,
                mimetype="audio/mpeg",
                headers={
                    "Content-Disposition": "inline",
                    "Cache-Control": "no-cache",
                },
            )
        else:
            error = response.json().get("detail", "Unknown error")
            return jsonify({"error": f"ElevenLabs error: {error}"}), response.status_code

    except requests.exceptions.Timeout:
        return jsonify({"error": "ElevenLabs timed out"}), 503
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@voice_bp.route("/voices", methods=["GET"])
@jwt_required()
def get_voices():
    if not ELEVENLABS_API_KEY:
        return jsonify({"error": "API key not configured"}), 500
    try:
        response = requests.get(
            "https://api.elevenlabs.io/v1/voices",
            headers={"xi-api-key": ELEVENLABS_API_KEY},
            timeout=10,
        )
        return jsonify(response.json()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500