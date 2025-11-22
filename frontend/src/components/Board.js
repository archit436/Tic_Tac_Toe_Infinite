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
 */
const Board = ({ board, onCellClick, oldestPieceX, oldestPieceO }) => {
  
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
    </div>
  );
};
// Make the Board component available for import in other files.
export default Board;
