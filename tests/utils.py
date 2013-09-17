# coding: utf-8
import json


class MockResponse(object):

    def __init__(self, content='null', status=200):
        self.status_code = status
        self.content = content

    def json(self):
        return json.loads(self.content)
