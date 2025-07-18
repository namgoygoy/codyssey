from flask import Flask, request, render_template
from gtts import gTTS
import os
import io
import base64
from datetime import datetime

app = Flask(__name__)

VALID_LANGS = {'ko', 'en', 'ja', 'es'}

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    audio = None

    if request.method == 'POST':
        input_text = request.form.get('input_text', '').strip()
        lang = request.form.get('lang', 'ko')

        # 입력 검증
        if not input_text:
            error = "텍스트를 입력하세요."
        elif lang not in VALID_LANGS:
            error = f"지원하지 않는 언어입니다: {lang}"
        else:
            try:
                # 로그 기록
                with open("input_log.txt", "a", encoding="utf-8") as f:
                    f.write(f"{datetime.now()} - 텍스트: {input_text}, 언어: {lang}\n")

                # TTS 처리
                tts = gTTS(text=input_text, lang=lang)
                mp3_fp = io.BytesIO()
                tts.write_to_fp(mp3_fp)
                mp3_fp.seek(0)
                audio = base64.b64encode(mp3_fp.read()).decode('utf-8')
            except Exception as e:
                error = f"음성 생성 실패: {e}"

    return render_template("index.html", error=error, audio=audio)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
