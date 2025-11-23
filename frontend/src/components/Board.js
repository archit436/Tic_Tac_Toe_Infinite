/**
 * Board Component
 * ===============
 * 
 * Displays the 3x3 Tic Tac Toe grid.
 * Manages cell rendering and click handling.
 * Highlights oldest pieces that will vanish.
 */

import React from 'react';
import Cell from './Cell';
import './Board.css';

/**
 * Board component that renders the 3x3 grid.
 *
 * @param {Array<Array<string>>} board - 2D array representing board state
 * @param {function} onCellClick - Handler for cell clicks (row, col). Handled by the parent component (App).
 * @param {Array<number>|null} oldestPieceX - Position of X's oldest piece [row, col]
 * @param {Array<number>|null} oldestPieceO - Position of O's oldest piece [row, col]
 * @param {Array<Array<number>>|null} winningLine - Array of three [row, col] positions forming the winning line
 * @param {string} gameState - Current game state (in_progress, x_wins, o_wins, draw)
 */
const Board = ({ board, onCellClick, oldestPieceX, oldestPieceO, winningLine, gameState }) => {
  
  /**
   * Helper Function to check if a cell position is the oldest piece.
   *
   * @param {number} row - Row index
   * @param {number} col - Column index
   * @returns {boolean} True if this is an oldest piece
   */
  const isOldestPiece = (row, col) => {
    // Check if this cell matches X's oldest piece
    if (oldestPieceX && oldestPieceX[0] === row && oldestPieceX[1] === col) {
      return true;
    }
    // Check if this cell matches O's oldest piece
    if (oldestPieceO && oldestPieceO[0] === row && oldestPieceO[1] === col) {
      return true;
    }
    return false;
  };

  /**
   * Calculate SVG line coordinates for the winning line.
   * Converts grid positions to pixel coordinates for drawing.
   *
   * @returns {Object|null} Object with x1, y1, x2, y2 coordinates or null
   */
  const getLineCoordinates = () => {
    if (!winningLine || winningLine.length !== 3) {
      return null;
    }

    // Cell size is 100px (as defined in Cell.css)
    // Board has 20px padding (as defined in Board.css)
    const cellSize = 100;
    const boardPadding = 20;
    const offset = cellSize / 2; // Center of cell

    // Get start and end positions
    const start = winningLine[0];
    const end = winningLine[2];

    // Calculate center coordinates for start and end
    // Add boardPadding to account for the board's padding
    let x1 = start[1] * cellSize + offset + boardPadding;
    let y1 = start[0] * cellSize + offset + boardPadding;
    let x2 = end[1] * cellSize + offset + boardPadding;
    let y2 = end[0] * cellSize + offset + boardPadding;

    // Extend the line by 15% on each side (but not to the edge)
    const dx = x2 - x1;
    const dy = y2 - y1;
    const extension = 0.15;

    x1 -= dx * extension;
    y1 -= dy * extension;
    x2 += dx * extension;
    y2 += dy * extension;

    return { x1, y1, x2, y2 };
  };

  const lineCoords = getLineCoordinates();

  /**
   * Get the color for the victory line based on the winner.
   * X gets cyan (#00d9ff), O gets pink (#ff006e)
   */
  const getLineColor = () => {
    if (gameState === 'x_wins') {
      return '#00d9ff'; // Cyan for X
    } else if (gameState === 'o_wins') {
      return '#ff006e'; // Pink for O
    }
    return '#ffd700'; // Default gold (shouldn't be used)
  };

  // Render the 3x3 board grid using Cell components.
  return (
    // Main Container that will hold all 9 cells.
    <div className="board">
      {/* Iterate through each row  of the board from backend*/}
      {board.map((row, rowIndex) => (
        // Container for a single row
        <div key={rowIndex} className="board-row">
          {/* Iterate through each cell in the row */}
          {row.map((cell, colIndex) => (
            // As defined in Cell.js
            <Cell
              key={`${rowIndex}-${colIndex}`} // Unique key for each cell
              value={cell}
              onClick={() => onCellClick(rowIndex, colIndex)}
              isOldest={isOldestPiece(rowIndex, colIndex)}
            />
          ))}
        </div>
      ))}

      {/* Victory line overlay */}
      {lineCoords && (
        <svg className="victory-line-overlay" viewBox="0 0 340 340">
          <line
            className="victory-line"
            x1={lineCoords.x1}
            y1={lineCoords.y1}
            x2={lineCoords.x2}
            y2={lineCoords.y2}
            stroke={getLineColor()}
            strokeDasharray="1000"
            strokeDashoffset="1000"
          />
        </svg>
      )}
    </div>
  );
};
// Make the Board component available for import in other files.
export default Board;
