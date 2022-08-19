"""
In search.py, you will implement generic search algorithms
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def get_start_state(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def is_goal_state(self, state):
        """
        state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def get_successors(self, state):
        """
        state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def get_cost_of_actions(self, actions):
        """
        actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def depth_first_search(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches
    the goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

	print("Start:", problem.get_start_state().state)
    print("Is the start a goal?", problem.is_goal_state(problem.get_start_state()))
    print("Start's successors:", problem.get_successors(problem.get_start_state()))
    """
    # add first state
    start_node = problem.get_start_state()
    stack = util.Stack()
    # visited set to store the visited nodes
    visited = set()
    # storing the path so far
    path = []
    stack.push((start_node, path))
    while not stack.isEmpty():
        curr, path = stack.pop()
        if problem.is_goal_state(curr):
            return path
        succ_lst = problem.get_successors(curr)
        for successor, action, cost in succ_lst:
            if successor not in visited:
                stack.push((successor, path + [action]))
                visited.add(successor)


def breadth_first_search(problem: SearchProblem):
    """
    Search the shallowest nodes in the search tree first.
    """
    # add first state
    start_node = problem.get_start_state()
    queue = util.Queue()
    # visited set to store the visited nodes
    visited = set()
    # storing the path so far
    path = []
    queue.push((start_node, path))
    while not queue.isEmpty():
        curr, path = queue.pop()
        if problem.is_goal_state(curr):
            return path
        succ_lst = problem.get_successors(curr)
        for successor, action, cost in succ_lst:
            if successor not in visited:
                queue.push((successor, path + [action]))
                visited.add(successor)


def uniform_cost_search(problem: SearchProblem):
    """
    Search the node of least total cost first.
    """
    start_node = problem.get_start_state()
    priorityQ = util.PriorityQueue()
    visited = set()
    path = []
    ind = 0
    # we use the ind to compare states with the same cost
    priorityQ.push((ind, start_node, path), 0)
    ind += 1
    while not priorityQ.isEmpty():
        ind1, curr, path = priorityQ.pop()
        if problem.is_goal_state(curr):
            return path
        succ_lst = problem.get_successors(curr)
        for successor, action, cost in succ_lst:
            if successor not in visited:
                priorityQ.push((ind, successor, path + [action]), cost)
                ind += 1
                visited.add(successor)


def null_heuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def a_star_search(problem, heuristic=null_heuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    "*** YOUR CODE HERE ***"
    start_node = problem.get_start_state()
    priorityQ = util.PriorityQueue()
    visited = set()
    path = []
    ind = 0
    g_n = 0
    f_n = 0
    # we use the ind to compare states with the same cost
    priorityQ.push((ind, start_node, path), f_n)
    ind += 1
    ind1, curr, path = priorityQ.pop()
    if problem.is_goal_state(curr):
        return path
    # taking all the successors
    succ_lst = problem.get_successors(curr)
    # for each successor we insert them to the PriorityQ using the f_n function
    for successor, action, cost in succ_lst:
        g_n_temp = g_n + cost
        f_n = g_n_temp + heuristic((successor, action, cost), problem)
        priorityQ.push((ind, successor, path + [action], g_n_temp), f_n)
        # to prevent infinite loops
        visited.add(successor)
        ind += 1
    while not priorityQ.isEmpty():
        ind1, curr, path, curr_g_n = priorityQ.pop()
        if problem.is_goal_state(curr):
            return path
        succ_lst = problem.get_successors(curr)
        for successor, action, cost in succ_lst:
            if successor not in visited:
                g_n_temp = curr_g_n + cost
                f_n = g_n_temp + heuristic((successor, action, cost), problem)
                priorityQ.push((ind, successor, path + [action], g_n_temp), f_n)
                ind += 1
                visited.add(successor)


# Abbreviations
bfs = breadth_first_search
dfs = depth_first_search
astar = a_star_search
ucs = uniform_cost_search
