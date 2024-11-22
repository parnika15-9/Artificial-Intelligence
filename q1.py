import copy
import random
from typing import List, Tuple, Optional

class EightPuzzle:
    def _init_(self, initial_state: List[List[int]]):
        self.current_state = initial_state
        self.goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
        
    def find_empty_tile(self) -> Tuple[int, int]:
        for i in range(3):
            for j in range(3):
                if self.current_state[i][j] == 0:
                    return i, j
        return -1, -1
    
    def get_possible_moves(self, i: int, j: int) -> List[Tuple[int, int]]:
        moves = []
        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            new_i, new_j = i + di, j + dj
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                moves.append((new_i, new_j))
        return moves
    
    def make_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> None:
        i1, j1 = from_pos
        i2, j2 = to_pos
        self.current_state[i1][j1], self.current_state[i2][j2] = \
            self.current_state[i2][j2], self.current_state[i1][j1]
    
    def manhattan_distance(self) -> int:
        distance = 0
        for i in range(3):
            for j in range(3):
                value = self.current_state[i][j]
                if value != 0:
                    goal_i, goal_j = (value-1) // 3, (value-1) % 3
                    distance += abs(i - goal_i) + abs(j - goal_j)
        return distance
    
    def misplaced_tiles(self) -> int:
        count = 0
        for i in range(3):
            for j in range(3):
                if self.current_state[i][j] != 0 and \
                   self.current_state[i][j] != self.goal_state[i][j]:
                    count += 1
        return count
    
    def hill_climbing(self, max_iterations: int = 1000, 
                     heuristic: str = 'manhattan') -> Tuple[bool, int]:
        steps = 0
        
        while steps < max_iterations:
            current_score = self.manhattan_distance() if heuristic == 'manhattan' \
                          else self.misplaced_tiles()
            
            if current_score == 0:
                return True, steps
            
            empty_i, empty_j = self.find_empty_tile()
            possible_moves = self.get_possible_moves(empty_i, empty_j)
            
            best_score = current_score
            best_move = None
            
            for move in possible_moves:
                self.make_move((empty_i, empty_j), move)
                new_score = self.manhattan_distance() if heuristic == 'manhattan' \
                           else self.misplaced_tiles()
                self.make_move(move, (empty_i, empty_j))
                
                if new_score < best_score:
                    best_score = new_score
                    best_move = move
            
            if best_move is None:
                return False, steps
            
            self.make_move((empty_i, empty_j), best_move)
            steps += 1
        
        return False, steps

def print_board(state: List[List[int]]) -> None:
    for row in state:
        print(row)
    print()

def get_user_input():
    print("Enter the initial state of the 8-puzzle (use 0 for empty tile)")
    print("Enter numbers row by row (space-separated):")
    initial_state = []
    for i in range(3):
        row = list(map(int, input(f"Enter row {i+1}: ").strip().split()))
        initial_state.append(row)
    return initial_state

def main():
    print("8-Puzzle Solver using Hill Climbing")
    initial_state = get_user_input()
    
    print("\nSelect heuristic:")
    print("1. Manhattan Distance")
    print("2. Misplaced Tiles")
    choice = input("Enter choice (1 or 2): ")
    
    heuristic = 'manhattan' if choice == '1' else 'misplaced'
    
    puzzle = EightPuzzle(initial_state)
    print("\nInitial State:")
    print_board(puzzle.current_state)
    
    success, steps = puzzle.hill_climbing(heuristic=heuristic)
    
    print(f"Solution found: {success}")
    print(f"Steps taken: {steps}")
    print("Final State:")
    print_board(puzzle.current_state)

if _name_ == "_main_":
    main()
