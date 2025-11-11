/**
 * API Service for Vanishing Tic Tac Toe
 * =====================================
 * 
 * This module handles all communication with the FastAPI backend.
 * It provides clean async functions that the React components can call
 * to interact with the game server, instead of dealing with raw fetch calls.
 * 
 * Backend should be running on http://localhost:8000 for now.
 */

// Base URL for the backend API
// TODO: In production, replace with your EC2 instance URL or domain
const API_BASE_URL = 'http://localhost:8000';

/*
 * Create a new game session.
 * 
 * Calls POST /game/new endpoint to initialize a fresh game.
 * 
 * @returns {Promise<Object>} Game state object with game_id, board, etc.
 * @throws {Error} If the request fails
 */
export const createNewGame = async () => {
  try {
    // Make POST request to create new game
    const response = await fetch(`${API_BASE_URL}/game/new`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Check if response was successful
    if (!response.ok) {
      throw new Error(`Failed to create game: ${response.statusText}`);
    }

    // Parse and return JSON response which we can use in the frontend.
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error creating new game:', error);
    throw error;
  }
};

/*
 * Submit a move to the backend.
 * 
 * Calls POST /game/{game_id}/move with move details.
 * Backend will validate the move, update the game state,
 * and handle the vanishing piece mechanic automatically.
 * 
 * @param {string} gameId - The unique game session ID
 * @param {number} row - Row index (0-2)
 * @param {number} col - Column index (0-2)
 * @param {string} player - The player making the move ("X" or "O")
 * @returns {Promise<Object>} Updated game state
 * @throws {Error} If move is invalid or request fails
 */
export const makeMove = async (gameId, row, col, player) => {
  try {
    // Prepare move data in a JSON object, aligned with pydantic model expected by backend.
    const moveData = {
      row: row,
      col: col,
      player: player,
    };

    // Make POST request to submit move
    const response = await fetch(`${API_BASE_URL}/game/${gameId}/move`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(moveData),
    });

    // Check if response was successful
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || `Failed to make move: ${response.statusText}`);
    }

    // Parse and return updated game state
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error making move:', error);
    throw error;
  }
};

/*
 * Fetch the current game state without making a move.
 * 
 * Calls GET /game/{game_id}/state to retrieve current board.
 * Useful for refreshing/syncing the UI.
 * 
 * @param {string} gameId - The unique game session ID
 * @returns {Promise<Object>} Current game state
 * @throws {Error} If game not found or request fails
 */
export const getGameState = async (gameId) => {
  try {
    // Make GET request to fetch game state. No data needed in body.
    const response = await fetch(`${API_BASE_URL}/game/${gameId}/state`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Check if response was successful
    if (!response.ok) {
      throw new Error(`Failed to get game state: ${response.statusText}`);
    }

    // Parse and return game state
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error getting game state:', error);
    throw error;
  }
};

/*
 * Reset a game to its initial state.
 * 
 * Calls POST /game/{game_id}/reset to clear the board
 * and start fresh with the same game ID.
 * 
 * @param {string} gameId - The unique game session ID
 * @returns {Promise<Object>} Reset game state (empty board)
 * @throws {Error} If game not found or request fails
 */
export const resetGame = async (gameId) => {
  try {
    // Make POST request to reset game
    const response = await fetch(`${API_BASE_URL}/game/${gameId}/reset`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Check if response was successful
    if (!response.ok) {
      throw new Error(`Failed to reset game: ${response.statusText}`);
    }

    // Parse and return reset game state
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error resetting game:', error);
    throw error;
  }
};

/*
 * Check if the backend is healthy and responsive.
 * 
 * Calls GET /health endpoint.
 * 
 * @returns {Promise<Object>} Health status
 * @throws {Error} If backend is unreachable
 */
export const checkHealth = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Health check failed: ${response.statusText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Backend health check failed:', error);
    throw error;
  }
};
