import time
import sys
import hashlib
import mergely
from faster_whisper import WhisperModel
import requests
import os
import json
from transformers import MBartForConditionalGeneration, MBart50TokenizerFast
from zhconv import convert


def check_url_status(url):
    try:
        # 使用HEAD请求方法
        response = requests.head(url)
        # 检查状态码
        return response.status_code == 200
    except requests.RequestException as e:
        # 出现请求错误时输出错误信息
        print(f"Error checking URL: {e}")
        return False

def handle(mp3):
    t1 = time.time()
    segments, info = model_speech2text.transcribe(mp3, beam_size=1)
    t2 = time.time()
    print("transcribe cost: ", t2 - t1)
    target = []
    for segment in segments:
        target.append({"start": segment.start, "end": segment.end, "text": convert(segment.text,"zh-hans")})
    total_time = target[-1]["end"]
    print("ratio:", total_time / (t2 - t1))
    return target


def handle_speech2text(url):
    t1 = time.time()
    md5_hash = hashlib.md5(url.encode()).hexdigest()
    local_url = f'http://localhost/{md5_hash}'

    if check_url_status(local_url):
        real_get_url = local_url
    else:
        real_get_url = url

    r = requests.get(real_get_url, allow_redirects=True)
    mp3_file_path = "/tmp/" + url.split("/")[-1]
    with open(mp3_file_path, 'wb') as f:
        f.write(r.content)
    t2 = time.time()
    print("download cost: ", t2 - t1)
    result = handle(mp3_file_path)
    os.remove(mp3_file_path)
    return result


model_size = "large-v2"
print("try to load model for speech2text")
print(time.time())
# Run on GPU with FP16
model_speech2text = WhisperModel(model_size, device="cuda", compute_type="float16")
print("model loadd")
print(time.time())
mc = mergely.Mergely("791d791feadc6eaceba1f61b4cf5b2f6b43ebb02fc90164ee18af3eebc6902a8")

while True:
    jobs = mc.batch_query_jobs('speech2text', 'pending', 0, 8)
    if len(jobs['data']['jobs'])<1:
        print("no jobs got" )
        time.sleep(1)

    for item in jobs["data"]["jobs"]:
        print(item["id"])
        print(time.time())
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
        print(time.time())
        print("\n")
    sys.exit(0)
