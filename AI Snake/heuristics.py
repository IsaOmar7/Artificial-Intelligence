import utils
from agent import State


def manhattan_distance(state: State):
    head = state.board.snake[0]
    fruit = state.board.fruit_location
    return utils.manhattan_d(head, fruit)


def weighed_compact_heuristics(state: State):
    manhattan = manhattan_distance(state)
    squareness = utils.squareness(state.board.snake)
    compactness = utils.compactness(state.board.snake)
    connectivity = utils.connectivity(state.board)
    dead_end = utils.dead_end(state.board)

    return manhattan + 4 * squareness + 4 * compactness + 3 * connectivity + 3 * dead_end
