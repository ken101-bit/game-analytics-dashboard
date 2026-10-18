from fastapi import FastAPI, HTTPException

app = FastAPI()

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

    return {
        "name": player["name"],
        "wins": player["wins"],
        "losses": player["losses"],
        "win_rate": win_rate
    }