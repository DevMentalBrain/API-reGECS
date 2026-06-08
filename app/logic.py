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

#Função que valida os proximos passos possiveis do professor
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

#Função que valida qual o aluno que o professor pode subir de ano
def get_valid_mentors(state, row, col):

    mentors = []

    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1)
    ]

    for dr, dc in directions:

        mentor_row = row + dr
        mentor_col = col + dc

        if not (0 <= mentor_row < 5 and 0 <= mentor_col < 5):
            continue

        cell = state.board[mentor_row][mentor_col]

        # Não pode ter professor
        if cell.professor is not None:
            continue

        # Não pode ser graduado
        if cell.level == 4:
            continue

        mentors.append(
            Position(
                row=mentor_row,
                col=mentor_col
            )
        )

    return mentors

#Função para ter todos os movimentos possiveis do professor
def generate_moves(state):

    moves = []

    professors = get_my_professors(state)

    for professor in professors:

        valid_positions = get_valid_moves_for_professor(
            state,
            professor["row"],
            professor["col"]
        )

        for position in valid_positions:

            mentors = get_valid_mentors(
                state,
                position.row,
                position.col
            )

            for mentor in mentors:

                moves.append(
                    Move(
                        professor=professor["name"],
                        move_to=position,
                        mentor_at=mentor
                    )
                )

    return moves

#Proximo movimento do professor, contendo para onde ele foi e qual aluno subiu
def apply_move(state, move):

    new_state = deepcopy(state)

    old_row = None
    old_col = None

    # encontra professor
    for row in range(5):
        for col in range(5):

            cell = new_state.board[row][col]

            if cell.professor == move.professor:
                old_row = row
                old_col = col
                break

    # remove da posição antiga
    new_state.board[old_row][old_col].professor = None

    # coloca na nova posição
    new_state.board[
        move.move_to.row
    ][
        move.move_to.col
    ].professor = move.professor

    # aplica mentoria
    mentor_cell = new_state.board[
        move.mentor_at.row
    ][
        move.mentor_at.col
    ]

    mentor_cell.level += 1

    return new_state