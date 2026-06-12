package api

const (
	TURING_TEAM_ID   = 1
	LOVELACE_TEAM_ID = 2

	SETUP_PHASE  = "setup_placement"
	PLAYER_PHASE = "player_turn"
)

type Cell struct {
	Level     int     `json:"level"`
	Professor *string `json:"professor"`
}

type Position struct {
	Row int `json:"row"`
	Col int `json:"col"`
}

type AITurnRequest struct {
	GameID           string   `json:"game_id"`
	TurnNumber       int      `json:"turn_number"`
	TurnPhase        string   `json:"turn_phase"`
	YourTeam         int      `json:"your_team"` // 1 = TURING, 2 = LOVELACE
	Board            [][]Cell `json:"board"`
	ProfessorToPlace *string  `json:"professor_to_place"`
}

type SetupResponse struct {
	Row int `json:"row"`
	Col int `json:"col"`
}

type PlayerTurnResponse struct {
	Professor string    `json:"professor"`
	MoveTo    Position  `json:"move_to"`
	MentorAt  *Position `json:"mentor_at,omitempty"`
}
