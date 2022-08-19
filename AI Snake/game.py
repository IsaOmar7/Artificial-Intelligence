from optparse import OptionParser
import pygame
import random
import display_engine
import config
from agent import *
from heuristics import *


class Game:

    def __init__(self, board_size, obstacle_chance, agent=None, display_class=display_engine.DefaultDisplayEngine,
                 border=0, board_file=None, num_of_games=None):
        self.board = Board(board_size, obstacle_chance, board_file)
        self.iterations = 0
        self.agent = agent
        self.state = None
        self.display = display_class(self.board.move)
        self.clock = pygame.time.Clock()
        self.border = border
        self.num_of_games = num_of_games

    def run(self):
        """
        This function runs the game until the game is won or the snake die
        """
        self.state = config.GameState.RUNNING
        self.board.spawn_snake(2, 2, 1)
        self.board.spawn_fruit()
        while self.state != config.GameState.GAME_OVER:
            if self.state == config.GameState.PAUSED:
                continue
            if self.border == 1:
                move = self.agent.next_move(self.board, True)
                if not move:
                    break
                self.board.next_move = move
                self.board.step()
            else:
                move = self.agent.next_move(self.board)
                if not move:
                    break
                self.board.next_move = move
                self.board.step()

            if self.board.snake[0] in self.board.obstacles or self.board.snake[0] in self.board.snake[
                                                                                     1:] or self.iterations == 256:
                self.state = config.GameState.GAME_OVER

            elif self.board.snake[0] == self.board.fruit_location:
                if len(self.board.snake) > pow(self.board.board_size, 2) - 1:  # Game won
                    self.state = config.GameState.GAME_OVER
                else:
                    self.iterations = 0
                    self.board.eat_fruit()
            self.iterations += 1
            self.display.render(self)
            self.clock.tick(config.FRAME_RATE)
        self.state = config.GameState.GAME_OVER
        self.display.render(self)
        self.board.end_game()


class Board:
    def __init__(self, board_size, obstacle_chance, board_file=None):
        self.board_size = board_size
        self.next_move = config.Direction.LEFT
        self.snake = []
        self.obstacles = set()
        self.fruit_location = ()
        if board_file:
            self.load_from_file(board_file)
        else:
            # generate a new board
            self.generate_obstacles(board_size, obstacle_chance,
                                    self.load_obstacles('obt.txt'))

    def move(self, direction):
        """
        Update the next move of the board
        :param direction: The direction we want to move to
        """
        self.next_move = direction

    @staticmethod
    def load_obstacles(file_name):
        """
        Loading the obstacles from a file to the object
        :param file_name: The file of the obstacles
        :return: a list of the coordinates of the obstacles
        """
        with open(f'data/{file_name}') as file:
            return [[[int(c) for c in b.split(',')] for b in a.split('_')] for a in file.readlines()]

    def load_from_file(self, file_name):
        with open(file_name) as file:
            _board = [line.split(',') for line in file.readlines()]
            if not _board:
                return
            for i in range(len(_board)):
                for j in range(len(_board[0])):
                    if _board[i][j] == 'x':
                        self.obstacles.add((i, j))

    def generate_obstacles(self, board_size, obstacle_chance, obstacles):
        """
        Generate obstacle from list of obstacles randomly placed throughout the board
        :param board_size: The size of the board
        :param obstacle_chance: number of tiles count as obstacle
        :param obstacles: list of obstacles
        :return: board with randomly generated obstacles
        """
        all_obstacles = []
        for i in range(int(board_size / 4) + 1):
            for j in range(int(board_size / 4) + 1):
                if random.random() > obstacle_chance:
                    continue
                cell_i = 4 * i
                cell_j = 4 * j
                curr_i = random.randint(1, 2)
                curr_j = random.randint(1, 2)
                ob = random.choice(obstacles)
                ob = [(row + curr_j + cell_j, col + curr_i + cell_i) for row, col in ob]
                ob = [(row, col) for row, col in ob if row < board_size and col < board_size]
                all_obstacles += ob
        self.obstacles = all_obstacles[:]

    def spawn_snake(self, row, col, length):
        """
        Spawns a snake where the head's coordinates are (row, col) and with body length of `length` (including the head)
        """
        head = (row, col)
        self.snake = [head]
        if head in self.obstacles:
            self.obstacles.remove(head)
        for i in range(1, length):
            part = (row, col + i)
            if part in self.obstacles:
                self.obstacles.remove(part)
            self.snake.append(part)

    def step(self):
        """
        Updates the coordinates of the snake after making a move in the game
        """
        head_i, head_j = self.snake[0]
        direction = self.next_move
        if direction == config.Direction.LEFT:
            head_j -= 1
        elif direction == config.Direction.RIGHT:
            head_j += 1
        elif direction == config.Direction.UP:
            head_i -= 1
        elif direction == config.Direction.DOWN:
            head_i += 1

        head_i = (head_i + self.board_size) % self.board_size
        head_j = (head_j + self.board_size) % self.board_size

        if (head_i, head_j) != self.fruit_location:
            self.snake.pop()

        self.snake.insert(0, (head_i, head_j))

    def spawn_fruit(self):
        """
        add fruit to random location on the board
        """
        i = random.randint(0, config.BOARD_SIZE - 1)
        j = random.randint(0, config.BOARD_SIZE - 1)

        while (i, j) in self.obstacles or (i, j) in self.snake:
            i = random.randint(0, config.BOARD_SIZE - 1)
            j = random.randint(0, config.BOARD_SIZE - 1)
        self.fruit_location = (i, j)

    def eat_fruit(self):
        """
        Eating the fruit and changing it's location
        """
        self.spawn_fruit()

    def end_game(self):
        """
        Ending the game and printing the score of the game to the screen
        """
        print(f'Game Ended, Score: {len(self.snake)}')

    def __eq__(self, other):
        return isinstance(other, Board) and other.snake[0] == self.snake[0]


