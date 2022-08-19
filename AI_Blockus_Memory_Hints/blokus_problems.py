from board import Board
from search import SearchProblem, ucs
import util


class BlokusFillProblem(SearchProblem):
    """
    A one-player Blokus game as a search problem.
    This problem is implemented for you. You should NOT change it!
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.expanded = 0

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        """
        state: Search state
        Returns True if and only if the state is a valid goal state
        """
        return not any(state.pieces[0])

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, 1) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        return len(actions)


#####################################################
# This portion is incomplete.  Time to write code!  #
#####################################################
class BlokusCornersProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0)):
        self.expanded = 0
        "*** YOUR CODE HERE ***"
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)
        self.targets = [(board_w - 1, board_h - 1), (0, board_w - 1), (board_h - 1, 0)]

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        "*** YOUR CODE HERE ***"
        # checking for every target state if it's empty or not
        if (state.state[0][0] != -1) and (state.state[0][self.board.board_h - 1] != -1) and (
                state.state[self.board.board_w - 1][0] != -1) and (
                state.state[self.board.board_w - 1][self.board.board_h - 1] != -1):
            return True
        return False

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        "*** YOUR CODE HERE ***"
        actions_cost = 0
        for action in actions:
            actions_cost += action.piece.get_num_tiles()
        return actions_cost


def blokus_corners_heuristic(state, problem):
    """
    Your heuristic for the BlokusCornersProblem goes here.

    This heuristic must be consistent to ensure correctness.  First, try to come up
    with an admissible heuristic; almost all admissible heuristics will be consistent
    as well.

    If using A* ever finds a solution that is worse uniform cost search finds,
    your heuristic is *not* consistent, and probably not admissible!  On the other hand,
    inadmissible or inconsistent heuristics may find optimal solutions, so be careful.
    """
    "*** YOUR CODE HERE ***"
    action = state[1]
    curr_state = state[0]
    coord = problem.targets
    empty_corners = 0
    targets = []
    # checking which corners are empty
    for corner in coord:
        x, y = corner
        if curr_state.state[x][y] != -1:
            targets.append(corner)
        else:
            empty_corners += 1
    # taking the coords the piece should be at after we move it
    piece_place = []
    for x, y in action.orientation:
        piece_place.append((x + action.x, y + action.y))
    distance = (problem.board.board_h ** 2 + problem.board.board_w ** 2) ** 0.5
    d_list = []
    for x1, y1 in piece_place:
        for x2, y2 in targets:
            # we use the chebyshev distance to calculate the distance between a given tile and the targets
            # and we take the minimal distance for one of the targets
            curr_distance = chebyshev_distance((x1, y1), (x2, y2))
            if curr_distance < distance:
                distance = curr_distance
        d_list.append(distance)
        distance = (problem.board.board_h ** 2 + problem.board.board_w ** 2) ** 0.5
    return min(d_list)


class BlokusCoverProblem(SearchProblem):
    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=[(0, 0)]):
        self.targets = targets.copy()
        self.expanded = 0
        "*** YOUR CODE HERE ***"
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def is_goal_state(self, state):
        "*** YOUR CODE HERE ***"
        # iterating over the targets and checking if they are empty
        for target in self.targets:
            x, y = target
            if state.state[x, y] == -1:
                return False
        return True

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        # Note that for the search problem, there is only one player - #0
        self.expanded = self.expanded + 1
        return [(state.do_move(0, move), move, move.piece.get_num_tiles()) for move in state.get_legal_moves(0)]

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        "*** YOUR CODE HERE ***"
        actions_cost = 0
        for action in actions:
            actions_cost += action.piece.get_num_tiles()
        return actions_cost


def chebyshev_distance(point1, point2):
    """
    using this formula for calculating the distance between two points
    """
    return max(abs(point1[0] - point2[0]), abs(point1[1] - point2[1]))


def blokus_cover_heuristic(state, problem):
    "*** YOUR CODE HERE ***"
    action = state[1]
    curr_state = state[0]
    coord = problem.targets
    empty_targets = 0
    targets = []
    # checking which targets are empty
    for corner in coord:
        x, y = corner
        if curr_state.state[x][y] != -1:
            targets.append(corner)
        else:
            empty_targets += 1
    # taking the coords the piece should be at after we move it
    piece_place = []
    for x, y in action.orientation:
        piece_place.append((x + action.x, y + action.y))
    distance = (problem.board.board_h ** 2 + problem.board.board_w ** 2) ** 0.5
    d_list = []
    for x1, y1 in piece_place:
        for x2, y2 in targets:
            # we use the chebyshev distance to calculate the distance between a given tile and the targets
            # and we take the minimal distance for one of the targets
            curr_distance = chebyshev_distance((x1, y1), (x2, y2))
            if curr_distance < distance:
                distance = curr_distance
        d_list.append(distance)
        distance = (problem.board.board_h ** 2 + problem.board.board_w ** 2) ** 0.5
    return min(d_list)


def current_move(current_state, sub_path):
    for move in sub_path:
        current_state = current_state.do_move(0, move)
    return current_state


class ClosestLocationSearch:
    """
    In this problem you have to cover all given positions on the board,
    but the objective is speed, not optimality.
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=(0, 0)):
        self.expanded = 0
        self.targets = targets.copy()
        self.board_h = board_h
        self.board_w = board_w
        self.piece_list = piece_list
        self.board = Board(self.board_w, self.board_h, 1, self.piece_list, starting_point)
        self.starting_point = starting_point

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def solve(self):
        """
        This method should return a sequence of actions that covers all target locations on the board.
        This time we trade optimality for speed.
        Therefore, your agent should try and cover one target location at a time. Each time, aiming for the closest uncovered location.
        You may define helpful functions as you wish.

        Probably a good way to start, would be something like this --

        current_state = self.board.__copy__()
        backtrace = []

        while ....

            actions = set of actions that covers the closets uncovered target location
            add actions to backtrace

        return backtrace
        """
        "*** YOUR CODE HERE ***"
        current_state = self.board.__copy__()
        backtrace = []
        self.targets = sorted(self.targets, key=lambda target: util.manhattanDistance(self.starting_point, target))
        for i in range(len(self.targets)):
            sub_problem = BlokusCoverProblem(self.board_w, self.board_h, self.piece_list, self.starting_point,
                                             [self.targets[i]])
            sub_problem.board = current_state
            sub_path = ucs(sub_problem)
            current_state = current_move(current_state, sub_path)
            backtrace += sub_path
            self.expanded += sub_problem.expanded
        return backtrace


class MiniContestSearch:
    """
    Implement your contest entry here
    """

    def __init__(self, board_w, board_h, piece_list, starting_point=(0, 0), targets=(0, 0)):
        self.targets = targets.copy()
        "*** YOUR CODE HERE ***"
        self.board = Board(board_w, board_h, 1, piece_list, starting_point)

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        return self.board

    def solve(self):
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()
