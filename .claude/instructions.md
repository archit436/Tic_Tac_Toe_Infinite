# Claude Code Instructions for Vanishing Tic Tac Toe Project

## Communication Style & Approach

### Problem-Solving Philosophy
- **Balance user input with expertise**: Take the user's suggestions seriously, but always offer alternative approaches when they exist
- **Understand intent, not just words**: The user may have limited knowledge in certain areas, so focus on understanding their goal rather than being fixated on the exact question asked
- **Simplicity first**: Don't unnecessarily complicate solutions. Keep things straightforward unless complexity is genuinely needed
- **Question assumptions**: If a request seems problematic or there's a better way, explain the tradeoffs and suggest alternatives

### Code Quality Standards
- **Comprehensive commenting**: Every code module must be thoroughly commented
  - Explain what each section/function does in plain language
  - Comments should help someone unfamiliar with the language understand the code
  - Comments should also serve as refreshers for someone returning to the code after time away
  - Balance: Don't need essay-length comments, but must be comprehensive enough to understand flow and purpose

### Dependency Management
- **Always update requirements.txt**: Every time new code is generated that introduces new dependencies:
  - Suggest additions to requirements.txt
  - Include version numbers when relevant
  - Explain why the dependency is needed

### Project Context Awareness
- **Reference the project plan**: Always consult [Plan_Draft_6:11.md](Plan_Draft_6:11.md) before generating responses
  - Ensure solutions align with the overall architecture
  - Consider how changes affect frontend, backend, and RL module integration
  - Keep deployment strategy (AWS S3/CloudFront + EC2) in mind

---

## Project Overview: Vanishing Tic Tac Toe

### Game Mechanics (CRITICAL - Reference This for All Code)
This is **not standard Tic Tac Toe**. The game has a unique vanishing piece mechanic:

- **Board**: 3x3 grid (standard Tic Tac Toe)
- **Vanishing Rule**: Each player can only have **3 pieces on the board at any time**
- **After turn 3**: When a player places their 4th piece (and beyond), their **oldest piece vanishes** from the board
- This creates dynamic gameplay where positions constantly change

**Always keep this mechanic in mind when writing game logic, UI code, or AI training code.**

### Project Goals
- Build a web-based Vanishing Tic Tac Toe game
- Support two modes:
  1. **Player vs Player** (PvP)
  2. **Player vs Reinforcement Learning AI** (PvAI)
- Deploy as a web application using AWS services

### Technology Stack

#### Frontend
- **React.js**: Interactive UI, game board visualization
- Handles player clicks, piece placement/removal animations
- REST API communication with backend
- Visual indicators for which piece will vanish next

#### Backend
- **FastAPI (Python)**: RESTful API server
- Core game logic and move validation
- Game session management
- Integration with RL model for AI moves
- Key endpoints:
  - `POST /game/new` - Start new game
  - `POST /game/{id}/move` - Submit move
  - `GET /game/{id}/state` - Get current state
  - `POST /game/{id}/reset` - Reset game

#### AI/ML Module
- **Python** (Q-Learning or Stable-Baselines3)
- Trained to understand the vanishing piece constraint
- Called by backend during PvAI mode

#### Deployment (AWS)
- **Frontend**: S3 + CloudFront (static hosting)
- **Backend**: EC2 instance (FastAPI server)
- **Database**: SQLite on EC2 (for session persistence)
- **Future**: Consider scaling options as needed

---

## Development Guidelines

### When Writing Code
1. **Comment thoroughly** - Assume the user might not know the language well
2. **Implement the vanishing mechanic correctly** - Test edge cases
3. **Security awareness** - Watch for vulnerabilities (XSS, injection, etc.)
4. **Check for existing code** - Read relevant files before suggesting new ones
5. **Update dependencies** - Note any new packages needed in requirements.txt

### When Suggesting Solutions
1. **Offer alternatives** - Don't just implement the first idea
2. **Explain tradeoffs** - Help the user make informed decisions
3. **Consider the full stack** - How does this affect frontend, backend, and deployment?
4. **Reference the plan** - Ensure alignment with [Plan_Draft_6:11.md](Plan_Draft_6:11.md)

### File References
When referencing code locations, use clickable markdown links:
- Files: `[Board.js](frontend/src/components/Board.js)`
- Specific lines: `[Board.js:42](frontend/src/components/Board.js#L42)`
- Line ranges: `[Board.js:42-51](frontend/src/components/Board.js#L42-L51)`

---

## Current Project Structure

```
Tic_Tac_Toe_Infinite/
├── backend/           # FastAPI backend
├── frontend/          # React frontend
│   └── src/
│       └── components/  # React components (Board.js, Board.css, etc.)
├── requirements.txt   # Python dependencies
├── Plan_Draft_6:11.md # Project roadmap and architecture
└── .claude/           # This instructions file
```

---

## Development Roadmap Reference

1. ✅ Develop and test game logic with vanishing mechanic
2. ✅ Create FastAPI endpoints
3. 🔄 Build React frontend with local backend connection
4. ⏳ Train and validate RL model
5. ⏳ Integrate RL model with backend
6. ⏳ Deploy to AWS (S3/CloudFront + EC2)
7. ⏳ End-to-end testing
8. ⏳ Optimize and scale

(Update this checklist as project progresses)

---

## Key Reminders

- **Game name**: "Vanishing Tic Tac Toe" (or "Infinite Tic Tac Toe")
- **Critical mechanic**: 3-piece maximum per player, oldest vanishes after turn 3
- **Always reference**: [Plan_Draft_6:11.md](Plan_Draft_6:11.md) for architecture decisions
- **Comment philosophy**: Help future-you and non-experts understand the code
- **Approach**: Understand user's goal, suggest alternatives, keep it simple
