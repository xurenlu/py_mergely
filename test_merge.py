import unittest

from mergely import Mergely, Job


class MyTestCase(unittest.TestCase):

    def test_submit(self):
        client = Mergely('791d791feadc6eaceba1f61b4cf5b2f6b43ebb02fc90164ee18af3eebc6902a8')
        job = Job()
        job.uuid = '123'
        job.biz = 'speech2text'
        job.input_param = {
            'file': 'https://some.com/file'
        }
        resp = client.submit_job(job)
        self.assertEqual(True, resp["ok"])
        print(resp["data"]["uuid"])

        resp_job = client.query_job(resp["data"]["uuid"])
        self.assertEqual(True, resp_job["ok"])

    def test_batch(self):
        client = Mergely('791d791feadc6eaceba1f61b4cf5b2f6b43ebb02fc90164ee18af3eebc6902a8')
        resp = client.batch_query_jobs('speech2text', 'pending', 0, 20)
        self.assertEqual(True, resp["ok"])
        print(resp["data"]["jobs"])
        self.assertEqual(True, len(resp["data"]["jobs"]) > 0)


if __name__ == '__main__':
    unittest.main()
