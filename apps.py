from faster_whisper import WhisperModel
from fastapi import FastAPI, Form
import requests
import time

from typing import Optional
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast

LANGUAGE_TRANSLATE = "SnypzZz/Llama2-13b-Language-translate"

model_translate = MBartForConditionalGeneration.from_pretrained(LANGUAGE_TRANSLATE)
tokenizer_translate_en = MBart50TokenizerFast.from_pretrained(LANGUAGE_TRANSLATE, src_lang="en_XX")

tokenizer_translate_zh = MBart50TokenizerFast.from_pretrained(LANGUAGE_TRANSLATE, src_lang="zh_CN")

model_size = "large-v2"

# Run on GPU with FP16
model_speech2text = WhisperModel(model_size, device="cuda", compute_type="float16")

app = FastAPI()


def handle(mp3):
    start_time = time.time()
    segments, info = model_speech2text.transcribe(mp3, beam_size=1)
    end_time = time.time()
    target = []
    for segment in segments:
        target.append({"start": segment.start, "end": segment.end, "text": segment.text})

    return {"start_at": start_time, "result": target, "end_at": end_time, "cost": (end_time - start_time)}


@app.post("/api/v3/translate_en2zh")
async def translate(text: Optional[str] = Form(None)):
    model_inputs = tokenizer_translate_en(text, return_tensors="pt")
    generated_tokens = model_translate.generate(
        **model_inputs,
        forced_bos_token_id=tokenizer_translate_en.lang_code_to_id["zh_CN"]
    )
    return tokenizer_translate_en.batch_decode(generated_tokens, skip_special_tokens=True)


@app.post("/api/v3/translate_zh2en")
async def translate(text: Optional[str] = Form(None)):
    model_inputs = tokenizer_translate_zh(text, return_tensors="pt")
    generated_tokens = model_translate.generate(
        **model_inputs,
        forced_bos_token_id=tokenizer_translate_zh.lang_code_to_id["en_XX"]
    )
    return tokenizer_translate_zh.batch_decode(generated_tokens, skip_special_tokens=True)


@app.get("/api/v3/speech2text")
async def download_mp3(url: str):
    r = requests.get(url, allow_redirects=True)
    mp3_file_path = "/tmp/" + url.split("/")[-1]
    with open(mp3_file_path, 'wb') as f:
        f.write(r.content)
    result = handle(mp3_file_path)
    return {"status": "success", "message": "mp3 file processed successfully", "data": result}
