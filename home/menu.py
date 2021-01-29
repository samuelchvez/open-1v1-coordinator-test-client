from tabulate import tabulate
from utils.logo import LOGO
from utils.configurations_manager import ConfigurationsManager
from utils.consumers.users_consumer import UsersConsumer
from utils.consumers.tournaments_consumer import TournamentsConsumer
from utils import logger
from utils.tables import get_tournaments_table


unregistered_options = '''Welcome, please select an option:
  1. Register user
  2. Exit
'''

registered_options = '''Welcome again {}!, please select an option:
  1. Register to tournament
  2. Join tournament
  3. Create tournament
  4. Exit
'''

def build_menu(is_registered, registered_user):
    return '\n'.join([
        logger.log_title("Homepage"),
        registered_options.format(registered_user['nickname']) if is_registered else unregistered_options
    ])

def start():
    print(LOGO)

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

    users_consumer.authorize(config.get('token'))
    tournaments_consumer.authorize(config.get('token'))

    registered_user = users_consumer.get_user(
        config.get('userid')
    )
    is_registered = registered_user is not None

    while wants_to_be_in_home:
        print(build_menu(is_registered, registered_user))

        selected_option = int(input("> Input: "))

        if not is_registered:
            if selected_option == 1:
                nickname = input("> Nickname: ")
                registered_user = users_consumer.create_user(nickname)
                is_registered = True
                print(logger.log_success("User created successfully!"))
            elif selected_option == 2:
                wants_to_be_in_home = False
            else:
                print(logger.log_error("Invalid option"))
        else:
            if selected_option == 1:
                tournaments = tournaments_consumer.get_tournaments_by_status('CREATED')

                if len(tournaments) > 0:
                    headers, table = get_tournaments_table(tournaments)
                    print("\nSelect the desired tournament index to register:")
                    print(tabulate(table, headers, tablefmt='pretty'))
                    tournament_index = int(input(f"> Tournament (0 - {len(tournaments) - 1}): "))

                    if 0 <= tournament_index < len(tournaments):
                        selected_tournament = tournaments[tournament_index]
                    else:
                        print(logger.log_error("Invalid option"))
                else:
                    print(logger.log_error('No tournaments available'))
            elif selected_option == 2:
                tournaments = tournaments_consumer.get_tournaments_by_status('OPEN')

                if len(tournaments) > 0:
                    headers, table = get_tournaments_table(tournaments)
                    print("\nSelect the desired tournament index to join:")
                    print(tabulate(table, headers, tablefmt='pretty'))
                    tournament_index = int(input(f"> Tournament (0 - {len(tournaments) - 1}): "))

                    if 0 <= tournament_index < len(tournaments):
                        selected_tournament = tournaments[tournament_index]
                    else:
                        print(logger.log_error("Invalid option"))
                else:
                    print(logger.log_error('No tournaments available'))
            elif selected_option == 3:
                title = input("> Title: ")
                gameId = 'tictactoe@0.0.1'
                tournaments_consumer.create_tournament(
                    title,
                    gameId
                )
            elif selected_option == 4:
                wants_to_be_in_home = False
            else:
                print(logger.log_error("Invalid option"))
