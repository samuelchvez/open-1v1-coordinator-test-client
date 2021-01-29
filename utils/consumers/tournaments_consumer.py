from http import HTTPStatus
import json
import requests

from .resource import Resource
from .auth import BearerAuth


class TournamentsConsumer(Resource):
    def get_tournaments_by_status(self, status):
        if self.is_auth:
            response = requests.get(
                self.build_url(f'?status={status}'),
                auth=BearerAuth(self.token)
            )

            if response.status_code == HTTPStatus.OK:
                return json.loads(response.text)

            return []

        return Exception('Unauthorized')

    def create_tournament(self, title, gameId):
        if self.is_auth:
            response = requests.post(
                self.build_url(),
                auth=BearerAuth(self.token),
                json={
                    'title': title,
                    'gameId': gameId,
                },
            )

            if response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
                return json.loads(response.text)

            raise Exception(response.status_code, response.text)

        raise Exception('Unauthorized')