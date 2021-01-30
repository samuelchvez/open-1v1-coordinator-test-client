from dataclasses import dataclass
from http import HTTPStatus
import json
import requests

from .resource import Resource
from .auth import BearerAuth


class TournamentsConsumer(Resource):
    def get_tournament(self, tournament_id):
        if self.is_auth:
            response = requests.get(
                self.build_url(tournament_id),
                auth=BearerAuth(self.token)
            )

            if response.status_code == HTTPStatus.OK:
                return json.loads(response.text)

            return None

        raise Exception('Unauthorized')

    def get_tournaments_by_status(self, status):
        if self.is_auth:
            response = requests.get(
                self.build_url(f'?status={status}'),
                auth=BearerAuth(self.token)
            )

            if response.status_code == HTTPStatus.OK:
                return json.loads(response.text)

            return []

        raise Exception('Unauthorized')

    # TODO: handle rules (matching schema, rounds, etc)
    def create_tournament(self, title, game_id):
        if self.is_auth:
            response = requests.post(
                self.build_url(),
                auth=BearerAuth(self.token),
                json={
                    'title': title,
                    'gameId': game_id,
                },
            )

            if response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
                return json.loads(response.text)

            raise Exception(response.status_code, response.text)

        raise Exception('Unauthorized')

    def open_tournament(self, tournament_id):
        if self.is_auth:
            response = requests.patch(
                self.build_url(f'{tournament_id}/open'),
                auth=BearerAuth(self.token),
            )

            if response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
                return json.loads(response.text)

            raise Exception(response.status_code, response.text)

        raise Exception('Unauthorized')

    def start_tournament(self, tournament_id):
        if self.is_auth:
            response = requests.patch(
                self.build_url(f'{tournament_id}/start'),
                auth=BearerAuth(self.token),
            )

            if response.status_code in [HTTPStatus.OK, HTTPStatus.CREATED]:
                return json.loads(response.text)

            raise Exception(response.status_code, response.text)

        raise Exception('Unauthorized')


@dataclass
class TournamentStatus:
    created:str = 'CREATED'
    open:str = 'OPEN'
    playing:str = 'PLAYING'
    completed:str = 'COMPLETED'
