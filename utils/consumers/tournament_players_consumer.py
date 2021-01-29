from http import HTTPStatus
import json
import requests

from .resource import Resource
from .auth import BearerAuth


class TournamentPlayersConsumer(Resource):
    def get_tournament_player_registry(self, tournament):
        if self.is_auth:
            response = requests.get(
                self.build_url(tournament),
                auth=BearerAuth(self.token)
            )

            if response.status_code == HTTPStatus.OK:
                return json.loads(response.text)

            return None

        raise Exception('Unauthorized')

    def register_player(self, tournament_id, passkey):
        if self.is_auth:
            response = requests.post(
                self.build_url(tournament_id),
                auth=BearerAuth(self.token),
                json={
                    'playerPasskey': passkey,
                },
            )

            if response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
                return json.loads(response.text)

            raise Exception(response.status_code, response.text)

        raise Exception('Unauthorized')