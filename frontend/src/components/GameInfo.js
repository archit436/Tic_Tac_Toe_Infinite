/**
 * GameInfo Component
 * ==================
 * 
 * Displays game status information:
 * - Current player's turn
 * - Game state (in progress, won, draw)
 * - Move history counts
 */

import React from 'react';
import './GameInfo.css';

/**
 * GameInfo component for displaying game status.
 * 
 * @param {string} currentPlayer - Whose turn it is ("X" or "O")
 * @param {string} gameState - Current game state (in_progress, x_wins, o_wins, draw)
 * @param {Array} moveHistoryX - List of X's move positions
 * @param {Array} moveHistoryO - List of O's move positions
 */
const GameInfo = ({ currentPlayer, gameState, moveHistoryX, moveHistoryO }) => {
  
  /**
   * Format the game state for display.
   * 
   * @returns {string} Human-readable game status
   */
  const getStatusMessage = () => {
    switch (gameState) {
      case 'in_progress':
        return `Current Turn: Player ${currentPlayer}`;
      case 'x_wins':
        return '🎉 Player X Wins!';
      case 'o_wins':
        return '🎉 Player O Wins!';
      case 'draw':
        return '🤝 Game is a Draw!';
      default:
        return 'Unknown game state';
    }
  };

  /**
   * Get CSS class for status based on game state.
   * 
   * @returns {string} CSS class name
   */
  const getStatusClass = () => {
    if (gameState === 'in_progress') {
      return 'status-progress';
    } else if (gameState === 'x_wins' || gameState === 'o_wins') {
      return 'status-win';
    } else if (gameState === 'draw') {
      return 'status-draw';
    }
    return '';
  };

  // Render the game info panel.
  return (
    // Main container for game information
    <div className="game-info">
      {/* Display current game status */}
      <div className={`status ${getStatusClass()}`}>
        {getStatusMessage()}
      </div>

      {/* Info about vanishing mechanic */}
      {(moveHistoryX.length >= 3 || moveHistoryO.length >= 3) && (
        <div className="vanish-warning">
          ⚠️ Highlighted pieces will vanish on next move!
        </div>
      )}
    </div>
  );
};

// Make the GameInfo component available for import in other files.
export default GameInfo;
