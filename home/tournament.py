import json
import websockets

from utils import ascii_art
from datetime import datetime
from utils.consumers.tournaments_consumer import TournamentsConsumer
from utils.consumers.tournament_players_consumer import TournamentPlayersConsumer
from utils.configurations_manager import ConfigurationsManager
from utils import logger
from games import tictactoe


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


def waiting_for_match():
    print(logger.log_subtitle("Tournament started!"))
    print(logger.log_info("Waiting for match..."))


async def playing(
    websocket,
    passkey,
    tournament_id,
    match_id,
    game_state,
    next_turn,
):
    turn_success = False

    while not turn_success:
        logger.clear()
        print(tictactoe.get_interface(match_id, game_state, next_turn))
        move = tictactoe.get_move(game_state, next_turn)

        if move is not None:
            print(logger.log_info("Waiting for server to process move..."))

            try:
                await websocket.send(json.dumps({
                    'action': 'move',
                    'payload': {
                        'passkey': passkey,
                        'tournamentId': tournament_id,
                        'matchId': match_id,
                        'move': move,
                    },
                }))

                new_game_state = tictactoe.update_game(
                    game_state,
                    next_turn,
                    move
                )

                logger.clear()
                print(tictactoe.get_interface(match_id, new_game_state, None))

                turn_success = True

                print(logger.log_success("Server accepted the move!"))
                print(logger.log_info("Waiting for player to answer..."))
            except:
                print(logger.log_error("Server rejected the move"))
        else:
            print(logger.log_error("Invalid move"))


async def in_match_results(
    websocket,
    passkey,
    mtype,
    tournament_id,
    match_id,
    game_state,
    next_turn,
):
    set_ready_success = False

    while not set_ready_success:
        logger.clear()

        if mtype == 'match:won':
            print(ascii_art.WON)
        elif mtype == 'match:lost':
            print(ascii_art.LOST)
        elif mtype == 'match:draw':
            print(ascii_art.DRAW)

        print(tictactoe.get_interface(None, game_state, None))

        try:
            input("> When you are ready, press enter: ")

            await websocket.send(json.dumps({
                'action': 'set-ready',
                'payload': {
                    'passkey': passkey,
                    'tournamentId': tournament_id,
                    'matchId': match_id,
                },
            }))

            print(logger.log_info("Waiting for another match..."))

            set_ready_success = True
        except:
            print(logger.log_success("Server accepted the your status change"))


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
        print(logger.log_info("Waiting for torunament to start..."))

        async for message in websocket:
            await tournament_message_handler(
                websocket,
                passkey,
                message
            )


async def tournament_message_handler(websocket, passkey, str_message):
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

    mtype = message['type']
    mpayload = message['payload']

    if mtype == 'tournament:started':
        waiting_for_match()

    elif mtype == 'match:require_move':
        match  = mpayload['match']

        await playing(
            websocket,
            passkey,
            tournament_id=match['tournamentId'],
            match_id=match['matchId'],
            game_state=json.loads(match['gameState']),
            next_turn=match['nextTurn']
        )

    elif mtype in ['match:won', 'match:lost', 'match:draw']:
        match = mpayload['match']

        await in_match_results(
            websocket,
            passkey,
            mtype=mtype,
            tournament_id=match['tournamentId'],
            match_id=match['matchId'],
            game_state=json.loads(match['gameState']),
            next_turn=match['nextTurn']
        )
