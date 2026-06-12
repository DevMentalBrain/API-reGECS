package api

import (
	"encoding/json"
	"net/http"
	"time"

	"github.com/DevMentalBrain/API-reGECS/game"
	"github.com/DevMentalBrain/API-reGECS/mcts"
)

const THINK_TIME = 4100 * time.Millisecond

func HealthHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodGet {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}
	w.WriteHeader(http.StatusOK)
	w.Write([]byte("READY"))
}

func MoveHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req AITurnRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	state := RequestToState(req)

	if req.TurnPhase == SETUP_PHASE {
		row, col := game.HandleSetupPhase(state.Professors)
		response := SetupResponse{Row: row, Col: col}
		json.NewEncoder(w).Encode(response)
		return
	}

	bestMove := mcts.Search(state, THINK_TIME)
	isWinningMove := state.Board[bestMove.MoveTo] == game.YEAR_4
	response := MoveToResponse(bestMove, req.YourTeam, isWinningMove)

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(response)
}
