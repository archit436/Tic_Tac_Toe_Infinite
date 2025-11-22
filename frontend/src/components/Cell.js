/**
 * Cell Component
 * ==============
 * 
 * Represents a single cell in the 3x3 Tic Tac Toe board.
 * Displays X, O, or empty space.
 * Highlights the oldest piece that will vanish next.
 */

import React from 'react';
import './Cell.css';

/**
 * Cell component for a single board position.
 * 
 * @param {string} value - The content of the cell ("X", "O", or " ")
 * @param {function} onClick - Handler when cell is clicked. The parent component dictates this action.
 * @param {boolean} isOldest - Whether this is the oldest piece (will vanish next)
 * 
 * These parameters are passed by the parent component (Board).
 */
const Cell = ({ value, onClick, isOldest }) => {
  // Determine CSS class based on cell state.
  // It is either 'cell' or 'cell oldest'.
  const cellClass = `cell ${isOldest ? 'oldest' : ''}`;

  // Render the button representing the cell.
  return (
    <button 
      className={cellClass} // Apply dynamic class
      onClick={onClick} // Attach click handler
      data-value={value} // Add data attribute to help with styling
    >
      {/* Display X or O, or empty space */}
      {value}
    </button>
  );
};

// Make the Cell component available for import in other files.
export default Cell;
