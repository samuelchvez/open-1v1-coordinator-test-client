from http import HTTPStatus
import json
import requests

from .resource import Resource
from .auth import BearerAuth


class UsersConsumer(Resource):
    def get_user(self, userid):
        if self.is_auth:
            response = requests.get(
                self.build_url(userid),
                auth=BearerAuth(self.token)
            )

            if response.status_code == HTTPStatus.OK:
                return json.loads(response.text)

            return None

        return Exception('Unauthorized')

    def create_user(self, nickname):
        if self.is_auth:
            response = requests.post(
                self.build_url(),
                auth=BearerAuth(self.token),
                json={
                    'nickname': nickname,
                },
            )

            if response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
                return json.loads(response.text)

            raise Exception(response.status_code, response.text)

        raise Exception('Unauthorized')