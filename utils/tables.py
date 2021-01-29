from datetime import datetime


def get_tournaments_table(tournaments):
    table = []

    for i in range(len(tournaments)):
        tournament = tournaments[i]
        table.append(
            [
                i,
                tournament['title'],
                tournament['gameId'],
                datetime.fromtimestamp(
                    tournament['createdAt'] / 1000
                ),
                tournament['status']
            ]
        )

    return (
        ['Index', 'Title', 'Game Id', 'Created At', 'Status'],
        table
    )
