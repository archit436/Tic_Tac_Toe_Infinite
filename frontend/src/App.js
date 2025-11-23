/**
 * Vanishing Tic Tac Toe - React App
 * ==================================
 * 
 * Main application component that orchestrates the game.
 * Manages game state, handles user interactions, and coordinates
 * communication with the FastAPI backend.
 *  
 * This is the root component that ties together the Board and GameInfo components.
 */

import React, { useState, useEffect } from 'react';
import Board from './components/Board';
import GameInfo from './components/GameInfo';
import { createNewGame, makeMove, resetGame, checkHealth } from './api';
import './App.css';

function App() {
  // =========================================================================
  // STATE MANAGEMENT
  // =========================================================================
  
  // Game session ID from backend
  const [gameId, setGameId] = useState(null);
  
  // 2D array representing the board state
  const [board, setBoard] = useState([]);
  
  // Current player ("X" or "O")
  const [currentPlayer, setCurrentPlayer] = useState('X');
  
  // Game state (in_progress, x_wins, o_wins, draw)
  const [gameState, setGameState] = useState('in_progress');
  
  // Move history for each player
  const [moveHistoryX, setMoveHistoryX] = useState([]);
  const [moveHistoryO, setMoveHistoryO] = useState([]);
  
  // Oldest piece positions for highlighting
  const [oldestPieceX, setOldestPieceX] = useState(null);
  const [oldestPieceO, setOldestPieceO] = useState(null);

  // Winning line coordinates for victory animation
  const [winningLine, setWinningLine] = useState(null);

  // Loading and error states
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [backendHealthy, setBackendHealthy] = useState(false);

  // =========================================================================
  // INITIALIZATION
  // =========================================================================
  
  /**
   * Check backend health and initialize game on component mount.
   */
  useEffect(() => {
    const initializeApp = async () => {
      try {
        // Check if backend is running
        await checkHealth();
        setBackendHealthy(true);
        
        // Create initial game
        await handleNewGame();
      } catch (err) {
        setBackendHealthy(false);
        setError('Cannot connect to backend. Make sure the FastAPI server is running on http://localhost:8000');
      }
    };

    initializeApp();
  }, []); // Empty dependency array = run once on mount

  // =========================================================================
  // GAME STATE UPDATERS
  // =========================================================================
  
  /**
   * Update all game state from backend response.
   *
   * @param {Object} gameData - Game state object from backend
   */
  const updateGameState = (gameData) => {
    setGameId(gameData.game_id);
    setBoard(gameData.board);
    setCurrentPlayer(gameData.current_player);
    setGameState(gameData.state);
    setMoveHistoryX(gameData.move_history_x);
    setMoveHistoryO(gameData.move_history_o);
    setOldestPieceX(gameData.oldest_piece_x);
    setOldestPieceO(gameData.oldest_piece_o);
    setWinningLine(gameData.winning_line);
  };

  // =========================================================================
  // EVENT HANDLERS
  // =========================================================================
  
  /**
   * Handle creating a new game.
   * Calls backend to initialize fresh game session.
   */
  const handleNewGame = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      // Call backend to create new game
      const gameData = await createNewGame();
      
      // Update local state with new game data
      updateGameState(gameData);
      
      console.log('New game created:', gameData.game_id);
    } catch (err) {
      setError(`Failed to create new game: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Handle cell click event.
   * Submits move to backend and updates state.
   * 
   * @param {number} row - Row index (0-2)
   * @param {number} col - Column index (0-2)
   */
  const handleCellClick = async (row, col) => {
    // Prevent moves if game is over
    if (gameState !== 'in_progress') {
      return;
    }

    // Prevent moves if cell is already occupied
    if (board[row][col] !== ' ') {
      return;
    }

    // Prevent moves while loading
    if (isLoading) {
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      // Submit move to backend
      const gameData = await makeMove(gameId, row, col, currentPlayer);
      
      // Update local state with new game data
      updateGameState(gameData);
      
      console.log(`Player ${currentPlayer} moved to (${row}, ${col})`);
    } catch (err) {
      setError(`Failed to make move: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  /**
   * Handle reset button click.
   * Resets the current game to initial state.
   */
  const handleReset = async () => {
    if (!gameId) {
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      // Call backend to reset game
      const gameData = await resetGame(gameId);
      
      // Update local state with reset game data
      updateGameState(gameData);
      
      console.log('Game reset');
    } catch (err) {
      setError(`Failed to reset game: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  // =========================================================================
  // RENDER
  // =========================================================================

  return (
    <div className="App">
      {/* Header */}
      <header className="App-header">
        <h1>♾️ Vanishing Tic Tac Toe</h1>
        <p className="subtitle">Each player can only have 3 pieces at a time</p>
      </header>

      {/* Backend status indicator */}
      {!backendHealthy && (
        <div className="error-banner">
          ⚠️ Backend is not connected. Please start the FastAPI server.
        </div>
      )}

      {/* Main game area */}
      <main className="game-container">
        {/* Display error messages */}
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {/* Game info display */}
        {board.length > 0 && (
          <GameInfo
            currentPlayer={currentPlayer}
            gameState={gameState}
            moveHistoryX={moveHistoryX}
            moveHistoryO={moveHistoryO}
          />
        )}

        {/* Game board */}
        {board.length > 0 && (
          <Board
            board={board}
            onCellClick={handleCellClick}
            oldestPieceX={oldestPieceX}
            oldestPieceO={oldestPieceO}
            winningLine={winningLine}
            gameState={gameState}
          />
        )}

        {/* Control buttons */}
        <div className="controls">
          <button 
            className="btn btn-reset"
            onClick={handleReset}
            disabled={isLoading || !gameId}
          >
            Reset Game
          </button>
          <button 
            className="btn btn-new"
            onClick={handleNewGame}
            disabled={isLoading}
          >
            New Game
          </button>
        </div>

        {/* Loading indicator */}
        {isLoading && (
          <div className="loading">
            Processing...
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="App-footer">
        <p>Vanishing piece mechanic: oldest piece disappears after 3 pieces</p>
      </footer>
    </div>
  );
}

export default App;
