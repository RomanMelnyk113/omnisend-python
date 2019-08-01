import json
from http import HTTPStatus
from typing import Tuple, Union

import requests
from marshmallow import ValidationError

from omnisend.models import Contact

DEFAULT_BASE_URL = "https://api.omnisend.com/"
API_VERSION_3 = "v3"


class Omnisend:
    # public key
    api_key: str
    api_url: str
    errors: dict

    def __init__(self, api_key, api_url=None):
        self.api_key = api_key
        self.api_url = api_url or DEFAULT_BASE_URL + API_VERSION_3

    def _prepare_headers(self):
        return {"X-API-KEY": self.api_key}

    def _generate_url(self, endpoint):
        return self.api_url + endpoint

    def _clear_errors(self):
        self.errors = {}

    def _send_request(self, endpoint: str, data: dict = None, method="post") -> dict:
        kwargs = {"headers": self._prepare_headers()}
        func = getattr(requests, method)
        if method == "post":
            kwargs["json"] = data

        r = func(self._generate_url(endpoint), **kwargs)
        res = json.loads(r.text)
        if r.status_code != HTTPStatus.OK:
            # raise ClientException("Omnisend error: {}".format(r.text))
            self.errors = res

        return res

    def create_contact(self, data: dict) -> Tuple[Union[dict, None], Union[dict, None]]:
        """
        Create new contact from provided data
        More details can be found here
        https://api-docs.omnisend.com/v3/contacts/create-contacts

        :type data: dict - new contact data
        """

        self._clear_errors()
        endpoint = "/contacts"
        contact_schema = Contact()
        try:
            result = contact_schema.dump(data)
        except ValidationError as err:
            self.errors = err.messages
            return None, self.errors

        response = self._send_request(endpoint, data=result, method="post")
        return (None, self.errors) if self.errors else (response, None)
