"""
Infinite Tic Tac Toe - Core Game Logic
======================================
This module implements the game logic for a modified Tic Tac Toe where:
- Standard 3x3 grid
- Each player can only have 3 pieces on the board at any time
- After a player's 3rd move, their oldest piece vanishes when they place a new piece
- Standard win conditions apply (3 in a row horizontally, vertically, or diagonally)
"""

from typing import List, Tuple, Optional
from enum import Enum

# We start by defining two Enum classes that do not need to be initalized.
# They are both defined by default as singleton instances.
class Player(Enum):
    """
    Enum to represent the two players in the game.
    Using an Enum allows you to define constants in a manner which makes code more readable.
    Enums have name and value components. we make them the same here for the players for simplicity.
    """
    X = "X"  # Player 1
    O = "O"  # Player 2
    EMPTY = " "  # Empty cell


class GameState(Enum):
    """
    Enum to represent the current state of the game.
    """
    IN_PROGRESS = "in_progress"
    X_WINS = "x_wins"
    O_WINS = "o_wins"
    DRAW = "draw"


class InfiniteTicTacToe:
    """
    Main game class that manages the board state and game logic.
    """
    
    def __init__(self):
        """
        Constructor function - called everytime a new instance of the class is created.
        Initialize a new game with an empty 3x3 board and tracking structures.
        We use type hints to indicate the expected types of attributes.
        """
        # Create 3x3 board, initialized with empty cells
        # Board is represented as a 2D list: board[row][col]
        self.board: List[List[str]] = [[Player.EMPTY.value for _ in range(3)] for _ in range(3)]
        
        # Track move history for each player to identify the oldest piece
        # Each entry is a tuple (row, col) representing a move position
        self.move_history_x: List[Tuple[int, int]] = []
        self.move_history_o: List[Tuple[int, int]] = []
        
        # Track whose turn it is (X always starts)
        self.current_player: Player = Player.X
        
        # Track game state
        self.state: GameState = GameState.IN_PROGRESS

    # We define several modifier and getter methods to interact with the elements of the class. 
      
    def get_board(self) -> List[List[str]]:
        """
        Get the current board state.
        
        Returns:
            2D list representing the board (3x3 grid)
        """
        return self.board
    
    def get_current_player(self) -> Player:
        """
        Get the player whose turn it currently is.
        
        Returns:
            Player enum (X or O)
        """
        return self.current_player
    
    def get_game_state(self) -> GameState:
        """
        Get the current state of the game.
        
        Returns:
            GameState enum indicating if game is in progress, won, or drawn
        """
        return self.state
    
    def get_move_history(self, player: Player) -> List[Tuple[int, int]]:
        """
        Get the move history for a specific player.
        
        Args:
            player: The player whose history to retrieve
            
        Returns:
            List of (row, col) tuples representing move positions in chronological order
        """
        if player == Player.X:
            return self.move_history_x.copy()
        elif player == Player.O:
            return self.move_history_o.copy()
        return []
    
    def is_valid_move(self, row: int, col: int) -> bool:
        """
        Check if a move to the specified position is valid.
        
        A move is valid if:
        1. The position is within the board bounds (0-2 for both row and col)
        2. The cell is currently empty
        3. The game is still in progress
        
        Args:
            row: Row index (0-2)
            col: Column index (0-2)
            
        Returns:
            True if the move is valid, False otherwise
        """
        # Check if game is still in progress
        if self.state != GameState.IN_PROGRESS:
            return False
        
        # Check if position is within board bounds
        if row < 0 or row > 2 or col < 0 or col > 2:
            return False
        
        # Check if cell is empty
        if self.board[row][col] != Player.EMPTY.value:
            return False
        
        return True
    
    def make_move(self, row: int, col: int) -> bool:
        """
        Execute a move for the current player.
        
        This method handles the core vanishing piece mechanic:
        1. Validates the move
        2. If player has 3 pieces already, removes their oldest piece
        3. Places the new piece
        4. Updates move history
        5. Checks for win/draw conditions
        6. Switches to the other player
        
        Args:
            row: Row index (0-2)
            col: Column index (0-2)
            
        Returns:
            True if move was successful, False if invalid
        """
        # Validate the move
        if not self.is_valid_move(row, col):
            return False
        
        # Get the move history for the current player
        if self.current_player == Player.X:
            move_history = self.move_history_x
        else:
            move_history = self.move_history_o
        
        # VANISHING PIECE MECHANIC:
        # If player already has 3 pieces on the board, remove the oldest one
        if len(move_history) >= 3:
            # Get the oldest move (first in the list)
            oldest_row, oldest_col = move_history[0]
            
            # Remove the oldest piece from the board
            self.board[oldest_row][oldest_col] = Player.EMPTY.value
            
            # Remove the oldest move from history
            move_history.pop(0)
        
        # Place the new piece on the board
        self.board[row][col] = self.current_player.value
        
        # Add the new move to the player's history
        move_history.append((row, col))
        
        # Check if this move resulted in a win
        if self._check_win(self.current_player):
            self.state = GameState.X_WINS if self.current_player == Player.X else GameState.O_WINS
        # Check if the board is full (draw condition)
        elif self._check_draw():
            self.state = GameState.DRAW
        
        # Switch to the other player for the next turn
        self.current_player = Player.O if self.current_player == Player.X else Player.X
        
        return True
    
    def _check_win(self, player: Player) -> bool:
        """
        Check if the specified player has won the game.
        
        Win conditions:
        - 3 in a row horizontally
        - 3 in a row vertically
        - 3 in a row diagonally
        
        Args:
            player: The player to check for a win
            
        Returns:
            True if the player has won, False otherwise
        """
        symbol = player.value
        
        # Check all rows for 3 in a row
        for row in range(3):
            if all(self.board[row][col] == symbol for col in range(3)):
                return True
        
        # Check all columns for 3 in a row
        for col in range(3):
            if all(self.board[row][col] == symbol for row in range(3)):
                return True
        
        # Check top-left to bottom-right diagonal
        if all(self.board[i][i] == symbol for i in range(3)):
            return True
        
        # Check top-right to bottom-left diagonal
        if all(self.board[i][2-i] == symbol for i in range(3)):
            return True
        
        return False
    
    def _check_draw(self) -> bool:
        """
        Check if the game is a draw.
        
        A draw occurs when:
        - The board is full (all cells occupied)
        - No player has won
        
        Note: With the vanishing piece mechanic, a full board is rare but possible
        if both players keep blocking each other.
        
        Returns:
            True if the game is a draw, False otherwise
        """
        # Check if any empty cells exist
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == Player.EMPTY.value:
                    return False
        
        # Board is full and no one has won (otherwise _check_win would have caught it)
        return True
    
    def reset(self):
        """
        Reset the game to initial state.
        Clears the board, move histories, and resets to Player X's turn.
        """
        self.board = [[Player.EMPTY.value for _ in range(3)] for _ in range(3)]
        self.move_history_x = []
        self.move_history_o = []
        self.current_player = Player.X
        self.state = GameState.IN_PROGRESS
    
    def get_oldest_piece_position(self, player: Player) -> Optional[Tuple[int, int]]:
        """
        Get the position of the oldest piece for a player.
        This is useful for the frontend to highlight which piece will vanish next.
        
        Args:
            player: The player whose oldest piece to find
            
        Returns:
            Tuple of (row, col) if player has pieces on board, None otherwise
        """
        move_history = self.move_history_x if player == Player.X else self.move_history_o
        
        if len(move_history) > 0:
            return move_history[0]
        return None
    
    def print_board(self):
        """
        Print the board to console in a readable format.
        Useful for debugging and testing.
        """
        print("\n  0   1   2")
        for i, row in enumerate(self.board):
            print(f"{i} {' | '.join(row)}")
            if i < 2:
                print("  " + "-" * 11)
        print()


