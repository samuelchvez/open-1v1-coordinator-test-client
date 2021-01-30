from utils.logo import LOGO
from utils.configurations_manager import ConfigurationsManager
from utils.consumers.users_consumer import UsersConsumer
from utils.consumers.tournaments_consumer import TournamentsConsumer
from utils.consumers.tournament_players_consumer import TournamentPlayersConsumer
from . import menu_options as menu
from utils import logger


unregistered_options = '''Welcome, please select an option:
  1. Register user
  2. Exit
'''

registered_options = '''Please select an option:
  1. Register to tournament
  2. Open tournament
  3. Join tournament
  4. Start tournament
  5. Create tournament
  6. Exit
'''

def render(is_registered):
    return '\n'.join([
        logger.log_title("Homepage"),
        registered_options if is_registered else unregistered_options
    ])


def start():
    wants_to_be_in_home = True
    config = ConfigurationsManager()
    users_consumer = UsersConsumer(
        endpoint=config.get('api'),
        path='users'
    )
    tournaments_consumer = TournamentsConsumer(
        endpoint=config.get('api'),
        path='tournaments'
    )
    tournament_players_consumer = TournamentPlayersConsumer(
        endpoint=config.get('api'),
        path='tournament-player-registries'
    )

    users_consumer.authorize(config.get('token'))
    tournaments_consumer.authorize(config.get('token'))
    tournament_players_consumer.authorize(config.get('token'))
    registered_user = users_consumer.get_user(config.get('userid'))
    is_registered = registered_user is not None

    if is_registered:
        print(logger.log_subtitle(f"Welcome again {registered_user['nickname']}"))
    else:
        print(logger.log_subtitle("Welcome to the tournament administrative client"))

    print(LOGO)

    while wants_to_be_in_home:
        print(render(is_registered))

        try:
            selected_option = int(input("> Input: "))

            if not is_registered:
                if selected_option == 1:
                    registered_user = menu.register_user()
                    is_registered = True

                elif selected_option == 2:
                    wants_to_be_in_home = False

                else:
                    print(logger.log_error("Invalid option"))
            else:
                if selected_option == 1:
                    menu.register_to_tournament(
                        tournaments_consumer,
                        tournament_players_consumer
                    )

                elif selected_option == 2:
                    menu.open_tournament(
                        registered_user,
                        tournaments_consumer
                    )

                elif selected_option == 3:
                    menu.join_to_tournament(
                        config,
                        tournaments_consumer,
                        tournament_players_consumer,
                    )

                elif selected_option == 4:
                    menu.start_tournament(
                        registered_user,
                        tournaments_consumer
                    )

                elif selected_option == 5:
                    menu.create_tournament(tournaments_consumer)

                elif selected_option == 6:
                    wants_to_be_in_home = False

                else:
                    print(logger.log_error("Invalid option"))

        except Exception as error:
            print(logger.log_error(str(error)))
