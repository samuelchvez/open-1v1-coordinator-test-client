import asyncio

from utils.configurations_manager import ConfigurationsManager
from tabulate import tabulate

from utils import logger
from utils.tables import get_tournaments_table
from utils.consumers.tournaments_consumer import TournamentStatus
from . import tournament as tmt


tournament_status = TournamentStatus()


def register_user(users_consumer):
    nickname = input("> Nickname: ")
    registered_user = users_consumer.create_user(nickname)
    print(logger.log_success("User created successfully!"))

    return registered_user


def register_to_tournament(tournaments_consumer, tournament_players_consumer):
    tournaments = tournaments_consumer.get_tournaments_by_status(
        tournament_status.created
    )

    if len(tournaments) > 0:
        headers, table = get_tournaments_table(tournaments)
        print("\nSelect the desired tournament index to register:")
        print(tabulate(table, headers, tablefmt='pretty'))
        tournament_index = int(input(f"> Tournament (0 - {len(tournaments) - 1}): "))

        if 0 <= tournament_index < len(tournaments):
            selected_tournament = tournaments[tournament_index]
            tournament_id = selected_tournament['tournamentId']

            if tournament_players_consumer.get_tournament_player_registry(tournament_id) is None:
                result = tournament_players_consumer.register_player(tournament_id)

                print(
                    logger.log_success(
                        f"Registered! don't lose your passkey: {result['playerPasskey']}"
                    )
                )
            else:
                print(logger.log_error("You are already registered in this tournament"))
        else:
            print(logger.log_error("Invalid option"))
    else:
        print(logger.log_error('No tournaments available'))


def open_tournament(registered_user, tournaments_consumer):
    # Filter only my own CREATED tournaments
    tournaments = [
        tournament
        for tournament in tournaments_consumer.get_tournaments_by_status(
            tournament_status.created
        )
        if tournament['createdBy'] == registered_user['userId']
    ]

    if len(tournaments) > 0:
        headers, table = get_tournaments_table(tournaments)
        print("\nSelect the desired tournament index to open it:")
        print(tabulate(table, headers, tablefmt='pretty'))
        tournament_index = int(input(f"> Tournament (0 - {len(tournaments) - 1}): "))

        if 0 <= tournament_index < len(tournaments):
            selected_tournament = tournaments[tournament_index]

            open_tournament = tournaments_consumer.open_tournament(
                selected_tournament['tournamentId']
            )

            headers, table = get_tournaments_table([open_tournament])
            print(logger.log_success("Tournament is now open!"))
            print(tabulate(table, headers, tablefmt='pretty'))
        else:
            print(logger.log_error("Invalid option"))
    else:
        print(logger.log_error('No tournaments available'))


def start_tournament(registered_user, tournaments_consumer):
    # Filter only my own OPEN tournaments
    tournaments = [
        tournament
        for tournament in tournaments_consumer.get_tournaments_by_status(
            tournament_status.open
        )
        if tournament['createdBy'] == registered_user['userId']
    ]

    if len(tournaments) > 0:
        headers, table = get_tournaments_table(tournaments)
        print("\nSelect the desired tournament index to start it:")
        print(tabulate(table, headers, tablefmt='pretty'))
        tournament_index = int(input(f"> Tournament (0 - {len(tournaments) - 1}): "))

        if 0 <= tournament_index < len(tournaments):
            selected_tournament = tournaments[tournament_index]

            started_tournament = tournaments_consumer.start_tournament(
                selected_tournament['tournamentId']
            )

            headers, table = get_tournaments_table([started_tournament])
            print(logger.log_success("Tournament is now started!"))
            print(tabulate(table, headers, tablefmt='pretty'))
        else:
            print(logger.log_error("Invalid option"))
    else:
        print(logger.log_error('No tournaments available'))


def join_to_tournament(
    config,
    tournaments_consumer,
    tournament_players_consumer,
):
    passkey = input("> Passkey: ")

    asyncio.get_event_loop().run_until_complete(
        tmt.tournament_handler(
            config,
            tournaments_consumer,
            tournament_players_consumer,
            passkey
        )
    )


def create_tournament(tournaments_consumer):
    title = input("> Title: ")

    # TODO: handle rules (matching schema, rounds, etc)
    tournaments_consumer.create_tournament(
        title,
        'tictactoe@0.0.1',
    )
    print(logger.log_success(f"Tournament {title} created!"))
