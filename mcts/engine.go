package mcts

import (
	"math"
	"math/rand"
)

type State[M any] interface {
	GetMoves() []M
	CloneAndApplyMove(M) State[M]
	GetResult() int8
	IsTerminal() bool
}

type Node[M any] struct {
	State        State[M]
	Parent       *Node[M]
	Children     []*Node[M]
	Move         M
	Visits       int
	Wins         float64
	UntriedMoves []M
}

func NewNode[M any](state State[M], parent *Node[M], Move M) *Node[M] {
	return &Node[M]{
		State:        state,
		Parent:       parent,
		Children:     make([]*Node[M], 0),
		Move:         Move,
		UntriedMoves: state.GetMoves(),
	}
}

func NewRootNode[M any](state State[M]) *Node[M] {
	return &Node[M]{
		State:        state,
		Parent:       nil,
		Children:     make([]*Node[M], 0),
		UntriedMoves: state.GetMoves(),
	}
}

func (n *Node[M]) SelectChild() *Node[M] {
	var bestChild *Node[M]
	bestValue := math.Inf(-1)

	for _, child := range n.Children {
		uctValue := calculateUCT(child)

		if uctValue > bestValue {
			bestValue = uctValue
			bestChild = child
		}
	}

	return bestChild
}

func (n *Node[M]) Expand() *Node[M] {
	lastIdx := len(n.UntriedMoves) - 1
	move := n.UntriedMoves[lastIdx]
	n.UntriedMoves = n.UntriedMoves[:lastIdx]

	nextState := n.State.CloneAndApplyMove(move)
	child := NewNode(nextState, n, move)
	n.Children = append(n.Children, child)

	return child
}

func (n *Node[M]) Rollout(localRand *rand.Rand) State[M] {
	currentState := n.State

	// Play until the game is over
	for !currentState.IsTerminal() {
		moves := currentState.GetMoves()
		if len(moves) == 0 {
			break
		}

		randomMove := moves[localRand.Intn(len(moves))]
		currentState = currentState.CloneAndApplyMove(randomMove)
	}

	return currentState
}

func (n *Node[M]) Backpropagate(terminalState State[M]) {
	current := n

	for current != nil {
		current.Visits++

		if current.Parent != nil {
			current.Wins += float64(current.State.GetResult())
		}

		current = current.Parent
	}
}
