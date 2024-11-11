import heapq
from numpy import array_equal
import numpy as np
import time


class Puzzle:
    goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]

    def __init__(self, puzzle_board):
        self.puzzle_board = puzzle_board

    def find_possible_states(self):
        successor_states = []
        blank_row, blank_col = self.find_blank()

        # Define possible moves (right, down, left, up)
        possible_moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        for move in possible_moves:
            new_row = blank_row + move[0]
            new_col = blank_col + move[1]

            if 0 <= new_row < 3 and 0 <= new_col < 3:
                new_puzzle = self.swap_tiles(blank_row, new_row, blank_col, new_col)
                successor_states.append(new_puzzle)
        return successor_states

    # swapping 0 with neighbours
    def swap_tiles(self, old_row, new_row, old_col, new_col):
        # new_puzzle = self.puzzle_board.copy()
        new_puzzle = [row.copy() for row in self.puzzle_board]
        # print(old_row, new_row, old_col, new_col)
        temp = new_puzzle[old_row][old_col]
        new_puzzle[old_row][old_col] = new_puzzle[new_row][new_col]
        new_puzzle[new_row][new_col] = temp

        # temp = new_puzzle[old_row, old_col]
        # new_puzzle[old_row, old_col] = new_puzzle[new_row, new_col]
        # new_puzzle[new_row, new_col] = temp
        return Puzzle(new_puzzle)

    def find_blank(self):
        for i in range(3):
            for j in range(3):
                if self.puzzle_board[i][j] == 0:
                    return i, j

    def is_solvable(self):
        flatten_puzzle = [number for row in self.puzzle_board for number in row if number != 0]
        inversions = 0
        blank_row, _ = self.find_blank()

        for i in range(len(flatten_puzzle) - 1):
            for j in range(i + 1, len(flatten_puzzle)):
                if flatten_puzzle[i] > flatten_puzzle[j]:
                    inversions += 1

        # Calculate the parity of the total number of inversions
        inversions_even = (inversions % 2 == 0)

        # For an odd-sized puzzle, a puzzle is solvable if the number of inversions is even
        if len(self.puzzle_board) % 2 == 1:
            return inversions_even
        # For an even-sized puzzle, a puzzle is solvable if:
        # - the number of inversions is even, and the blank is on an odd row counting from the bottom, or
        # - the number of inversions is odd, and the blank is on an even row counting from the bottom
        else:
            return (inversions_even and blank_row % 2 == 1) or (inversions % 2 == 1 and blank_row % 2 == 0)

    def printPuzzle(self):
        for i in range(3):
            for j in range(3):
                if self.puzzle_board[i][j] != 0:
                    print(self.puzzle_board[i][j], end=" ")
                else:
                    print(" ", end=" ")
            print()
        print()


class Node:
    def __init__(self, puzzle, parent=None):
        self.puzzle = puzzle
        self.g = 0  # cost to reach current node
        self.h = 0  # estimated distance to goal state (heuristic)
        self.f = 0  # total
        self.parent = parent

    def __lt__(self, other):
        return self.f < other.f


def create_puzzles():
    puzzles = []
    while len(puzzles) < 100:
        random_numbers = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8])
        np.random.shuffle(random_numbers)
        puzzle = Puzzle(random_numbers.reshape(3, 3))
        if puzzle.is_solvable() and puzzle not in puzzles:
            puzzles.append(puzzle)
        # print(puzzle.puzzle_board)
    return puzzles


def manhattan_distance(puzzle):
    distance = 0
    for i in range(3):
        for j in range(3):
            current_number = puzzle.puzzle_board[i][j]
            if current_number != 0:
                goal_location = find_goal_location(current_number)
                distance += abs(goal_location[0] - i) + abs(goal_location[1] - j)
    return distance


def find_goal_location(number):
    for i in range(3):
        for j in range(3):
            if Puzzle.goal_state[i][j] == number:
                return i, j


def hamming_distance(puzzle):
    misplaced_tiles = 0
    for i in range(3):
        for j in range(3):
            if puzzle.puzzle_board[i][j] != Puzzle.goal_state[i][j] and puzzle.puzzle_board[i][j] != 0:
                misplaced_tiles += 1
    return misplaced_tiles


# A* Algorithm
def solve_puzzle(start, heuristic):
    start_node = Node(start)
    goal_node = Node(Puzzle.goal_state)
    nodes_count = 0

    pqueue = []
    closed_set = set()

    heapq.heappush(pqueue, start_node)

    while pqueue:
        current_node = heapq.heappop(pqueue)
        puzzle_board_tuple = tuple(map(tuple, current_node.puzzle.puzzle_board))
        closed_set.add(puzzle_board_tuple)
        nodes_count += 1

        if array_equal(current_node.puzzle.puzzle_board, Puzzle.goal_state):
            print(f"Solution Found after expanding {nodes_count} nodes.")
            path = []
            while current_node:
                path.append(current_node.puzzle)
                current_node = current_node.parent
            path.reverse()
            for puzzle in path:
                puzzle.printPuzzle()
            return nodes_count

        for child in current_node.puzzle.find_possible_states():
            child = Node(child)
            child_board_tuple = tuple(map(tuple, child.puzzle.puzzle_board))
            if child_board_tuple not in closed_set:
                child.parent = current_node
                child.g = current_node.g + 1
                child.h = heuristic(child.puzzle)
                child.f = child.g + child.h
                heapq.heappush(pqueue, child)
    return None


def print_menu():
    print("------ 8-Puzzle Menu ------")
    print("1. Solve 100 Puzzles using Manhattan Heuristic")
    print("2. Solve 100 Puzzles using Hamming Heuristic")
    print("3. Exit")


if __name__ == '__main__':
    while True:
        puzzles = create_puzzles()
        i = 1
        total_time = 0
        print_menu()
        selection = input("Enter your Choice: ")
        total_nodes = 0

        if selection == "3":
            print("See ya")
            exit(1)
        if selection == "1":
            for puzzle in puzzles:
                print(f"Puzzle {i}: ")
                start = time.time()
                total_nodes += solve_puzzle(puzzle, manhattan_distance)
                end = time.time()
                print()
                total_time += end - start
                i += 1

        elif selection == "2":
            for puzzle in puzzles:
                print(f"Puzzle {i}: ")
                start = time.time()
                total_nodes += solve_puzzle(puzzle, hamming_distance)
                end = time.time()
                total_time += end - start
                print()
                i += 1
        else:
            print("Please enter a valid number")
            print()
            continue

        print(f"Total Time: {total_time}")
        print(f"Mean Time: {total_time / 100}")
        print(f"Total expanded Nodes {total_nodes}")
        print(f"Mean expanded Nodes: {total_nodes / 100}")
        print()

    # start = Puzzle([[2, 3, 4],
    #                [1, 8, 5],
    #                [6, 7, 0]])
    # print(start.is_solvable())
    # solve_puzzle(start, manhattan_distance)
