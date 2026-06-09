from app.schemas import GameState, Move, Position, TeamID, PlayerTurnResponse, SetupResponse
from copy import deepcopy
from time import perf_counter

TEAM_PROFESSORS = {
    TeamID.TURING: ["CLARO", "REY"],
    TeamID.LOVELACE: ["KARIN", "BEATRIZ"]
}

#Função que procura os professores e ve onde eles estão no tabuleiro
def get_my_professors(state):

    professors = []

    my_professors = TEAM_PROFESSORS[
        state.current_player
    ]

    for row in range(5):
        for col in range(5):

            cell = state.board[row][col]

            if (
                cell.professor is not None
                and cell.professor in my_professors
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

    current_level = state.board[row][col].level

    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1)
    ]

    for dr, dc in directions:

        new_row = row + dr
        new_col = col + dc

        # fora do tabuleiro
        if not (0 <= new_row < 5 and 0 <= new_col < 5):
            continue

        cell = state.board[new_row][new_col]

        # não pode entrar em graduado
        if cell.level == 4:
            continue

        # não pode entrar em casa ocupada
        if cell.professor is not None:
            continue

        # pode subir no máximo 1 nível
        if cell.level > current_level + 1:
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

    professor_row = None
    professor_col = None

    # encontra o professor
    found = False

    for row in range(5):
        for col in range(5):

            if (
                new_state.board[row][col].professor
                == move.professor
            ):
                professor_row = row
                professor_col = col
                found = True
                break

        if found:
            break

    destination = new_state.board[
        move.move_to.row
    ][
        move.move_to.col
    ]

    # verifica vitória ANTES da mentoria
    if destination.level == 3:
        new_state.winner = new_state.current_player

    # remove da posição antiga
    new_state.board[
        professor_row
    ][
        professor_col
    ].professor = None

    # coloca na nova posição
    destination.professor = move.professor

    # só aplica mentoria se não venceu
    if new_state.winner is None:

        mentor_cell = new_state.board[
            move.mentor_at.row
        ][
            move.mentor_at.col
        ]

        mentor_cell.level += 1

        if mentor_cell.level > 4:
            mentor_cell.level = 4

    # troca jogador
    if new_state.current_player == TeamID.TURING:
        new_state.current_player = TeamID.LOVELACE
    else:
        new_state.current_player = TeamID.TURING

    return new_state    

#Heuristica
def evaluate(state):

    # Vitória
    if state.winner == state.root_player:
        return 10000

    # Derrota
    if state.winner is not None:
        return -10000

    score = 0

    # Mobilidade
    score += len(generate_moves(state)) * 10

    for row in range(5):
        for col in range(5):

            cell = state.board[row][col]

            # Casas preparadas para vitória
            if cell.level == 3:
                score += 100

            # Casas quase preparadas
            elif cell.level == 2:
                score += 25

            # Casas graduadas (barreiras)
            elif cell.level == 4:
                score += 5

    # Verifica se existe vitória imediata
    for move in generate_moves(state):

        destination = state.board[
            move.move_to.row
        ][
            move.move_to.col
        ]

        if destination.level == 3:
            score += 5000

    return score

#Função para determinar quando parar
def is_terminal(state, depth):

    if state.winner is not None:
        return True

    if depth >= 3:
        return True

    if len(generate_moves(state)) == 0:
        return True

    return False

def minimax(state, depth, alpha, beta, maximizing):
    global nodes_visited
    nodes_visited += 1
    
    if is_terminal(state, depth):
        return evaluate(state)

    moves = generate_moves(state)

    if maximizing:

        best_score = float("-inf")

        for move in moves:

            new_state = apply_move(
                state,
                move
            )

            score = minimax(
                new_state,
                depth + 1,
                alpha,
                beta,
                False
            )

            best_score = max(
                best_score,
                score
            )

            alpha = max(
                alpha,
                best_score
            )

            if beta <= alpha:
                break

        return best_score

    else:

        best_score = float("inf")

        for move in moves:

            new_state = apply_move(
                state,
                move
            )

            score = minimax(
                new_state,
                depth + 1,
                alpha,
                beta,
                True
            )

            best_score = min(
                best_score,
                score
            )

            beta = min(
                beta,
                best_score
            )

            if beta <= alpha:
                break

        return best_score
    
def get_best_move(state):

    best_move = None
    best_score = float("-inf")

    moves = generate_moves(state)

    for move in moves:

        new_state = apply_move(
            state,
            move
        )

        score = minimax(
            new_state,
            depth=1,
            alpha=float("-inf"),
            beta=float("inf"),
            maximizing=False
        )

        if score > best_score:

            best_score = score
            best_move = move

    return best_move

def choose_setup(board, professor_to_place):

    preferred_positions = [
        (2, 2),
        (2, 1),
        (2, 3),
        (1, 2),
        (3, 2),
    ]

    for row, col in preferred_positions:

        if board[row][col].professor is None:

            return SetupResponse(
                row=row,
                col=col
            )

def choose_turn(board, team_id):
    global nodes_visited
    nodes_visited = 0
    start_time = perf_counter()

    state = GameState(
        board=board,
        current_player=team_id,
        root_player=team_id
    )

    best_move = get_best_move(state)

    end_time = perf_counter()

    print(f"Tempo: {end_time - start_time:.4f}s")
    print(nodes_visited)

    if best_move is None:
        return None
    
    destination = board[
    best_move.move_to.row
    ][
        best_move.move_to.col
    ]

    if destination.level == 3:
        best_move.mentor_at = None

    return PlayerTurnResponse(
        professor=best_move.professor,
        move_to=best_move.move_to,
        mentor_at=best_move.mentor_at
    )