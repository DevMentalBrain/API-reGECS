package game

func HandleSetupPhase(professorsPositions [PROFESSORS_COUNT]int8) (row, col int) {
	// Board center and its corners (1D)
	preferredSpots := []int{12, 11, 13, 7, 17, 6, 8, 16, 18}

PreferedSpotsLoop:
	for _, i := range preferredSpots {
		row := i / 5
		col := i % 5

		for _, pos := range professorsPositions {
			// Skip spots that are already taken
			if pos == int8(i) {
				continue PreferedSpotsLoop
			}
		}

		return row, col
	}

	// Fallback to any open spot
FallbackLoop:
	for i := range int8(BOARD_SIZE) {
		for _, pos := range professorsPositions {
			if pos == i {
				// Skip spots that are already taken
				continue FallbackLoop
			}
		}

		row := i / 5
		col := i % 5
		return int(row), int(col)
	}

	return 0, 0
}
