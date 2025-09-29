
"""
Enhanced Flask API Server for Infinite Tic Tac Toe with Blur Preview Feature
This module provides RESTful API endpoints for the frontend to interact with the game
Includes enhanced endpoints for blur preview functionality
Handles CORS for local development and manages game sessions
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from game_logic_main import InfiniteTicTacToe
import json

# Initialize Flask application
app = Flask(__name__)

# Enable CORS for all routes to allow frontend communication
# This is essential for local development when frontend and backend run on different ports
CORS(app)

# Global game instance (in production, this would be session-based or database-stored)
# For local development, we'll use a single game instance
game = InfiniteTicTacToe()

@app.route('/')
def home():
    """
    Home endpoint to verify server is running

    Returns:
        JSON response confirming server status
    """
    return jsonify({
        'message': 'Infinite Tic Tac Toe API Server with Blur Preview is running!',
        'version': '1.1',
        'features': ['blur_preview', 'oldest_piece_tracking'],
        'endpoints': {
            'GET /': 'Server status',
            'GET /game/state': 'Get current game state with blur info',
            'POST /game/move': 'Make a move',
            'POST /game/reset': 'Reset the game',
            'GET /game/players': 'Get player information',
            'GET /game/preview': 'Get blur preview information'
        }
    })

@app.route('/game/state', methods=['GET'])
def get_game_state():
    """
    Get the current state of the game including blur preview information
    Used by frontend to sync with backend state and show blur effects

    Returns:
        JSON response containing complete game state with oldest piece data
    """
    try:
        state = game.get_game_state()
        return jsonify({
            'success': True,
            'data': state
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error getting game state: {str(e)}'
        }), 500

@app.route('/game/preview', methods=['GET'])
def get_blur_preview():
    """
    Get blur preview information for the current player
    Tells frontend which piece should be blurred before the next move

    Returns:
        JSON response with blur preview data for current player
    """
    try:
        current_player = game.current_player
        oldest_piece = game.get_oldest_piece_for_player(current_player)
        will_remove = game.will_remove_piece(current_player)

        return jsonify({
            'success': True,
            'data': {
                'current_player': current_player,
                'should_blur': will_remove,
                'piece_to_blur': oldest_piece,
                'pieces_on_board': len(game.player_moves[current_player])
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error getting blur preview: {str(e)}'
        }), 500

@app.route('/game/move', methods=['POST'])
def make_move():
    """
    Process a player move with enhanced response including blur information
    Expects JSON payload with row and col coordinates

    Expected request body:
    {
        "row": 0,     # Integer 0-2
        "col": 1      # Integer 0-2
    }

    Returns:
        JSON response with move result, updated game state, and next blur info
    """
    try:
        # Parse JSON data from request
        data = request.get_json()

        # Validate that required fields are present
        if not data or 'row' not in data or 'col' not in data:
            return jsonify({
                'success': False,
                'message': 'Missing required fields. Please provide row and col.'
            }), 400

        # Extract and validate coordinates
        try:
            row = int(data['row'])
            col = int(data['col'])
        except (ValueError, TypeError):
            return jsonify({
                'success': False,
                'message': 'Row and col must be integers.'
            }), 400

        # Attempt to make the move
        result = game.make_move(row, col)

        # Add blur preview information for next player
        if result['success']:
            next_player = game.current_player
            result['next_blur_info'] = {
                'current_player': next_player,
                'should_blur': game.will_remove_piece(next_player),
                'piece_to_blur': game.get_oldest_piece_for_player(next_player)
            }

        # Return the result with appropriate status code
        if result['success']:
            return jsonify(result)
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@app.route('/game/reset', methods=['POST'])
def reset_game():
    """
    Reset the game to initial state
    Clears the board and starts a new game

    Returns:
        JSON response confirming reset and new game state with blur info
    """
    try:
        result = game.reset_game()

        # Add initial blur info (should be no blur since it's a fresh start)
        result['blur_info'] = {
            'current_player': game.current_player,
            'should_blur': False,
            'piece_to_blur': None
        }

        return jsonify({
            'success': True,
            'data': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error resetting game: {str(e)}'
        }), 500

@app.route('/game/players', methods=['GET'])
def get_players_info():
    """
    Get information about current players, their piece counts, and oldest pieces
    Useful for frontend to display player status and manage blur effects

    Returns:
        JSON response with comprehensive player information
    """
    try:
        state = game.get_game_state()
        return jsonify({
            'success': True,
            'data': {
                'current_player': state['current_player'],
                'player_piece_counts': {
                    'X': len(state['player_moves']['X']),
                    'Y': len(state['player_moves']['Y'])
                },
                'total_moves': state['total_moves'],
                'oldest_pieces': state['oldest_pieces'],
                'will_remove_next': state['will_remove_next']
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error getting player info: {str(e)}'
        }), 500

@app.errorhandler(404)
def not_found(error):
    """
    Handle 404 errors with JSON response

    Returns:
        JSON error response for undefined endpoints
    """
    return jsonify({
        'success': False,
        'message': 'Endpoint not found'
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    """
    Handle 405 errors (wrong HTTP method) with JSON response

    Returns:
        JSON error response for incorrect HTTP methods
    """
    return jsonify({
        'success': False,
        'message': 'Method not allowed for this endpoint'
    }), 405

if __name__ == '__main__':
    """
    Run the Flask development server
    Server will run on http://localhost:5000 by default
    Debug mode is enabled for development (shows detailed errors)
    """
    print("Starting Enhanced Infinite Tic Tac Toe API Server...")
    print("Server will be available at: http://localhost:5000")
    print("New Features: Blur preview for oldest piece removal")
    print("API endpoints:")
    print("  GET  /                 - Server status")
    print("  GET  /game/state       - Get game state with blur info") 
    print("  POST /game/move        - Make a move")
    print("  POST /game/reset       - Reset game")
    print("  GET  /game/players     - Get player info")
    print("  GET  /game/preview     - Get blur preview info")
    print("\nPress Ctrl+C to stop the server")

    # Start the server
    # host='0.0.0.0' allows external connections (useful for testing from other devices)
    # port=5000 is the default Flask port
    # debug=True enables hot reloading and detailed error messages
    app.run(host='0.0.0.0', port=5000, debug=True)
