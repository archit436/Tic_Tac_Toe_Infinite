/* ========================================================================== 
   PHASE 1: SIMPLE UI INTERACTIONS FOR NEON THEME
   Demo functions moved to global scope for console testing
   ========================================================================== */

// Global demo functions that can be called from browser console
function showWinDemo() {
    document.getElementById('win-message').textContent = 'PLAYER X WINS!';
    document.getElementById('win-overlay').classList.add('show');
}

function switchActivePlayerDemo() {
    const playerX = document.getElementById('player-x');
    const playerO = document.getElementById('player-o');
    const gameStatusText = document.getElementById('game-status');
    
    if (playerX.classList.contains('active')) {
        playerX.classList.remove('active');
        playerO.classList.add('active');
        gameStatusText.textContent = 'PLAYER O TURN';
    } else {
        playerO.classList.remove('active');
        playerX.classList.add('active');
        gameStatusText.textContent = 'PLAYER X TURN';
    }
}

// Wait for page to fully load before setting up event handlers
document.addEventListener('DOMContentLoaded', function() {
    
    /* ========================================================================== 
       BUTTON EVENT HANDLERS
       ========================================================================== */
    
    // New game button with visual feedback
    document.getElementById('new-game-btn').addEventListener('click', function() {
        console.log('New Game clicked - will connect to Python backend');
        this.style.boxShadow = '0 0 25px #00ffff';
        setTimeout(() => {
            this.style.boxShadow = '';
        }, 200);
    });
    
    // Reset button with visual feedback
    document.getElementById('reset-btn').addEventListener('click', function() {
        console.log('Reset clicked - will connect to Python backend');
        this.style.boxShadow = '0 0 25px #ff6600';
        setTimeout(() => {
            this.style.boxShadow = '';
        }, 200);
    });
    
    // Continue button in win notification
    document.getElementById('continue-btn').addEventListener('click', function() {
        document.getElementById('win-overlay').classList.remove('show');
        console.log('Continue clicked - game continues');
    });
    
    /* ========================================================================== 
       GAME BOARD INTERACTIONS
       ========================================================================== */
    
    // Add click handlers to all game cells
    document.querySelectorAll('.cell').forEach(cell => {
        cell.addEventListener('click', function() {
            const row = this.dataset.row;
            const col = this.dataset.col;
            
            console.log(`Cell clicked: row ${row}, col ${col}`);
            
            if (!this.textContent) { // Only if cell is empty
                this.style.boxShadow = '0 0 20px #ff00ff';
                setTimeout(() => {
                    this.style.boxShadow = '';
                }, 300);
            }
        });
        
        // Hover effects
        cell.addEventListener('mouseenter', function() {
            if (!this.textContent) {
                this.style.transform = 'scale(1.05)';
            }
        });
        
        cell.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });
    
    console.log('Neon Tic Tac Toe UI loaded - ready for Phase 2 Python integration');
    console.log('Demo functions available: showWinDemo() and switchActivePlayerDemo()');
});
/* ========================================================================== 
   END OF FILE
   ========================================================================== */