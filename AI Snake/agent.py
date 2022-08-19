import copy
import hamiltonian_cycle
from config import Direction
import utils


class State:
    def __init__(self, board, g_heu, heuristic_function, path):
        self.board = board
        if heuristic_function is not None:
            self.h = heuristic_function(self)
        else:
            self.h = 0
        self.g = g_heu
        self.f = self.h + self.g
        self.path = path

    def is_goal(self):
        """
        Checking if we the snake's head got to the location of the fruit
        (if the snake ate the fruit)
        :return: True if the snake ate the fruit, False otherwise
        """
        if self.board.snake[0] == self.board.fruit_location:
            return True
        return False

    def is_legal_move(self, i, j):
        """
        Take indexes of the snake's head coordinates after a move and check if the move is legal
        :param i: The first coordinate of the snake's head
        :param j: The second coordinate of the snake's head
        :return: True of the move is legal,false otherwise
        """
        board_size = self.board.board_size

        i, j = utils.cyclic(i, board_size), utils.cyclic(j, board_size)
        return 0 <= i < board_size and 0 <= j < board_size and (i, j) not in self.board.obstacles and (
            i, j) not in self.board.snake

    def legal_action(self, flag=False):
        """
        Returns the legal actions of the snake from it's current state
        :param flag: A parameter to determine if the board has borders or not
        :return: A list of the legal moves
        """
        legal_actions = {Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN}
        i, j = self.board.snake[0]

        if not self.is_legal_move(i - 1, j):
            legal_actions.remove(Direction.UP)
        if not self.is_legal_move(i + 1, j):
            legal_actions.remove(Direction.DOWN)
        if not self.is_legal_move(i, j - 1):
            legal_actions.remove(Direction.LEFT)
        if not self.is_legal_move(i, j + 1):
            legal_actions.remove(Direction.RIGHT)
        if flag:
            if j - 1 < 0 and Direction.LEFT in legal_actions:
                legal_actions.remove(Direction.LEFT)
            if j + 1 >= self.board.board_size and Direction.RIGHT in legal_actions:
                legal_actions.remove(Direction.RIGHT)
            if i - 1 < 0 and Direction.UP in legal_actions:
                legal_actions.remove(Direction.UP)
            if i + 1 >= self.board.board_size and Direction.DOWN in legal_actions:
                legal_actions.remove(Direction.DOWN)
        return list(legal_actions)

    def __eq__(self, other):
        return other.board == self.board

    def __hash__(self) -> int:
        return hash(self.board)


class Agent:
    def next_move(self, board, flag=False):
        """
        Returns the next move of the snake according to the agent
        :param board: The board of the game
        :param flag: A parameter to determine if the board has borders
        :return: The next legal move of the snake, None of there is no legal moves
        """
        raise Exception("Method not implemented!")


class AStarAgent(Agent):
    def __init__(self, heuristic_function):
        self.heuristic_function = heuristic_function
        self.moves = []

    def next_move(self, board, flag=False):
        if not self.moves:
            self.moves = self.search(board, flag)
            if not self.moves:
                return None
        return self.moves.pop()

    def search(self, board, flag):
        """
        Searching for the path from the snake current location to the fruit
        :param board: The board of the path
        :param flag: A parameter that determines if the board has borders
        :return: A path to the fruit, empty list of there is no path
        """
        fringe = utils.PriorityQueueWithFunction(lambda state: state.f)
        initial_state = State(board, 0, self.heuristic_function, [])
        fringe.push(initial_state)
        visited = []
        while not fringe.is_empty():
            item: State = fringe.pop()
            if item in visited:
                continue
            visited.append(item)
            if item.is_goal():
                return item.path
            for move in item.legal_action(flag):
                new_board = copy.deepcopy(item.board)
                new_board.next_move = move
                new_board.step()
                new_state = State(new_board, item.g + 1, self.heuristic_function, [move] + item.path)
                fringe.push(new_state)
        return []


