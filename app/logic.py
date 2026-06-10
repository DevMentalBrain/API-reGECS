from app.schemas import GameState, Move, Position, TeamID, PlayerTurnResponse, SetupResponse
from copy import deepcopy
from time import perf_counter

TEAM_PROFESSORS = {
    TeamID.TURING: ["CLARO", "REY"],
    TeamID.LOVELACE: ["KARIN", "BEATRIZ"]
}

DIRECTIONS = (
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),           (0, 1),
    (1, -1),  (1, 0),  (1, 1)
)

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

def get_valid_moves_for_professor(state, row, col):

    valid_moves = []
    board = state.board

    current_level = board[row][col].level

    for dr, dc in DIRECTIONS:

        new_row = row + dr
        new_col = col + dc

        if not (0 <= new_row < 5 and 0 <= new_col < 5):
            continue

        cell = board[new_row][new_col]

        if cell.level == 4:
            continue

        if cell.professor is not None:
            continue

        if cell.level > current_level + 1:
            continue

        valid_moves.append(
            Position(
                row=new_row,
                col=new_col
            )
        )

    return valid_moves

def get_valid_mentors(state, row, col, origin_row=None, origin_col=None):

    mentors = []
    board = state.board

    for dr, dc in DIRECTIONS:

        mentor_row = row + dr
        mentor_col = col + dc

        if not (0 <= mentor_row < 5 and 0 <= mentor_col < 5):
            continue

        cell = board[mentor_row][mentor_col]

        if cell.professor is not None:
            if (
                mentor_row == origin_row
                and mentor_col == origin_col
            ):
                pass
            else:
                continue

        if cell.level == 4:
            continue

        mentors.append(
            Position(
                row=mentor_row,
                col=mentor_col
            )
        )

    return mentors

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
                position.col,
                professor["row"],
                professor["col"]
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

def apply_move(state, move):

    new_board = [
        [cell.model_copy(deep=True) for cell in row]
        for row in state.board
    ]

    new_state = GameState(
        board=new_board,
        current_player=state.current_player,
        root_player=state.root_player,
        winner=state.winner
    )

    professor_row = None
    professor_col = None

    board = new_state.board

    found = False

    for row in range(5):
        for col in range(5):

            if board[row][col].professor == move.professor:

                professor_row = row
                professor_col = col
                found = True
                break

        if found:
            break

    destination = board[
        move.move_to.row
    ][
        move.move_to.col
    ]

    if destination.level == 3:
        new_state.winner = new_state.current_player

    board[
        professor_row
    ][
        professor_col
    ].professor = None

    destination.professor = move.professor

    if new_state.winner is None:

        mentor_cell = board[
            move.mentor_at.row
        ][
            move.mentor_at.col
        ]

        mentor_cell.level += 1

        if mentor_cell.level > 4:
            mentor_cell.level = 4

    if new_state.current_player == TeamID.TURING:
        new_state.current_player = TeamID.LOVELACE
    else:
        new_state.current_player = TeamID.TURING

    return new_state

def evaluate(state):

    if state.winner == state.root_player:
        return 100000

    if state.winner is not None:
        return -100000

    score = 0
    board = state.board

    my_professors = TEAM_PROFESSORS[state.root_player]

    enemy_team = (
        TeamID.LOVELACE
        if state.root_player == TeamID.TURING
        else TeamID.TURING
    )

    enemy_professors = TEAM_PROFESSORS[enemy_team]

    moves = generate_moves(state)

    # Mobilidade (peso baixo)
    score += len(moves)

    level3_positions = []

    for row in range(5):
        for col in range(5):

            cell = board[row][col]

            if cell.level == 3:
                score += 300
                level3_positions.append((row, col))

            elif cell.level == 2:
                score += 40

            elif cell.level == 4:
                score += 10

    # Vitória imediata
    for move in moves:

        destination = board[
            move.move_to.row
        ][
            move.move_to.col
        ]

        if destination.level == 3:
            score += 20000

    # Distância para casas vencedoras
    for row in range(5):
        for col in range(5):

            professor = board[row][col].professor

            if professor is None:
                continue

            if not level3_positions:
                continue

            best_dist = min(
                abs(row-r) + abs(col-c)
                for r, c in level3_positions
            )

            if professor in my_professors:

                score += (10 - best_dist) * 80

            elif professor in enemy_professors:

                score -= (10 - best_dist) * 80

    return score

def is_terminal(state, depth):

    if state.winner is not None:
        return True

    if depth >= 2:
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

    moves = generate_moves(state)

    print("MOVES:", len(moves))

    if not moves:
        return None

    best_move = None
    best_score = float("-inf")

    for move in moves:

        new_state = apply_move(state, move)

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