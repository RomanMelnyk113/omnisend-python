import json
from http import HTTPStatus
from typing import Tuple, Union

import requests
from marshmallow import Schema, ValidationError

from omnisend.models import Cart, Contact, Order

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

    def send_request(
        self, endpoint: str, schema: "Schema()", data: dict = None, method="post"
    ) -> Tuple[Union[dict, None], Union[dict, None]]:
        self._clear_errors()
        schema = schema()
        try:
            result = schema.dump(data)
        except ValidationError as err:
            self.errors = err.messages
            return None, self.errors

        response = self._send_request(endpoint, result, method=method)
        return (None, self.errors) if self.errors else (response, None)

    def create_contact(self, data: dict) -> Tuple[Union[dict, None], Union[dict, None]]:
        """
        Create new contact from provided data
        More details can be found here
        https://api-docs.omnisend.com/v3/contacts/create-contacts

        :type data: dict - new contact data
        """

        endpoint = "/contacts"
        return self.send_request(endpoint, schema=Contact, data=data, method="post")

    def get_contact(self, contact_id: str):
        pass

    def create_cart(self, data: dict) -> Tuple[Union[dict, None], Union[dict, None]]:
        """
        Create new cart
        More details can be found here:
        https://api-docs.omnisend.com/v3/carts/create-new-cart
        :param cart_info:
        :return:
        """
        endpoint = "/carts"
        return self.send_request(endpoint, schema=Cart, data=data, method="post")

    def get_cart(self, cart_id: str) -> Tuple[Union[dict, None], Union[dict, None]]:
        self._clear_errors()
        endpoint = "/carts/{}".format(cart_id)
        return self.send_request(endpoint, schema=Cart, method="get")

    def update_cart(self, cart_id: str, data: dict):
        self._clear_errors()
        endpoint = "/carts/{}".format(cart_id)
        return self.send_request(endpoint, schema=Cart, data=data, method="patch")

    def replace_cart(self, cart_id: str, data: dict):
        self._clear_errors()
        endpoint = "/carts/{}".format(cart_id)
        return self.send_request(endpoint, schema=Cart, data=data, method="put")

    def replace_cart_product(self, cart_id: str, cart_product_id: str, data: dict):
        self._clear_errors()
        endpoint = "/carts/{}/products/{}".format(cart_id, cart_product_id)
        return self.send_request(endpoint, schema=Cart, data=data, method="put")

    def create_order(self, data: dict) -> Tuple[Union[Cart, None], Union[dict, None]]:
        """
        Create new order
        More details can be found here:
        https://api-docs.omnisend.com/v3/orders/create-new-order
        :param data:
        :return:
        """
        endpoint = "/orders"
        return self.send_request(endpoint, schema=Order, data=data, method="post")
