package api

import "github.com/DevMentalBrain/API-reGECS/game"

func RequestToState(req AITurnRequest) game.State {
	internalBoard := [game.BOARD_SIZE]int8{}
	internalProfs := [game.PROFESSORS_COUNT]int8{}

	for i, row := range req.Board {
		for j, cell := range row {
			idx := i*game.ROW_SIZE + j // 2D to 1D
			internalBoard[idx] = int8(cell.Level)

			if cell.Professor == nil {
				continue
			}

			profName := *cell.Professor
			internalProfIdx := game.ProfNameToIndex(req.YourTeam, profName)
			internalProfs[internalProfIdx] = int8(idx)
		}
	}

	return game.State{
		Board:      internalBoard,
		Professors: internalProfs,
		IsOurTurn:  true,
	}
}

func MoveToResponse(move game.Move, teamID int, winningMove bool) PlayerTurnResponse {
	profName := game.ProfIndexToName(teamID, move.ProfIndex)
	moveTo := Position{Row: int(move.MoveTo) / 5, Col: int(move.MoveTo) % 5}
	var mentorAt *Position

	if !winningMove {
		mentorAt = &Position{Row: int(move.MentorAt) / 5, Col: int(move.MentorAt) % 5}
	}

	return PlayerTurnResponse{
		Professor: profName,
		MoveTo:    moveTo,
		MentorAt:  mentorAt,
	}
}
