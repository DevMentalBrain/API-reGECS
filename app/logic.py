from schemas import GameState, Move, Position

def choose_setup(board):
    pass

def choose_turn(board, team_id):
    state = GameState(
        board=board,
        current_player=team_id
    )
    pass

#Função que procura os professores e ve onde eles estão no tabuleiro
def get_my_professors(state):
    professors = []

    team_name = (
        "TURING"
        if state.current_player == 1
        else "LOVELACE"
    )

    for row in range(5):
        for col in range(5):

            cell = state.board[row][col]

            if (
                cell.professor is not None
                and team_name in cell.professor
            ):
                professors.append({
                    "name": cell.professor,
                    "row": row,
                    "col": col
                })

    return professors

#Função que valida os proximos passos do professor
def get_valid_moves_for_professor(state, row, col):

    valid_moves = []

    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1)
    ]

    for dr, dc in directions:

        new_row = row + dr
        new_col = col + dc

        if not (0 <= new_row < 5 and 0 <= new_col < 5):
            continue

        cell = state.board[new_row][new_col]

        if cell.level == 4:
            continue

        if cell.professor is not None:
            continue

        valid_moves.append(
            Position(
                row=new_row,
                col=new_col
            )
        )

    return valid_moves


# Função que gera as proximas jogadas
def generate_moves(state) -> list[Move]:
    moves = []

    # vamos implementar depois

    return moves