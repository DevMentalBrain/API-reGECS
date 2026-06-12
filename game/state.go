package game

import "github.com/DevMentalBrain/API-reGECS/mcts"

type Move struct {
	ProfIndex int8 // 0 - 3  (4 Professors)
	MoveTo    int8 // 0 - 24 (25 positions)
	MentorAt  int8 // 0 - 24 (25 positions)
}

type State struct {
	// Board positions levels (1D array)
	// values: 0 - 3 (Years) and 4 (Graduated/Blocked)
	Board [BOARD_SIZE]int8

	// Professors positions
	// 0 and 1 belongs to player 1 (we)
	// 2 and 3 belongs to player 2 (opponent)
	Professors [PROFESSORS_COUNT]int8

	IsOurTurn bool
}

func NewMove(profIndex, moveTo, mentorAt int8) Move {
	return Move{ProfIndex: profIndex, MoveTo: moveTo, MentorAt: mentorAt}
}

func NewState(board [BOARD_SIZE]int8, profs [PROFESSORS_COUNT]int8, isOurTurn bool) State {
	return State{Board: board, Professors: profs, IsOurTurn: isOurTurn}
}

func (s State) GetMoves() []Move {
	moves := make([]Move, 0, 64) // preallocate

	// get moves for current player only
	var start, end int8
	if s.IsOurTurn {
		start = 0
		end = OUR_LAST_PROFESSOR_INDEX + 1
	} else {
		start = OUR_LAST_PROFESSOR_INDEX + 1
		end = PROFESSORS_COUNT
	}

	for i := start; i < end; i++ {
		currBoardIdx := s.Professors[i]
		currentLevel := s.Board[currBoardIdx]
		neighbours := AdjacencyMap[currBoardIdx].Elements
		neighboursCount := AdjacencyMap[currBoardIdx].Count

		for j := range neighboursCount {
			futureBoardIdx := neighbours[j]
			futurePositionLevel := s.Board[futureBoardIdx]

			// Level check
			if futurePositionLevel > currentLevel+1 || futurePositionLevel == GRADUATED {
				continue
			}

			// Victory check
			if futurePositionLevel == YEAR_4 {
				// mentorAt is the index of the position where the professor was before
				// just to avoid an invalid move and finish the simulation
				moves = append(moves, NewMove(i, futureBoardIdx, currBoardIdx))
				continue
			}

			// Block check
			isBlocked := false
			for k := range int8(PROFESSORS_COUNT) {
				// skip the current professor position
				if k == i {
					continue
				}

				if futureBoardIdx == s.Professors[k] {
					isBlocked = true
					break
				}
			}

			if isBlocked {
				continue
			}

			// Promotion check
			promotions := AdjacencyMap[futureBoardIdx].Elements
			promotionsCount := AdjacencyMap[futureBoardIdx].Count

			for k := range promotionsCount {
				promotionIdx := promotions[k]

				// Level check
				promotionPositionLevel := s.Board[promotionIdx]
				if promotionPositionLevel == GRADUATED {
					continue
				}

				// Block check
				isBlocked = false
				for l := range int8(PROFESSORS_COUNT) {
					// let promote the current professor position
					if l == i {
						continue
					}

					if promotionIdx == s.Professors[l] {
						isBlocked = true
						break
					}
				}

				if isBlocked {
					continue
				}

				moves = append(moves, NewMove(i, futureBoardIdx, promotionIdx))
			}
		}
	}

	return moves
}

func (s State) CloneAndApplyMove(move Move) mcts.State[Move] {
	newState := s // deep copy

	newState.Professors[move.ProfIndex] = move.MoveTo
	newState.Board[move.MentorAt]++
	newState.IsOurTurn = !newState.IsOurTurn

	return newState
}

func (s State) GetResult() int8 {
	for i := range int8(PROFESSORS_COUNT) {
		currBoardIdx := s.Professors[i]
		currPositionLevel := s.Board[currBoardIdx]
		isOurProfessor := i <= OUR_LAST_PROFESSOR_INDEX

		if currPositionLevel == YEAR_4 {
			if isOurProfessor {
				return RESULT_WIN
			} else {
				return RESULT_LOSS
			}
		}
	}

	return RESULT_IN_PROGRESS
}

func (s State) IsTerminal() bool {
	return s.GetResult() != RESULT_IN_PROGRESS
}
