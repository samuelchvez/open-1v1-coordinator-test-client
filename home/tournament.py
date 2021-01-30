import json
from datetime import datetime
from utils.consumers.tournaments_consumer import TournamentsConsumer
from utils.consumers.tournament_players_consumer import TournamentPlayersConsumer
from utils.configurations_manager import ConfigurationsManager
import websockets

from utils import logger


def tournament_title(tournament):
    tournament_created_at = datetime.fromtimestamp(
        tournament['createdAt'] // 1000
    )

    return '\n'.join([
        logger.log_title(f"{tournament['title']} ({tournament['status']})"),
        f"- Game: {tournament['gameId']}",
        "- Rules: roundrobin, 2 rounds each",  # TODO: handle rules
        f"- Created at: {tournament_created_at}\n",
    ])


async def tournament_handler(
    config: ConfigurationsManager,
    tournaments_consumer: TournamentsConsumer,
    tournament_players_consumer: TournamentPlayersConsumer,
    passkey: str,
):
    logger.clear()
    print(logger.log_subtitle("Waiting for connection acceptance"))

    wsurl = f"{config.get('websocket')}/?playerPasskey={passkey}"

    async with websockets.connect(wsurl) as websocket:
        tournament_player_registry = tournament_players_consumer.get_tournament_player_registry_by_passkey(
            passkey,
        )

        tournament = tournaments_consumer.get_tournament(
            tournament_player_registry['tournamentId'],
        )

        print(tournament_title(tournament))
        print(logger.log_info("Waiting to start..."))

        async for message in websocket:
            await tournament_message_handler(message)


async def tournament_message_handler(str_message):
    try:
        message = json.loads(str_message)
    except:
        print(logger.log_error(f"Malformed message {str_message}"))
        return

    if 'type' not in message or 'payload' not in message:
        print(
            logger.log_error(
                f"Message missing type or payload key {str_message}"
            )
        )
        return

    # tournament_id = None
    # match_id = None
    # match_game_state = [
    #     [0, 0, 0],
    #     [0, 0, 0],
    #     [0, 0, 0],
    # ]
    # im_i_player_1 = True

    mtype = message['type']
    mpayload = message['payload']

    if mtype == 'tournament:started':
        print(logger.log_subtitle("Tournament started!"))
