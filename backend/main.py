"""
Vanishing Tic Tac Toe - FastAPI Backend
========================================
This module provides REST API endpoints for the Vanishing Tic Tac Toe game.
It manages game sessions and coordinates between the frontend and game logic.

Endpoints:
- POST /game/new - Create a new game session
- POST /game/{game_id}/move - Submit a player move
- GET /game/{game_id}/state - Get current game state
- POST /game/{game_id}/reset - Reset a game
- GET /health - Health check endpoint
"""

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Optional
from enum import Enum
import uuid
import logging

# Import the game logic we created earlier
from game_logic import VanishingTicTacToe, GameState, Player


# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================
# Set up logging to track API calls and errors
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# PYDANTIC MODELS FOR REQUEST/RESPONSE VALIDATION
# ============================================================================
# These models ensure data consistency between frontend and backend
# Pydantic automatically validates incoming requests and serializes responses to JSON

class MoveRequest(BaseModel):
    """
    Request model for making a move.
    
    Attributes:
        row: Row index (0-2) where player wants to place a piece
        col: Column index (0-2) where player wants to place a piece
        player: The player making the move ("X" or "O")
    """
    row: int
    col: int
    player: str


class GameResponse(BaseModel):
    """
    Response model that returns the current game state.
    Sent after moves or when fetching state.
    
    Attributes:
        game_id: Unique identifier for this game session
        board: 2D array representing the current board state
        current_player: Whose turn it is ("X" or "O")
        state: Current game state (in_progress, x_wins, o_wins, draw)
        move_history_x: List of positions where player X has pieces
        move_history_o: List of positions where player O has pieces
        oldest_piece_x: Position of X's oldest piece (will vanish next if X places a 4th piece)
        oldest_piece_o: Position of O's oldest piece (will vanish next if O places a 4th piece)
    """
    game_id: str
    board: list
    current_player: str
    state: str
    move_history_x: list
    move_history_o: list
    oldest_piece_x: Optional[list]  # [row, col] or None
    oldest_piece_o: Optional[list]  # [row, col] or None


class GameListResponse(BaseModel):
    """
    Response model for listing all active games.
    
    Attributes:
        game_ids: List of all active game session IDs
        total_games: Count of active games
    """
    game_ids: list
    total_games: int


# ============================================================================
# FASTAPI APPLICATION SETUP
# ============================================================================

app = FastAPI(
    title="Vanishing Tic Tac Toe API",
    description="REST API for the Vanishing Tic Tac Toe game with vanishing piece mechanic",
    version="1.0.0"
)

# Configure CORS (Cross-Origin Resource Sharing)
# This allows the React frontend (running on different port/domain) to call these endpoints
# We are essentially dictating who can access our API endpoints.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: In production, restrict to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# GAME SESSION STORAGE
# ============================================================================
# In-memory storage of active game sessions
# Key: game_id (string), Value: VanishingTicTacToe instance
# NOTE: This data is lost when the server restarts.
# For production, use a database (SQLite, PostgreSQL, etc.)
games: Dict[str, VanishingTicTacToe] = {}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def _build_game_response(game_id: str, game: VanishingTicTacToe) -> GameResponse:
    """
    Helper function to convert a game instance into a JSON-serializable GameResponse.
    
    This standardizes the format of game state sent to the frontend.
    
    Args:
        game_id: The unique identifier for this game
        game: The VanishingTicTacToe game instance
        
    Returns:
        GameResponse object ready to be serialized to JSON
    """
    # Get oldest piece positions for display purposes (UI can highlight them)
    oldest_x = game.get_oldest_piece_position(Player.X)
    oldest_o = game.get_oldest_piece_position(Player.O)
    
    # Convert tuples to lists for JSON serialization
    oldest_x_list = [oldest_x[0], oldest_x[1]] if oldest_x else None
    oldest_o_list = [oldest_o[0], oldest_o[1]] if oldest_o else None
    
    return GameResponse(
        game_id=game_id,
        board=game.get_board(),
        current_player=game.get_current_player().value,
        state=game.get_game_state().value,
        move_history_x=game.get_move_history(Player.X),
        move_history_o=game.get_move_history(Player.O),
        oldest_piece_x=oldest_x_list,
        oldest_piece_o=oldest_o_list,
    )


# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/health", tags=["System"])
async def health_check():
    """
    Health check endpoint for a GET request with '/health'.
    Used to verify the backend is running and responsive.
    We use 'async' to allow for non-blocking concurrent requests.
    The tag is for documenatation grouping.

    Returns:
        JSON indicating server is healthy.
    """
    return {"status": "healthy", "service": "Vanishing Tic Tac Toe API"}


@app.post("/game/new", response_model=GameResponse, tags=["Game Management"])
async def create_new_game():
    """
    Create a new game session in response to a POST request with '/game/new'.
    
    Initializes a fresh 3x3 board with Player X to move first.
    Stores the game in memory and returns the initial state.
    
    Returns:
        GameResponse with initial game state (empty board, X to move)
    """
    # Generate a unique ID for this game session
    game_id = str(uuid.uuid4())
    
    # Create a new game instance
    game = VanishingTicTacToe()

    # Store the game in our in-memory storage
    games[game_id] = game
    
    logger.info(f"Created new game: {game_id}")
    
    # Return the initial game state
    return _build_game_response(game_id, game)


