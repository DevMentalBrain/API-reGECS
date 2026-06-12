package mcts

import "math"

// UCT constant ~= sqrt(2)
// A lower value makes the AI explore more
// A greater value makes the AI focus on the winning path
const C = 1.41421356237

func calculateUCT[M any](node *Node[M]) float64 {
	winRate := node.Wins / float64(node.Visits)

	// The lower the visit count of the child relative to the parent, the higher this number is
	exploration := C * math.Sqrt(math.Log(float64(node.Parent.Visits))/float64(node.Visits))

	return winRate + exploration
}

func getMostVisitedChild[M any](nodes []*Node[M]) *Node[M] {
	totalVisits := make(map[any]int)
	var bestMove *Node[M]
	maxVisits := -1

	for _, node := range nodes {
		for _, child := range node.Children {
			// Uses interface{} as a temporary key to sum equal moves
			moveKey := any(child.Move)
			totalVisits[moveKey] += child.Visits

			if totalVisits[moveKey] > maxVisits {
				maxVisits = totalVisits[moveKey]
				bestMove = child
			}
		}
	}

	return bestMove
}