class HamiltonianAgent(Agent):
    def __init__(self, board_size):
        self.maze: hamiltonian_cycle.Maze = hamiltonian_cycle.Maze(board_size)
        self.maze.generate()
        self.path = []

    def next_move(self, board, flag=False):
        y, x = board.snake[0]
        tail_y, tail_x = board.snake[~0]
        fruit_y, fruit_x = board.fruit_location

        head_pos = self.maze.get_path_number(x, y)
        tail_pos = self.maze.get_path_number(tail_x, tail_y)
        fruit_pos = self.maze.get_path_number(fruit_x, fruit_y)

        distance_to_fruit = self.maze.path_distance(head_pos, fruit_pos)
        distance_to_tail = self.maze.path_distance(head_pos, tail_pos)
        cutting_amount_available = distance_to_tail - 5
        empty_squares = self.maze.board_size - len(board.snake) - 3

        if empty_squares < self.maze.board_size / 4:
            cutting_amount_available = 0
        elif distance_to_fruit < distance_to_tail:
            cutting_amount_available -= 1
            if (distance_to_tail - distance_to_fruit) * 4 > empty_squares:
                cutting_amount_available -= 10
        cutting_amount_desired = distance_to_fruit
        if cutting_amount_desired < cutting_amount_available:
            cutting_amount_available = cutting_amount_desired
        if cutting_amount_available < 0:
            cutting_amount_available = 0

        state: State = State(board, 0, lambda s: 0, None)
        if flag:
            legal_moves = state.legal_action(True)
        else:
            legal_moves = state.legal_action()
        can_go_right = Direction.RIGHT in legal_moves and x < board.board_size - 1
        can_go_left = Direction.LEFT in legal_moves and x > 0
        can_go_down = Direction.DOWN in legal_moves and y < board.board_size - 1
        can_go_up = Direction.UP in legal_moves and y > 0

        best_dir = None
        best_dist = -1

        if can_go_right:
            dist = self.maze.path_distance(head_pos, self.maze.get_path_number(x + 1, y))
            if cutting_amount_available >= dist > best_dist:
                best_dir = Direction.RIGHT
                best_dist = dist
        if can_go_left:
            dist = self.maze.path_distance(head_pos, self.maze.get_path_number(x - 1, y))
            if cutting_amount_available >= dist > best_dist:
                best_dir = Direction.LEFT
                best_dist = dist
        if can_go_up:
            dist = self.maze.path_distance(head_pos, self.maze.get_path_number(x, y - 1))
            if cutting_amount_available >= dist > best_dist:
                best_dir = Direction.UP
                best_dist = dist
        if can_go_down:
            dist = self.maze.path_distance(head_pos, self.maze.get_path_number(x, y + 1))
            if cutting_amount_available >= dist > best_dist:
                best_dir = Direction.DOWN
                best_dist = dist

        if best_dist >= 0:
            return best_dir
        if can_go_up:
            return Direction.UP
        if can_go_left:
            return Direction.LEFT
        if can_go_down:
            return Direction.DOWN
        if can_go_right:
            return Direction.RIGHT
        else:
            return None


class BreadthFirstSearchAgent(Agent):
    def __init__(self):
        self.path = []

    def next_move(self, board, flag=False):
        if not self.path:
            self.path = self.search(board, flag)
            if not self.path:
                return None
        return self.path.pop()

    def search(self, board, flag=False):
        """
       Searching for the path from the snake current location to the fruit
       :param board: The board of the path
       :param flag: A parameter that determines if the board has borders
       :return: A path to the fruit, empty list of there is no path
       """
        fringe = utils.Queue()
        initial_state = State(board, 0, None, [])
        fringe.push(initial_state)
        visited = list()
        while not fringe.is_empty():
            item = fringe.pop()
            if item in visited:
                continue
            visited.append(item)
            if item.is_goal():
                return item.path
            for move in item.legal_action(flag):
                self.update_fringe(item, move, fringe)
        return []

    def update_fringe(self, item: State, move, fringe):
        """
         Updating the fringe and the path
         :param item: The current state of the snake
         :param move: The move the snake will take
         :param fringe: The data structure that contains the states
         """
        new_board = copy.deepcopy(item.board)
        new_board.next_move = move
        new_board.step()
        new_state = State(new_board, item.g + 1, None, [move] + item.path)
        fringe.push(new_state)


class BestFirstSearchAgent(Agent):
    def __init__(self, heuristic_function=utils.manhattan_d):
        self.path = []
        self.h = heuristic_function

    def next_move(self, board, flag=False):
        if not self.path:
            self.path = self.search(board, flag)
            if not self.path:
                return None
        return self.path.pop()

    def search(self, board, flag=False):
        """
       Searching for the path from the snake current location to the fruit
       :param board: The board of the path
       :param flag: A parameter that determines if the board has borders
       :return: A path to the fruit, empty list of there is no path
       """
        fringe = utils.PriorityQueue()
        initial_state = State(board, 0, None, [])
        fringe.push(initial_state, self.h)
        visited = []
        while not fringe.is_empty():
            item = fringe.pop()
            if item in visited:
                continue
            visited.append(item)
            if item.is_goal():
                return item.path
            for move in item.legal_action(flag):
                self.update_fringe(item, move, fringe)
        return []

    def update_fringe(self, item: State, move, fringe):
        """
        Updating the fringe and the path
        :param item: The current state of the snake
        :param move: The move the snake will take
        :param fringe: The data structure that contains the states
        """
        new_board = copy.deepcopy(item.board)
        new_board.next_move = move
        new_board.step()
        new_state = State(new_board, item.g + 1, None, [move] + item.path)
        fringe.push(new_state, item.g)