def main():
    usage_str = """USAGE:python3 game.py <options>"""
    parser = OptionParser(usage_str)
    parser.add_option(
        '-b', '--border', help="The borders of the board", default=0, type=int
    )
    parser.add_option(
        '-s', '--size', dest='board_size',
        help='The size of the board.With Hamiltonian cycle agent it must be even number',
        default=config.BOARD_SIZE, type=int
    )
    parser.add_option(
        '-o', '--obstacle-chance', help='Chance to spawn obstacles in the board',
        default=1, type=int, metavar='[0-1]',
    )

    parser.add_option('-n', '--num-of-games', help='Number of games to play', default=1, type=int)
    parser.add_option('-f', '--frame-rate', help='Limit frame rate of the game', default=config.FRAME_RATE, type=int)

    agents = ['astar', 'bfs', 'hamiltonian', 'gbfs']
    heus = ['manhattan', 'wighted-compact']
    parser.add_option(
        '--agent', choices=agents, help=f'The agent to drive the snake',
        default=agents[0], type='choice', metavar=agents
    )
    parser.add_option('--heu', choices=heus, help=f'The heuristic for the A* agent', default=heus[0], metavar=heus)

    displays = ['GUI', 'CLI', 'Silent']
    parser.add_option(
        '--display', metavar=displays, choices=displays, default='GUI',
        help='Display type for the game'
    )

    args, _ = parser.parse_args()

    config.FRAME_RATE = args.frame_rate
    config.BLOCK_SIZE = config.GUI_WIDTH / args.board_size

    display = get_display(args.display)
    heu = get_heuristic(args.heu)
    agent = get_agent(
        args.agent,
        size=args.board_size, heu=heu)
    border = args.border
    game = Game(args.board_size, args.obstacle_chance, agent, display, border, num_of_games=args.num_of_games)

    scores = []
    for _ in range(args.num_of_games):
        game.run()
        scores.append(len(game.board.snake))
    avg = sum(scores) / args.num_of_games
    avg_coverage = avg / (args.board_size * args.board_size)
    print(f'Finished with average score of {avg}, average board coverage: {avg_coverage * 100: 0.2f}%')


def get_heuristic(name: str):
    """
    Take the name of a heuristics function and returns an instance of the heuristics
    :param name: The name of the heuristics function
    :return: An instance of the heuristics function
    """
    name = name.lower()
    if name == 'manhattan':
        return manhattan_distance
    if name == 'weighted-compact':
        return weighed_compact_heuristics


def get_agent(name: str, **kwargs):
    """
    Take the name of an agent and returns an instance of the agent
    :param name: The name of the agent
    :param kwargs: Parameters for each agent to initiate
    :return: An instance of the agent
    """
    name = name.lower()
    if name == 'astar':
        return AStarAgent(kwargs['heu'])
    elif name == 'hamiltonian':
        board_size = kwargs['size']
        return HamiltonianAgent(board_size)
    elif name == 'bfs':
        return BreadthFirstSearchAgent()
    else:
        return BestFirstSearchAgent()


def get_display(name: str):
    """
    Take a name of display engine and return an instance of the display agent
    :param name: The name of the display agent
    :return: An instance of the display agent
    """
    if name == 'GUI':
        return display_engine.GUIDisplayEngine
    elif name == 'Silent':
        return display_engine.DefaultDisplayEngine


if __name__ == '__main__':
    main()