# Example usage and testing
if __name__ == "__main__":
    """
    Simple test to demonstrate the game mechanics.
    Run this file directly to see the vanishing piece mechanic in action.
    """
    game = InfiniteTicTacToe()
    
    print("=== Infinite Tic Tac Toe Demo ===")
    print("Each player can only have 3 pieces on the board.")
    print("After the 3rd piece, the oldest piece vanishes.\n")
    
    # Simulate a game
    moves = [
        (0, 0),  # X
        (1, 1),  # O
        (0, 1),  # X
        (0, 2),  # O
        (2, 2),  # X - X now has 3 pieces
        (2, 0),  # O - O now has 3 pieces
        (1, 0),  # X - X's piece at (0,0) vanishes, new piece at (1,0)
        (1, 2),  # O - O's piece at (1,1) vanishes, new piece at (1,2)
    ]
    
    for i, (row, col) in enumerate(moves):
        player = game.get_current_player()
        print(f"Move {i+1}: Player {player.value} places at ({row}, {col})")
        
        if game.make_move(row, col):
            game.print_board()
            
            # Show move history
            print(f"X's pieces: {game.get_move_history(Player.X)}")
            print(f"O's pieces: {game.get_move_history(Player.O)}\n")
            
            # Check game state
            state = game.get_game_state()
            if state != GameState.IN_PROGRESS:
                print(f"Game Over! Result: {state.value}")
                break
        else:
            print("Invalid move!")
