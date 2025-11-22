/**
 * React Entry Point
 * =================
 * 
 * This is where React starts. It mounts the App component
 * to the DOM element with id="root" in index.html.
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

// Get the root DOM element
const root = ReactDOM.createRoot(document.getElementById('root'));

// Render the App component
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
