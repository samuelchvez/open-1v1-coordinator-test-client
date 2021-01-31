import copy

from utils import logger


CELLS = {
    'player1': 1,
    'player2': -1,
    'no_player': 0,
}

REVERSE_CELLS = {
    1: 'X',
    -1: 'O',
    0: ' ',
}

PLAYER_PIECES = {
    1: 'X',
    2: 'O',
}

PLAYERS = {
    1: 'player1',
    2: 'player2',
}


get_cell = lambda game_cell, row_number, col_number: (
    f' {str(row_number * 3 + col_number)} '
        if game_cell == CELLS['no_player']
        else f' {REVERSE_CELLS[game_cell]} '
)


get_row = lambda game_row, row_number: '|'.join(
    get_cell(game_row[i], row_number, i) for i in range(len(game_row))
)


get_board = lambda game_state: '\n--- --- ---\n'.join(
    get_row(game_state[i], i) for i in range(len(game_state))
)


get_playing_piece = lambda next_turn: f"Playing piece: {PLAYER_PIECES[next_turn]}"


get_interface = lambda match_id, game_state, next_turn: '\n'.join([
    logger.log_title(f"Playing match: {match_id}") if match_id is not None else '',
    get_board(game_state),
    '',
    logger.log_info(get_playing_piece(next_turn)) if next_turn is not None else ''
])


def get_move(game_state, next_turn):
    move = int(input("> Movement (0, 8): "))

    if 0 <= move < 9:
        row, col = divmod(move, 3)
        
        if game_state[row][col] == CELLS['no_player']:
            return move

    return None


def update_game(game_state, next_turn, move):
    if 0 <= move < 9:
        row, col = divmod(move, 3)
        new_state = copy.deepcopy(game_state)
        new_state[row][col] = CELLS[PLAYERS[next_turn]]

        return new_state

    return game_state
