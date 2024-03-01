from time import sleep
import sys
import mergely
from faster_whisper import WhisperModel
import requests
import os
import json
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast


def handle(mp3):
    segments, info = model_speech2text.transcribe(mp3, beam_size=1)
    target = []
    for segment in segments:
        target.append({"start": segment.start, "end": segment.end, "text": segment.text})
    return target


def handle_speech2text(url):
    r = requests.get(url, allow_redirects=True)
    mp3_file_path = "/tmp/" + url.split("/")[-1]
    with open(mp3_file_path, 'wb') as f:
        f.write(r.content)

    result = handle(mp3_file_path)
    os.remove(mp3_file_path)
    return result


def translate_zh2en(text):
    model_inputs = tokenizer_translate_zh(text, return_tensors="pt")
    generated_tokens = model_translate.generate(
        **model_inputs,
        forced_bos_token_id=tokenizer_translate_zh.lang_code_to_id["en_XX"]
    )
    return tokenizer_translate_zh.batch_decode(generated_tokens, skip_special_tokens=True)


def translate_en2zh(text: str):
    model_inputs = tokenizer_translate_en(text, return_tensors="pt")
    generated_tokens = model_translate.generate(
        **model_inputs,
        forced_bos_token_id=tokenizer_translate_en.lang_code_to_id["zh_CN"]
    )
    return tokenizer_translate_en.batch_decode(generated_tokens, skip_special_tokens=True)


model_translate = MBartForConditionalGeneration.from_pretrained("SnypzZz/Llama2-13b-Language-translate")
tokenizer_translate_en = MBart50TokenizerFast.from_pretrained("SnypzZz/Llama2-13b-Language-translate", src_lang="en_XX")
tokenizer_translate_zh = MBart50TokenizerFast.from_pretrained("SnypzZz/Llama2-13b-Language-translate", src_lang="zh_CN")

model_size = "large-v2"

# Run on GPU with FP16
model_speech2text = WhisperModel(model_size, device="cuda", compute_type="float16")

mc = mergely.Mergely("791d791feadc6eaceba1f61b4cf5b2f6b43ebb02fc90164ee18af3eebc6902a8")

while True:
    jobs = mc.batch_query_jobs('speech2text', 'allocated', 1, 20)
    if len(jobs['data']['jobs'])<1:
        sleep(1)

    for item in jobs["data"]["jobs"]:
        if item["status"] == "pending" or item["status"] == "allocated":
            if item["biz"] == "translate_zh2en":
                input_param = json.loads(item["input_param"])
                result = translate_zh2en(input_param["text"])
                mc.report_job_result({
                    "uuid": item["uuid"],
                    "result": result
                })
            elif item["biz"] == "translate_en2zh":
                input_param = json.loads(item["input_param"])
                result = translate_en2zh(input_param["text"])
                mc.report_job_result({
                    "uuid": item["uuid"],
                    "result": result
                })
            elif item["biz"] == "speech2text":
                input_param = json.loads(item["input_param"])
                result = handle_speech2text(input_param["file"])
                mc.report_job_result({
                    "uuid": item["uuid"],
                    "result": result
                })
            else:
                # TODO: Add implementation
                pass
    sys.exit(0)
