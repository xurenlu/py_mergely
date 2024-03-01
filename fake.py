from time import sleep

import mergely
# from faster_whisper import WhisperModel
import requests
import os
import sys
import json


# from transformers import MBartForConditionalGeneration, MBart50TokenizerFast


def handle_speech2text(url):
    target = []
    target.append({"start": 0, "end": 1, "text": "hello"})
    target.append({"start": 1, "end": 2, "text": "world"})
    return target


# model_translate = MBartForConditionalGeneration.from_pretrained("SnypzZz/Llama2-13b-Language-translate")
# tokenizer_translate_en = MBart50TokenizerFast.from_pretrained("SnypzZz/Llama2-13b-Language-translate", src_lang="en_XX")
# tokenizer_translate_zh = MBart50TokenizerFast.from_pretrained("SnypzZz/Llama2-13b-Language-translate", src_lang="zh_CN")
#
# model_size = "large-v2"
#
# # Run on GPU with FP16
# model_speech2text = WhisperModel(model_size, device="cuda", compute_type="float16")

mc = mergely.Mergely("e369b1f961f78122733ec9d3e8a288eb6a4de3cc21732539d3e2c5c860383512",
                     "http://localhost:3000/api/v3/")

while True:
    jobs = mc.batch_query_jobs('speech2text', 'pending', 0, 20)
    if len(jobs["data"]["jobs"]) < 1:
        print("No job allocated, sleep 1s")
        sleep(1)

    for item in jobs["data"]["jobs"]:
        if item["status"] == "pending" or item["status"] == "allocated":
            if item["biz"] == "speech2text":
                input_param = json.loads(item["input_param"])
                result = handle_speech2text(input_param["file"])

                mc.report_job_result({
                    "uuid": item["uuid"],
                    "result": json.dumps(result)
                })
            else:
                # TODO: Add implementation
                pass
    sys.exit(0)
