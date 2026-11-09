from multiprocessing import connection
import sqlite3
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

@app.put("/players/{player_id}")
def update_player(player_id: int, player: PlayerCreate):

    if player_id not in players:
        raise HTTPException(
            status_code=404,
            detail="Player not found"
        )

    players[player_id] = {
        "name": player.name,
        "wins": player.wins,
        "losses": player.losses,
        "kills": player.kills
    }

    return {"message": "Player updated successfully"} 

@app.delete("/players/{player_id}")
def delete_player(player_id: int):

    if player_id not in players:
        raise HTTPException(
            status_code=404,
            detail="Player not found"
        )

    del players[player_id]

    return {"message": "Player deleted successfully"}

@app.get("/database/players/{player_id}")
def get_database_player(player_id: int):
    connection = sqlite3.connect("players.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM players WHERE id = ?",
        (player_id,)
    )

    player = cursor.fetchone()
    connection.close()

    if player is None:
        raise HTTPException(
            status_code=404,
            detail="Player not found"
        )
    total_games = player[2] + player[3]

    if total_games > 0:
        win_rate = (player[2] / total_games) * 100
        kills_per_game = player[4] / total_games

    else:
        win_rate = 0
        kills_per_game = 0

    return {
        "id": player[0],
        "name": player[1],
        "wins": player[2],
        "losses": player[3],
        "kills": player[4],
        "win_rate": win_rate,
        "kills_per_game": kills_per_game
    }

@app.post("/database/players", status_code=201)
def create_database_player(player: PlayerCreate):
    connection = sqlite3.connect("players.db")
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO players (name, wins, losses, kills) VALUES (?, ?, ?, ?)",
        (player.name, player.wins, player.losses, player.kills)
    )

    new_player_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return {
        "id": new_player_id,
        "message": "Player created successfully"
    }

@app.get("/database/players")
def get_all_database_players():
    connection = sqlite3.connect("players.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM players")
    players = cursor.fetchall()
    
    connection.close()

    player_list = []

    for player in players:
        player_list.append({
        "id": player[0],
        "name": player[1],
        "wins": player[2],
        "losses": player[3],
        "kills": player[4]
    })
    return player_list

@app.put("/database/players/{player_id}")
def update_database_player(player_id: int, player: PlayerCreate):
    connection = sqlite3.connect("players.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE players
        SET name = ?, wins = ?, losses = ?, kills = ?
        WHERE id = ?
        """,
        (
            player.name,
            player.wins,
            player.losses,
            player.kills,
            player_id
        )
    )

    rows_updated = cursor.rowcount

    if rows_updated == 0:
        connection.close()
        raise HTTPException(
            status_code=404,
            detail="Player not found"
        )

    connection.commit()
    connection.close()

    return {
        "id": player_id,
        "message": "Player updated successfully"
    }

@app.delete("/database/players/{player_id}")
def delete_database_player(player_id: int):
    connection = sqlite3.connect("players.db")
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM players WHERE id = ?",
        (player_id,)
    )

    rows_deleted = cursor.rowcount

    if rows_deleted == 0:
        connection.close()
        raise HTTPException(
            status_code=404,
            detail="Player not found"
        )

    connection.commit()
    connection.close()

    return {
        "id": player_id,
        "message": "Player deleted successfully"
    }