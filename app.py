import uuid

from flask import Flask, jsonify, render_template, request

from game import ROSTER, Battle, Pokemon, random_cpu_pick, roster_info

app = Flask(__name__)
GAMES = {}  # game_id -> Battle (lives in memory while the server runs)


def bad(msg, code=400):
    return jsonify({"error": msg}), code


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/roster")
def roster():
    return jsonify(roster_info())


@app.post("/api/start")
def start():
    data = request.get_json(silent=True) or {}
    mode = data.get("mode")
    picks = data.get("picks", [])
    names = data.get("names", [])

    if mode not in ("cpu", "pvp"):
        return bad("Mode must be 'cpu' or 'pvp'.")
    needed = 1 if mode == "cpu" else 2
    if len(picks) != needed or not all(
        isinstance(p, int) and 0 <= p < len(ROSTER) for p in picks
    ):
        return bad("Pick a valid Pokémon for each player.")

    clean = [
        (str(n).strip()[:14] or f"Player {i + 1}") for i, n in enumerate(names[:2])
    ]
    while len(clean) < 2:
        clean.append(f"Player {len(clean) + 1}")

    p1 = Pokemon(*ROSTER[picks[0]])
    if mode == "cpu":
        p2 = Pokemon(*ROSTER[random_cpu_pick(p1.name)])
        players = [(clean[0], p1, False), ("Computer", p2, True)]
    else:
        p2 = Pokemon(*ROSTER[picks[1]])
        players = [(clean[0], p1, False), (clean[1], p2, False)]

    game_id = uuid.uuid4().hex
    GAMES[game_id] = Battle(players)
    return jsonify({"game_id": game_id, "state": GAMES[game_id].to_dict()})


@app.post("/api/move")
def move():
    data = request.get_json(silent=True) or {}
    battle = GAMES.get(data.get("game_id"))
    if battle is None:
        return bad("Game not found. Start a new battle.", 404)
    try:
        events = battle.play(int(data.get("move", -1)))
    except (ValueError, TypeError) as e:
        return bad(str(e))
    return jsonify({"events": events, "state": battle.to_dict()})


if __name__ == "__main__":
    app.run(debug=True)
