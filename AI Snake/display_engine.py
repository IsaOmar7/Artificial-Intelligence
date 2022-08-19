import pygame
import config


class DisplayEngine:
    """
    Abstract class
    """

    def __init__(self, input_cb):
        """
        Initiating instance of the class
        :param input_cb: function that returns the next Direction
        """
        self.input_cb = input_cb

    def render(self, game):
        raise Exception("Unimplemented method")


class GUIDisplayEngine(DisplayEngine):
    """
    A class to display on the monitor
    """

    def __init__(self, input_cb):
        # super().__init__(lambda x: print(x))
        super().__init__(input_cb)
        pygame.init()
        self.screen = pygame.display.set_mode(
            (config.HEIGHT, config.GUI_WIDTH))
        self.timer = pygame.time.Clock()
        self.screen.fill((0, 0, 0))
        self.apple = pygame.image.load(f'data/apple.png').convert()
        self.body = pygame.image.load(f'data/body.png').convert()
        self.head = pygame.image.load(f'data/head.png').convert()
        self.first_run = True
        self.played_games = 0
        self.end_game = False

    def render(self, game):
        if game.state == config.GameState.GAME_OVER:
            self.played_games += 1
            if game.num_of_games <= self.played_games:
                if self.end_game:
                    self.screen.fill((0, 0, 0,))
                    pygame.display.update()
                    self.end_game = False
            else:
                self.first_run = True
                self.screen.fill((0, 0, 0,))
                pygame.display.update()
        else:
            board = game.board
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                if event.type == pygame.KEYDOWN:
                    if game.state == config.GameState.PAUSED:
                        game.state = config.GameState.RUNNING
                    if event.key == pygame.K_LEFT and board.next_move != config.Direction.RIGHT:
                        self.input_cb(config.Direction.LEFT)
                    elif event.key == pygame.K_UP and board.next_move != config.Direction.DOWN:
                        self.input_cb(config.Direction.UP)
                    elif event.key == pygame.K_DOWN and board.next_move != config.Direction.UP:
                        self.input_cb(config.Direction.DOWN)
                    elif event.key == pygame.K_RIGHT and board.next_move != config.Direction.LEFT:
                        self.input_cb(config.Direction.RIGHT)
            block_size = config.BLOCK_SIZE
            if self.first_run:
                for obs_cor in board.obstacles:
                    row, col = obs_cor[0] * block_size, obs_cor[1] * block_size
                    rect = pygame.Rect(col, row, block_size, block_size)
                    pygame.draw.rect(self.screen, (228, 87, 46), rect)
            self.first_run = False
            apple_row, apple_col = board.fruit_location[0] * block_size, \
                                   board.fruit_location[1] * block_size
            self.screen.blit(self.apple, (apple_col, apple_row))
            pygame.display.update()
            head = board.snake[0]
            if board.next_move == config.Direction.UP:
                multiply = 0
            elif board.next_move == config.Direction.DOWN:
                multiply = 2
            elif board.next_move == config.Direction.LEFT:
                multiply = 1
            else:
                multiply = 3
            rotate = 90
            self.screen.blit(pygame.transform.rotate(self.head, rotate * multiply),
                             (head[1] * block_size, head[0] * block_size))
            if len(board.snake) > 1:
                body = board.snake[1]
                self.screen.blit(self.body,
                                 (body[1] * block_size, body[0] * block_size))
            pygame.display.update()
            tail = board.snake[-1]
            pygame.draw.rect(self.screen, (0, 0, 0),
                             (tail[1] * block_size, tail[0] * block_size, 43,
                              43))


class DefaultDisplayEngine(DisplayEngine):
    """
    a class to make sure we have an implementation for the render function
    """

    def render(self, game):
        pass
