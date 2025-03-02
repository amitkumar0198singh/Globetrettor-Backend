# Globetrotter - Travel Guessing Game API

Globetrotter is a full-stack travel guessing game web app where players receive AI-generated destination clues and attempt to guess the correct location. The game includes a leaderboard, a challenge-a-friend feature, and a scoring system. This repository contains the backend API built using Django and Django REST Framework (DRF).

## Features

- **User Authentication**: Register and log in users without using Django’s default authentication model.
- **Destination Management**: Retrieve, create, and bulk-create travel destinations.
- **Game Logic**: Start a game session, receive clues, make guesses, and track scores.
- **Leaderboard**: Track and update users' highest scores.
- **Challenge a Friend**: Invite friends to play via a shareable link.

## API Endpoints

### Authentication
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/player/auth/registration/` | `POST` | Register a new player |
| `/player/auth/login/` | `POST` | Log in a player |
| `/player/auth/token/refresh/` | `POST` | Refresh authentication token |

### Destinations
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/destination/` | `GET` | Retrieve all destinations |
| `/destination/{id}/` | `GET` | Retrieve a specific destination |
| `/destination/create/` | `POST` | Create a new destination (Authenticated) |
| `/destination/bulk-create/` | `POST` | Bulk-create destinations (Authenticated) |

### Game
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/game/start/` | `POST` | Start a new game session |
| `/game/guess/` | `POST` | Submit a destination guess |
| `/game/score/` | `GET` | Get the current game score |
| `/game/end/` | `POST` | End the current game session |

### Leaderboard & Challenges
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/player/leaderboard/` | `GET` | Retrieve the leaderboard |
| `/player/invite-player/` | `POST` | Send a game invite to another player |

## Installation & Setup

### Prerequisites
- Python 3.12+
- Django & Django REST Framework
- Django Built-in cache

### Installation Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/amitkumar0198singh/Globetrettor-Backend.git
   cd Globetrettor-Backend
   ```

2. Create and activate a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

4. Run database migrations:
   ```sh
   python manage.py migrate
   ```

5. Start the development server:
   ```sh
   python manage.py runserver
   ```

## Game Logic Overview

1. **Game Start**: A player starts a session, and a random destination is selected.
2. **Clues & Choices**: Two clues about the destination are provided, along with multiple-choice options.
3. **Guess Submission**: The player selects a city as their guess.
4. **Scoring**: If correct, the player's score is updated; if incorrect, the game continues.
5. **Game Timeout**: Sessions last 60 seconds or reset upon page refresh.
6. **Leaderboard Update**: Scores are updated only if the new score is higher than the previous best.

## Contributing

Contributions are welcome! Feel free to submit pull requests or raise issues.

## License

This project is licensed under the MIT License.