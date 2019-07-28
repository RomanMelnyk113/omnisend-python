import json
from datetime import datetime
from http import HTTPStatus

import requests

from omnisend import ClientException

DEFAULT_BASE_URL = "https://api.omnisend.com/"
API_VERSION_3 = "v3"


class Omnisend:
    # public key
    api_key: str
    api_url: str

    def __init__(self, api_key, api_url=None):
        self.api_key = api_key
        self.api_url = api_url or DEFAULT_BASE_URL + API_VERSION_3

    def _prepare_headers(self):
        return {"X-API-KEY": self.api_key}

    def _generate_url(self, endpoint):
        return self.api_url + endpoint

    def _send_request(self, endpoint: str, data: dict):
        headers = self._prepare_headers()
        r = requests.post(self._generate_url(endpoint), headers=headers, json=data)
        if r.status_code != HTTPStatus.OK:
            raise ClientException("Omnisend error: {}".format(r.text))

        return json.loads(r.text)

    def create_contact(self, contact_info: dict):
        """
        Create new contact from provided data
        More details can be found here
        https://api-docs.omnisend.com/v3/contacts/create-contacts

        :type contact_info: dict - new contact data
        """
        endpoint = "/contacts"
        if "email" not in contact_info:
            raise AttributeError("Email field is required")

        if "status" not in contact_info:
            contact_info["status"] = "subscribed"

        if "statusDate" not in contact_info:
            contact_info["statusDate"] = datetime.utcnow().strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )
        result = self._send_request(endpoint, contact_info)
        return result

    def get_contact(self, contact_id: str):
        pass