@app.post("/game/{game_id}/move", response_model=GameResponse, tags=["Gameplay"])
async def make_move(game_id: str, move_request: MoveRequest):
    """
    Submit a move for the current player, as response to a POST request with '/game/{game_id}/move'.
    The frontend also needs to provide the move details in the request body.
    
    Validates the move, executes it on the game board, and returns the updated state.
    Includes the vanishing piece mechanic: if a player has 3 pieces and places a 4th,
    their oldest piece automatically disappears.
    
    Args:
        game_id: The unique ID of the game session
        move_request: MoveRequest containing row, col, and player
        
    Returns:
        GameResponse with updated game state after the move
        
    Raises:
        HTTPException 404: If game_id doesn't exist
        HTTPException 400: If move is invalid or it's not the player's turn
    """
    # Check if game exists
    if game_id not in games:
        logger.warning(f"Attempted move on non-existent game: {game_id}")
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = games[game_id]
    
    # Validate it's the correct player's turn
    expected_player = game.get_current_player().value
    if move_request.player != expected_player:
        logger.warning(f"Game {game_id}: Player {move_request.player} attempted move out of turn")
        raise HTTPException(
            status_code=400,
            detail=f"It's {expected_player}'s turn, not {move_request.player}'s"
        )
    
    # Attempt to make the move
    move_successful = game.make_move(move_request.row, move_request.col)
    
    if not move_successful:
        logger.warning(f"Game {game_id}: Invalid move at ({move_request.row}, {move_request.col})")
        raise HTTPException(status_code=400, detail="Invalid move")
    
    logger.info(f"Game {game_id}: Player {move_request.player} moved to ({move_request.row}, {move_request.col})")
    
    # Return updated game state
    return _build_game_response(game_id, game)


@app.get("/game/{game_id}/state", response_model=GameResponse, tags=["Gameplay"])
async def get_game_state(game_id: str):
    """
    Fetch the current state of a game without making a move, in response to a GET request with '/game/{game_id}/state'.
    
    Useful for the frontend to refresh/sync the board state without modifying it.
    
    Args:
        game_id: The unique ID of the game session
        
    Returns:
        GameResponse with current game state
        
    Raises:
        HTTPException 404: If game_id doesn't exist
    """
    # Check if game exists
    if game_id not in games:
        logger.warning(f"Attempted to fetch state for non-existent game: {game_id}")
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = games[game_id]
    return _build_game_response(game_id, game)


@app.post("/game/{game_id}/reset", response_model=GameResponse, tags=["Game Management"])
async def reset_game(game_id: str):
    """
    Reset a game to its initial state, in response to a POST request with '/game/{game_id}/reset'.
    
    Clears the board, resets move histories, and gives Player X the first move.
    Keeps the same game_id.
    
    Args:
        game_id: The unique ID of the game session to reset
        
    Returns:
        GameResponse with reset game state (empty board, X to move)
        
    Raises:
        HTTPException 404: If game_id doesn't exist
    """
    # Check if game exists
    if game_id not in games:
        logger.warning(f"Attempted reset on non-existent game: {game_id}")
        raise HTTPException(status_code=404, detail="Game not found")
    
    game = games[game_id]
    game.reset()
    
    logger.info(f"Game {game_id} reset to initial state")
    
    return _build_game_response(game_id, game)


@app.get("/games", response_model=GameListResponse, tags=["System"])
async def list_active_games():
    """
    List all currently active game sessions, in response to a GET request with '/games'.
    
    Useful for debugging and monitoring. In production, you might want to restrict
    access to this endpoint or move it behind authentication.
    
    Returns:
        GameListResponse with list of active game IDs and count
    """
    # Extract all active game IDs
    game_ids = list(games.keys())
    # Package using pydantic model and return.
    return GameListResponse(
        game_ids=game_ids,
        total_games=len(game_ids)
    )


@app.delete("/game/{game_id}", tags=["Game Management"])
async def delete_game(game_id: str):
    """
    Delete a game session (clean up memory), in response to a DELETE request with '/game/{game_id}'.
    
    Use this when a player is done with a game to free up memory.
    
    Args:
        game_id: The unique ID of the game session to delete
        
    Returns:
        Confirmation message
        
    Raises:
        HTTPException 404: If game_id doesn't exist
    """
    # Check if game exists
    if game_id not in games:
        logger.warning(f"Attempted deletion of non-existent game: {game_id}")
        raise HTTPException(status_code=404, detail="Game not found")
    
    # Remove the game from storage
    del games[game_id]
    
    logger.info(f"Deleted game: {game_id}")
    
    return {"message": f"Game {game_id} deleted successfully"}


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================
# Run the server with: uvicorn main:app --reload
# The --reload flag enables auto-restart when code changes (useful during development)
# This FastAPI server will keep running and listening for requests on localhost:8000
#
# In production, run with: uvicorn main:app --host 0.0.0.0 --port 8000
# This exposes the API to external requests on port 8000

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)