import json
from datetime import datetime
from http import HTTPStatus
from urllib.parse import urlencode

import requests

from omnisend import ClientException

DEFAULT_BASE_URL = 'https://api.omnisend.com/'
API_VERSION_3 = 'v3'


class Omnisend:
    # public key
    api_key: str

    # mistertango api endpoint
    api_url: str

    def __init__(self, api_key, api_url=None):
        self.api_key = api_key
        self.api_url = api_url or DEFAULT_BASE_URL + API_VERSION_3

    def _prepare_headers(self):
        return {
            'X-API-KEY': self.api_key,
            # 'Content-Type': 'application/x-www-form-urlencoded'
        }

    def _generate_url(self, endpoint):
        return self.api_url + endpoint

    def _send_request(self, endpoint: str, data: dict):
        post_params = urlencode(data)

        headers = self._prepare_headers()
        r = requests.post(self._generate_url(endpoint), headers=headers, data=post_params)
        if r.status_code != HTTPStatus.OK:
            raise ClientException('Omnisend error: {}'.format(r.text))

        return json.loads(r.text)

    def create_contact(self, contact_info: dict):
        endpoint = '/contacts'
        if 'email' not in contact_info:
            raise AttributeError('Email field is required')

        if 'status' not in contact_info:
            contact_info['status'] = 'subscribed'

        if 'statusDate' not in contact_info:
            contact_info['statusDate'] = datetime.utcnow().isoformat()


        result = self._send_request(endpoint, contact_info)
