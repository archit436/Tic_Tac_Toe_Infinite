
"""
Enhanced Infinite Tic Tac Toe Game Logic with Blur Preview Feature
This module contains the core game logic for infinite tic tac toe where:
- Players can only have 3 pieces on the board at any time
- After placing the 4th piece, the oldest piece disappears
- The oldest piece is identified for UI blur effects before removal
- Standard win conditions apply at any point during the game
"""

class InfiniteTicTacToe:
    def __init__(self):
        """
        Initialize the game with an empty 3x3 board and tracking structures
        """
        # 3x3 board represented as list of lists, empty cells are None
        self.board = [[None for _ in range(3)] for _ in range(3)]

        # Track the order of moves for each player (queue-like structure)
        # This helps us identify which piece to remove when player has >3 pieces
        self.player_moves = {
            'X': [],  # List of (row, col) tuples for player X moves
            'Y': []   # List of (row, col) tuples for player Y moves  
        }

        # Current player ('X' starts first)
        self.current_player = 'X'

        # Game status: 'ongoing', 'X_wins', 'Y_wins', 'draw'
        self.game_status = 'ongoing'

        # Track total moves made (for debugging and game analysis)
        self.total_moves = 0

    def get_oldest_piece_for_player(self, player):
        """
        Get the oldest piece position for a specific player
        This is used by the frontend to show which piece will be removed next

        Args:
            player (str): Player identifier ('X' or 'Y')

        Returns:
            tuple or None: (row, col) of oldest piece if player has moves, None otherwise
        """
        if player in self.player_moves and len(self.player_moves[player]) > 0:
            return self.player_moves[player][0]  # First item is oldest
        return None

    def will_remove_piece(self, player):
        """
        Check if making the next move will cause a piece to be removed for the given player

        Args:
            player (str): Player identifier ('X' or 'Y')

        Returns:
            bool: True if next move will trigger piece removal, False otherwise
        """
        return len(self.player_moves[player]) >= 3

    def make_move(self, row, col):
        """
        Attempt to make a move at the specified position

        Args:
            row (int): Row index (0-2)
            col (int): Column index (0-2)

        Returns:
            dict: Result of the move attempt with status and information
        """
        # Input validation
        if not self._is_valid_position(row, col):
            return {
                'success': False,
                'message': 'Invalid position. Row and column must be between 0-2.',
                'board': self._get_board_state()
            }

        # Check if position is already occupied
        if self.board[row][col] is not None:
            return {
                'success': False,
                'message': 'Position already occupied.',
                'board': self._get_board_state()
            }

        # Check if game is already over
        if self.game_status != 'ongoing':
            return {
                'success': False,
                'message': f'Game is over. Status: {self.game_status}',
                'board': self._get_board_state()
            }

        # Make the move
        self.board[row][col] = self.current_player
        self.player_moves[self.current_player].append((row, col))
        self.total_moves += 1

        # Handle infinite rule: remove oldest piece if player now has more than 3 pieces
        removed_piece = None
        if len(self.player_moves[self.current_player]) > 3:
            # Remove the oldest move (first in the list)
            old_row, old_col = self.player_moves[self.current_player].pop(0)
            self.board[old_row][old_col] = None
            removed_piece = (old_row, old_col)

        # Check for win condition after the move
        winner = self._check_winner()
        if winner:
            self.game_status = f'{winner}_wins'
        elif self._is_board_full() and not winner:
            # This is rare in infinite tic tac toe but possible in edge cases
            self.game_status = 'draw'

        # Switch to the other player
        self.current_player = 'Y' if self.current_player == 'X' else 'X'

        return {
            'success': True,
            'message': 'Move successful',
            'board': self._get_board_state(),
            'removed_piece': removed_piece,
            'current_player': self.current_player,
            'game_status': self.game_status,
            'winner': winner if winner else None
        }

    def _is_valid_position(self, row, col):
        """
        Check if the given position is within board bounds

        Args:
            row (int): Row index
            col (int): Column index

        Returns:
            bool: True if position is valid (0-2 for both row and col)
        """
        return 0 <= row <= 2 and 0 <= col <= 2

    def _check_winner(self):
        """
        Check if there's a winner on the current board state
        Checks all rows, columns, and diagonals

        Returns:
            str or None: Winner ('X' or 'Y') if found, None otherwise
        """
        # Check rows
        for row in self.board:
            if row[0] == row[1] == row[2] and row[0] is not None:
                return row[0]

        # Check columns
        for col in range(3):
            if (self.board[0][col] == self.board[1][col] == self.board[2][col] 
                and self.board[0][col] is not None):
                return self.board[0][col]

        # Check diagonal (top-left to bottom-right)
        if (self.board[0][0] == self.board[1][1] == self.board[2][2] 
            and self.board[0][0] is not None):
            return self.board[0][0]

        # Check diagonal (top-right to bottom-left)
        if (self.board[0][2] == self.board[1][1] == self.board[2][0] 
            and self.board[0][2] is not None):
            return self.board[0][2]

        # No winner found
        return None

    def _is_board_full(self):
        """
        Check if the board is completely full (no empty cells)
        Note: In infinite tic tac toe, this is less likely due to piece removal

        Returns:
            bool: True if board is full, False otherwise
        """
        for row in self.board:
            for cell in row:
                if cell is None:
                    return False
        return True

    def _get_board_state(self):
        """
        Get the current board state in a format suitable for API response

        Returns:
            list: 3x3 list representing the board (None for empty, 'X'/'Y' for pieces)
        """
        return [row[:] for row in self.board]  # Return a deep copy

    def reset_game(self):
        """
        Reset the game to initial state
        Clears board, move history, and resets current player to 'X'

        Returns:
            dict: New game state after reset
        """
        self.board = [[None for _ in range(3)] for _ in range(3)]
        self.player_moves = {'X': [], 'Y': []}
        self.current_player = 'X'
        self.game_status = 'ongoing'
        self.total_moves = 0

        return {
            'message': 'Game reset successfully',
            'board': self._get_board_state(),
            'current_player': self.current_player,
            'game_status': self.game_status
        }

    def get_game_state(self):
        """
        Get complete current game state including blur preview information
        Useful for frontend synchronization and debugging

        Returns:
            dict: Complete game state information with oldest piece data
        """
        return {
            'board': self._get_board_state(),
            'current_player': self.current_player,
            'game_status': self.game_status,
            'player_moves': dict(self.player_moves),  # Copy the moves dictionary
            'total_moves': self.total_moves,
            'oldest_pieces': {
                'X': self.get_oldest_piece_for_player('X'),
                'Y': self.get_oldest_piece_for_player('Y')
            },
            'will_remove_next': {
                'X': self.will_remove_piece('X'),
                'Y': self.will_remove_piece('Y')
            }
        }