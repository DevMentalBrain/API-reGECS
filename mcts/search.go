package mcts

import (
	"fmt"
	"math/rand"
	"sync"
	"time"
)

func Search[M any](initialState State[M], maxDuration time.Duration) M {
  numWorkers := 8
	roots := make([]*Node[M], numWorkers)

	stop := make(chan any)
	time.AfterFunc(maxDuration, func() { close(stop) })

	var wg sync.WaitGroup

	for i := range roots {
		wg.Add(1)
		roots[i] = NewRootNode(initialState)

		go func(root *Node[M]) {
			defer wg.Done()

			// Initialize the random number generator
			// to get a different sequence of random numbers for each worker
			localRand := rand.New(rand.NewSource(time.Now().UnixNano()))

		SearchLoop:
			for {
				select {
				case <-stop:
					break SearchLoop
				default:
					// 1. Go forward in the three (if the root has untried moves, stay in the root)
					node := root
					for len(node.UntriedMoves) == 0 && len(node.Children) > 0 {
						node = node.SelectChild()
					}

					// 2. If the game is not over in this node, expand creating a child
					if len(node.UntriedMoves) > 0 && !node.State.IsTerminal() {
						node = node.Expand()
					}

					// 2. Simulate a game from the new child
					terminalState := node.Rollout(localRand)

					// 5. Backpropagate the result
					node.Backpropagate(terminalState)
				}
			}
		}(roots[i])
	}

	wg.Wait()

	globalSimulations := 0
	for _, root := range roots {
		globalSimulations += root.Visits
	}
	fmt.Printf("🧠 Motor Multi-Core desligado: %d simulações conjuntas realizadas.\n", globalSimulations)

	// MCTS rule: pick the node with the most Visits
	// This node is more resistant against the opponent's counter-moves.
	return getMostVisitedChild(roots).Move
}
