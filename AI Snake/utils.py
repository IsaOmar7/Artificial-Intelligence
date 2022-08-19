import heapq
import random

"""
Heuristics functions
"""


def color_rgb(c1, c2, fraction):
    return c1[0] + (c2[0] - c1[0]) * fraction, \
           c1[1] + (c2[1] - c1[1]) * fraction, \
           c1[2] + (c2[2] - c1[2]) * fraction


def cyclic(v, b):
    return (v + b) % b


def manhattan_d(a1, a2):
    return abs(a1[0] - a2[0]) + abs(a1[1] - a2[1])


def squareness(snake):
    x_max, x_min, y_min, y_max = 0, 0, 0, 0
    # getting the dominions of the snake
    for s in snake:
        x, y = s
        if x < x_min:
            x_min = x
        if x > x_max:
            x_max = x
        if y < y_min:
            y_min = y
        if y > y_max:
            y_max = y
    return (x_max - x_min) * (y_min - y_max) - len(snake)


def compactness(snake):
    comp = 0
    for i in range(len(snake)):
        for j in range(i + 1, len(snake)):
            if (abs(snake[i][0] - snake[j][0] == 0) and abs(snake[i][1] - snake[j][1] == 1)) or (
                    abs(snake[i][0] - snake[j][0] == 1) and abs(snake[i][1] - snake[j][1] == 0)):
                comp += 1
    return -comp


def connectivity(board):
    snake = board.snake
    empty_cells = []
    for i in range(board.board_size):
        for j in range(board.board_size):
            if (i, j) not in board.obstacles and (i, j) not in snake:
                empty_cells.append((i, j))
    if len(empty_cells) > 1:
        rand_field = empty_cells[random.randint(0, len(empty_cells) - 1)]
    else:
        return 0
    reached = [rand_field]
    empty_cells.remove(rand_field)

    while len(reached) > 0:
        curr_field = reached[0]
        reached.remove(curr_field)
        up, down, right, left = (curr_field[0], curr_field[1] + 1), (curr_field[0], curr_field[1] - 1), (
            curr_field[0] + 1, curr_field[1]), (curr_field[0] - 1, curr_field[1])
        if up in empty_cells:
            empty_cells.remove(up)
            reached.append(up)
        if down in empty_cells:
            empty_cells.remove(down)
            reached.append(down)
        if right in empty_cells:
            empty_cells.remove(right)
            reached.append(right)
        if left in empty_cells:
            empty_cells.remove(left)
            reached.append(left)
    return len(empty_cells)


def dead_end(board):
    snake = board.snake
    empty_cells = []
    for i in range(board.board_size):
        for j in range(board.board_size):
            if (i, j) not in board.obstacles and (i, j) not in snake:
                empty_cells.append((i, j))
    snake_head = snake[0]
    reached = [snake_head]

    while len(reached) > 0:
        curr_field = reached[0]
        reached.remove(curr_field)
        up, down, right, left = (curr_field[0], curr_field[1] + 1), (curr_field[0], curr_field[1] - 1), (
            curr_field[0] + 1, curr_field[1]), (curr_field[0] - 1, curr_field[1])

        if up in empty_cells:
            empty_cells.remove(up)
            reached.append(up)
        if down in empty_cells:
            empty_cells.remove(down)
            reached.append(down)
        if right in empty_cells:
            empty_cells.remove(right)
            reached.append(right)
        if left in empty_cells:
            empty_cells.remove(left)
            reached.append(left)
    return len(empty_cells)


"""
    End of heuristics functions
"""

"""
    Data structures
"""


class Stack:
    """
    Last In First Out (LIFO) container
    """

    def __init__(self):
        self.stack = []

    def push(self, item):
        """
        Pushing an item into the stack
        :param item: The item we want to push
        :return:
        """
        self.stack.append(item)

    def pop(self):
        """
        Returning the last added element to the stack and delete it
        :return: The last element in the stack
        """
        return self.stack.pop()

    def is_empty(self):
        """
        Check if the stack is empty
        :return: True if the stack is empty, false otherwise
        """
        return len(self.stack) == 0


class Queue:
    """
    First In First Out (FIFO) container
    """

    def __init__(self):
        self.queue = []

    def push(self, item):
        """
        Adding an element to the start of the list
        :param item: The item we want to add
        :return:
        """
        self.queue.insert(0, item)

    def pop(self):
        """
        Dequeue the first element added to the queue and removing it
        :return: The dequeued element
        """
        return self.queue.pop()

    def is_empty(self):
        """
        Check if the queue is empty
        :return: True if the queue is empty, False otherwise
        """
        return len(self.queue) == 0


class PriorityQueue:
    """
      Implements a priority queue data structure. Each inserted item
      has a priority associated with it and the client is usually interested
      in quick retrieval of the lowest-priority item in the queue. This
      data structure allows O(1) access to the lowest-priority item.

      Note that this PriorityQueue does not allow you to change the priority
      of an item.  However, you may insert the same item multiple times with
      different priorities.
    """

    def __init__(self):
        self.heap = []
        self.init = False

    def push(self, item, priority):
        if not self.init:
            self.init = True
            try:
                item < item
            except:
                item.__class__.__lt__ = lambda x, y: (True)
        pair = (priority, item)
        heapq.heappush(self.heap, pair)

    def pop(self):
        (priority, item) = heapq.heappop(self.heap)
        return item

    def is_empty(self):
        return len(self.heap) == 0

    def __len__(self):
        return len(self.heap)


class PriorityQueueWithFunction(PriorityQueue):
    """
    Implements a priority queue with the same push/pop signature of the
    Queue and the Stack classes. This is designed for drop-in replacement for
    those two classes. The caller has to provide a priority function, which
    extracts each item's priority.
    """

    def __init__(self, priorityFunction):
        "priorityFunction (item) -> priority"
        self.priorityFunction = priorityFunction  # store the priority function
        PriorityQueue.__init__(self)  # super-class initializer

    def push(self, item):
        "Adds an item to the queue with priority from the priority function"
        PriorityQueue.push(self, item, self.priorityFunction(item))


"""
END of Data Structure declaration
"""
