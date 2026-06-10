package game

// Board info
const (
	ROW_SIZE            = 5
	COL_SIZE            = 5
	BOARD_SIZE          = ROW_SIZE * COL_SIZE
	MAX_ADJACENCY_COUNT = 8
)

// Professors info
const (
	PROFESSORS_COUNT         = 4
	OUR_LAST_PROFESSOR_INDEX = 1
)

// Results enum
const (
	RESULT_WIN         = 1
	RESULT_IN_PROGRESS = 0
	RESULT_LOSS        = -1
)

// Position levels enum
const (
	YEAR_1 = iota
	YEAR_2
	YEAR_3
	YEAR_4
	GRADUATED
)
