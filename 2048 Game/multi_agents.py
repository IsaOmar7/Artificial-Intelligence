import numpy as np
import copy
import abc
import util
from game import Agent, Action


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def get_action(self, game_state):
        """
        You do not need to change this method, but you're welcome to.

        get_action chooses among the best options according to the evaluation function.

        get_action takes a game_state and returns some Action.X for some X in the set {UP, DOWN, LEFT, RIGHT, STOP}
        """

        # Collect legal moves and successor states
        legal_moves = game_state.get_agent_legal_actions()

        # Choose one of the best actions
        scores = [self.evaluation_function(game_state, action) for action in legal_moves]
        best_score = max(scores)
        best_indices = [index for index in range(len(scores)) if scores[index] == best_score]
        chosen_index = np.random.choice(best_indices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legal_moves[chosen_index]

    def evaluation_function(self, current_game_state, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (GameState.py) and returns a number, where higher numbers are better.

        """

        # Useful information you can extract from a GameState (game_state.py)
        counter = 0
        successor_game_state = current_game_state.generate_successor(action=action)
        board = successor_game_state.board
        for i in range(len(board)):
            counter += check_row(board[i])
        tr_arr = transpose_matrix(board)
        for i in range(len(tr_arr)):
            counter += check_row(tr_arr[i])
        max_tile = successor_game_state.max_tile
        score = successor_game_state.score + counter
        return score


def transpose_matrix(matrix):
    """
    Helper function to transpose a given matrix
    @param matrix The matrix we want to transpose
    @return A new transposed matrix
    """

    result = copy.deepcopy(matrix)
    for i in range(len(matrix)):
        # iterate through columns
        for j in range(len(matrix[0])):
            result[j][i] = matrix[i][j]
    return result


def check_row(row):
    """
    the function takes a row and checks how many of the same number in the row are adjacent to each other
    returns: the number of repetitive adjacent numbers.
    """
    counter = 0
    checked_lst = []
    for i in range(len(row)):
        if row[i] != 0 and row[i] not in checked_lst:
            for j in range(i + 1, len(row)):
                if row[j] != 0 and row[j] != row[i]:
                    break
                if row[j] != 0 and row[j] == row[i]:
                    checked_lst.append(row[i])
                    counter += 1
                    break
    return counter


def score_evaluation_function(current_game_state):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return current_game_state.score


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinmaxAgent, AlphaBetaAgent & ExpectimaxAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evaluation_function='scoreEvaluationFunction', depth=2):
        self.evaluation_function = util.lookup(evaluation_function, globals())
        self.depth = depth

    @abc.abstractmethod
    def get_action(self, game_state):
        return


class MinmaxAgent(MultiAgentSearchAgent):
    def get_action(self, game_state):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        game_state.get_legal_actions(agent_index):
            Returns a list of legal actions for an agent
            agent_index=0 means our agent, the opponent is agent_index=1

        Action.STOP:
            The stop direction, which is always legal

        game_state.generate_successor(agent_index, action):
            Returns the successor game state after an agent takes an action
        """
        depth = self.depth * 2
        action = self.minimax(game_state, depth, True)[1]
        return action
        # util.raiseNotDefined()

    def minimax(self, game_state, depth, flag):
        """
        recursive function that implements the actions of two players where our agent(0) tries to maximize the score
        by choosing the highest value in the current depth, and the opponent agent(1) tries to minimize it choosing
        the lowest value in the current depth.
        @param game_state: given game state
        @param depth: depth of the tree
        @param flag: an indicator of the index of an agent.If it's true then it our agent else it's the opponent.
        """
        if self.check_end_game__(game_state, depth):
            return self.evaluation_function(game_state), Action.STOP
        if flag:
            our_agent = game_state.get_legal_actions(0)
            successors_lst = self.successor_generate(game_state, our_agent, 0)
            max_eval = float('-inf')
            move = Action.STOP
            for successor in successors_lst:
                eval = self.minimax(successor[0], depth - 1, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    move = successor[1]
            return max_eval, move
        else:
            opponent_agent = game_state.get_legal_actions(1)
            successors_lst = self.successor_generate(game_state, opponent_agent, 1)
            min_eval = float('inf')
            move = Action.STOP
            for successor in successors_lst:
                eval = self.minimax(successor[0], depth - 1, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    move = successor[1]
            return min_eval, move

    def check_end_game__(self, game_state, depth):
        if depth == 0 or (len(game_state.get_legal_actions(0)) == 0 and len(game_state.get_legal_actions(1)) == 0):
            return True

    def successor_generate(self, game_state, agent, agent_index):
        lst = []
        for action in agent:
            succ = game_state.generate_successor(agent_index, action=action)
            lst.append((succ, action))
        return lst


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def get_action(self, game_state):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        """* YOUR CODE HERE *"""
        depth = 2 * self.depth
        action = self.alpha_beta_minimax(game_state, float('-inf'), float('inf'), depth, True)[1]
        return action
        # util.raiseNotDefined()

    def alpha_beta_minimax(self, game_state, alpha, beta, depth, flag):
        """
        recursive function that works the same as the minimax function, but uses to additional parameters to avoid
        checking unnecessary routes in the search tree.
        @param game_state: given game state
        @param alpha: makes sure that our agent doesn't check unnecessary nodes, initial value is minus infinity
        @param beta: makes sure that opponent agent doesn't check unnecessary nodes, initial value is infinity
        @param depth: depth of the search tree
        @param flag: an indicator of the index of an agent.If it's true then it our agent else it's the opponent.
        """
        if self.check_end_game__(game_state, depth):
            return self.evaluation_function(game_state), Action.STOP
        # our agent checks for max value
        if flag:
            our_agent = game_state.get_legal_actions(0)
            successors_lst = self.successor_generate(game_state, our_agent, 0)
            max_eval = float('-inf')
            move = Action.STOP
            for successor in successors_lst:
                eval = self.alpha_beta_minimax(successor[0], alpha, beta, depth - 1, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    move = successor[1]
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, move
        # opponent agent checks for min value
        else:
            opponent_agent = game_state.get_legal_actions(1)
            successors_lst = self.successor_generate(game_state, opponent_agent, 1)
            min_eval = float('inf')
            move = Action.STOP
            for successor in successors_lst:
                eval = self.alpha_beta_minimax(successor[0], alpha, beta, depth - 1, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    move = successor[1]
                beta = min(eval, beta)
                if alpha >= beta:
                    break
            return min_eval, move

    def check_end_game__(self, game_state, depth):
        if depth == 0 or (len(game_state.get_legal_actions(0)) == 0 and len(game_state.get_legal_actions(1)) == 0):
            return True

    def successor_generate(self, game_state, agent, agent_index):
        lst = []
        for action in agent:
            succ = game_state.generate_successor(agent_index, action=action)
            lst.append((succ, action))
        return lst


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """

    def get_action(self, game_state):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        The opponent should be modeled as choosing uniformly at random from their
        legal moves.
        """
        """* YOUR CODE HERE *"""
        depth = 2 * self.depth
        action = self.expectimax(game_state, depth, True, counter=0)[1]
        return action

    def expectimax(self, game_state, depth, flag, counter):
        """
        recursive function that works the same as the minimax function, our agent that is calculating the white move
        (maximum value)work the same as in minimax, however the opponent agent calculates the minimum by taking the
        average of all the black (minimum)actions.
        @param game_state: given game state
        @param depth: depth of the search tree
        @param flag: an indicator of the index of an agent.If it's true then it our agent else it's the opponent.
        """
        if self.check_end_game__(game_state, depth):
            return self.evaluation_function(game_state), Action.STOP
        if flag:
            our_agent = game_state.get_legal_actions(0)
            successors_lst = self.successor_generate(game_state, our_agent, 0)
            max_eval = float('-inf')
            move = Action.STOP
            for successor in successors_lst:
                eval = self.expectimax(successor[0], depth - 1, False, counter)[0]
                if eval > max_eval:
                    max_eval = eval
                    move = successor[1]
            return max_eval, move
        else:
            opponent_agent = game_state.get_legal_actions(1)
            lst = []
            successors_lst = self.successor_generate(game_state, opponent_agent, 1)
            for i in range(len(opponent_agent)):
                lst.append(i)
            random_choice = np.random.choice(lst)
            avg = 0
            for successor in successors_lst:
                eval = self.expectimax(successor[0], depth - 1, True, counter)[0]
                avg += eval / len(successors_lst)

            return avg, opponent_agent[random_choice]

    def check_end_game__(self, game_state, depth):
        if depth == 0 or (len(game_state.get_legal_actions(0)) == 0 and len(game_state.get_legal_actions(1)) == 0):
            return True

    def successor_generate(self, game_state, agent, agent_index):
        lst = []
        for action in agent:
            succ = game_state.generate_successor(agent_index, action=action)
            lst.append((succ, action))
        return lst


def better_evaluation_function(current_game_state):
    """
    Your extreme 2048 evaluation function (question 5).

    In order to win the game with the highest score we need to keep the tiles with the highest numbers next to
    each other closest to the one of the corners,Therefore we created a weights board ,using a Numpy array,
    which consists of weights assigned to each tile in a zigzag shape(Z).we chose to put the largest tile in the
    closest tile to the upper right corner(if it's empty then we put it in the upper right tile).
    Then we multiply and sum our board and the weights boards by coordinates
    with the help of numpy sum, in the end we get a list of maximum 4 values thar represent each possible action
    and we choose the one with the highest number.
    @param current_game_state: given game state
    @return: the successor with the highest score.
    """
    states_list = list()
    actions = current_game_state.get_agent_legal_actions()
    if not actions:
        return current_game_state.score
    for action in actions:
        successor = current_game_state.generate_successor(action=action)
        if successor not in states_list:
            states_list.append(successor)
    weights_board = np.array([[2 ** 7, 2 ** 7.5, 2 ** 8, 2 ** 8.5], [2 ** 6.5, 2 ** 6, 2 ** 5.5, 2 ** 5],
                              [2 ** 3, 2 ** 3.5, 2 ** 4, 2 ** 4.5], [2 ** 2.5, 2 ** 2, 2 ** 1.5, 2 ** 1]])
    score_list = list()
    for state in states_list:
        matrix = weights_board * state.board
        score = np.sum(matrix)
        score_list.append(score)
    return max(score_list)


# Abbreviation
better = better_evaluation_function
