from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
class PlayerCreate(BaseModel):
    name: str
    wins: int
    losses: int
    kills: int

players = {
    1: {"name": "Dragon99", "wins": 25, "losses": 10},
    2: {"name": "ShadowX", "wins": 40, "losses": 15},
    3: {"name": "Ken", "wins": 60, "losses": 20}
}

@app.get("/")
def home():
    return {"message": "Game Analytics API is running"}

@app.get("/players")
def get_players(min_wins: int = 0):
    filtered_players = {}

    for player_id, player in players.items():
        if player["wins"] >= min_wins:
            filtered_players[player_id] = player

    return filtered_players

@app.get("/players/{player_id}")
def get_player(player_id: int):

    if player_id not in players:
        raise HTTPException(
            status_code=404,
            detail="Player not found"
        )

    player = players[player_id]

    total_games = player["wins"] + player["losses"]

    if total_games == 0:
        win_rate = 0
    else:
        win_rate = round(
            player["wins"] / total_games * 100, 2
        )

    if total_games == 0:
        kills_per_game = 0
    else:
        kills_per_game = round(player.get("kills", 0) / total_games, 2)

    return {
        "name": player["name"],
        "wins": player["wins"],
        "losses": player["losses"],
        "kills": player.get("kills", 0),
        "win_rate": win_rate,
        "kills_per_game": kills_per_game
    }
    

    
@app.post("/players")
def create_player(player: PlayerCreate):
    new_id = max(players.keys(), default=0) + 1

    players[new_id] = {
        "name": player.name,
        "wins": player.wins,
        "losses": player.losses,
        "kills": player.kills
    }

    return {
        "message": "Player created successfully",
        "player_id": new_id
    }
