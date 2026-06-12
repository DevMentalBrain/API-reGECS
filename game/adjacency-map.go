package game

// stores the neighbors in a static array
// and the count of valid neighbors in the Count field
type AdjacencyList struct {
	Count    int8
	Elements [MAX_ADJACENCY_COUNT]int8
}

var AdjacencyMap [BOARD_SIZE]AdjacencyList

func init() {
	for i := range int8(BOARD_SIZE) {
		// get row and column (2D index) from 1D index
		currRow := i / ROW_SIZE
		currCol := i % COL_SIZE

		var list AdjacencyList

		// iterate over all adjacent cells (including itself)
		for deltaRow := int8(-1); deltaRow <= 1; deltaRow++ {
			for deltaCol := int8(-1); deltaCol <= 1; deltaCol++ {
				// skip itself
				if deltaRow == 0 && deltaCol == 0 {
					continue
				}

				newRow := currRow + deltaRow
				newCol := currCol + deltaCol

				// if neighbor is not out of the board
				if newRow >= 0 && newRow < ROW_SIZE && newCol >= 0 && newCol < COL_SIZE {
					list.Elements[list.Count] = newRow*5 + newCol // return to 1D index
					list.Count++
				}
			}
		}
		AdjacencyMap[i] = list
	}
}
