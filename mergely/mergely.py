import requests
import json
import socket


class MergelyException(Exception):
    pass


class Job:
    uuid: str
    biz: str
    input_param: dict
    status: str
    model: str
    model_version: str
    webhook: str

    def __init__(self):
        self.uuid = ''
        self.biz = ''
        self.input_param = {}
        self.status = ''

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'biz': self.biz,
            'input_param': self.input_param,
            'status': self.status,
            'model': self.model,
            'model_version': self.model_version,
            'web_hook': self.webhook
        }


# 定义如何序列化MyObject类的方法
def serialize(obj):
    if isinstance(obj, Job):
        return obj.to_dict()  # 或者直接使用 {'name': obj.name, 'age': obj.age}
    raise TypeError(f"Type {type(obj)} is not serializable")


END_POINT = "https://console.mergely.app/api/v3/"
VERSION = "1.0.17"


class Mergely:

    def __init__(self, token, ep=END_POINT):
        self.token = token
        self.headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'Application/json',
            'Accept': 'Application/json',
            'User-Agent': f'Mergely-Python-SDK/{VERSION}'
        }
        self.ep = ep

    def submit_job(self, job: Job):
        api = self.ep + 'job/submit'
        body = json.dumps({'job': job}, default=serialize)
        response = requests.post(api, body, headers=self.headers)
        if response.status_code != 200:
            raise MergelyException(response.text)
        return response.json()

    def query_job(self, uuid: str):
        api = self.ep + 'job/query?uuid=' + uuid
        response = requests.get(api, headers=self.headers)
        if response.status_code != 200:
            raise MergelyException(response.text)
        return response.json()

    def batch_query_jobs(self, biz: str, status: str, page: int = 0, page_size: int = 20):
        api = self.ep + 'job/batch/query'
        response = requests.get(api, {
            'biz': biz,
            'status': status,
            'page': page,
            'size': page_size
        }, headers=self.headers)
        if response.status_code != 200:
            raise MergelyException(response.text)
        return response.json()

    def cancel_job(self, uuid: str):
        api = self.ep + 'job/cancel?uuid=' + uuid
        response = requests.get(api, headers=self.headers)
        if response.status_code != 200:
            raise MergelyException(response.text)
        return response.json()

    def report_job_result(self, job: dict):
        api = self.ep + 'job/report'
        body = json.dumps({'job': job})
        response = requests.post(api, body, headers=self.headers)
        if response.status_code != 200:
            raise MergelyException(response.text)
        return response.json()

    def batch_report(self, jobs: []):
        api = self.ep + 'job/batch/report'
        body = json.dumps({'jobs': jobs}, default=serialize)
        response = requests.post(api, body, headers=self.headers)
        if response.status_code != 200:
            raise MergelyException(response.text)
        return response.json()

    def report_fail(self, uuid: str, error: str):
        api = self.ep + 'job/report/fail'
        body = json.dumps({'uuid': uuid, 'reason': error})
        response = requests.post(api, body, headers=self.headers)
        if response.status_code != 200:
            raise MergelyException(response.text)
        return response.json()

    def heartbeat(self, uuid: str):
        api = self.ep + "status/heartbeat"
        body = json.dumps({'uuid': uuid, 'hostname': socket.gethostname()})
        response = requests.post(api, body, headers=self.headers)
        if response.status_code != 200:
            raise MergelyException(response.text)
        return response.json()
