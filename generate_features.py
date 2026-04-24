import pandas as pd
from collections import defaultdict, deque

print("Carregando dados...")

df = pd.read_csv("data/results.csv")
elo = pd.read_csv("data/match_elos.csv")

df["date"] = pd.to_datetime(df["date"])
elo["date"] = pd.to_datetime(elo["date"])

df = pd.merge(
    df,
    elo[["date", "home_team", "away_team", "elo_home", "elo_away", "elo_diff"]],
    on=["date", "home_team", "away_team"],
    how="inner"
)

df = df.sort_values("date")

historico = defaultdict(lambda: deque(maxlen=5))

rows = []

def resultado_partida(home_score, away_score):
    if home_score > away_score:
        return "Vitória mandante"
    elif home_score < away_score:
        return "Vitória visitante"
    else:
        return "Empate"

def calcular_forma(time):
    jogos = historico[time]

    if len(jogos) == 0:
        return 0, 0

    pontos = sum(jogo["pontos"] for jogo in jogos)
    saldo = sum(jogo["saldo"] for jogo in jogos)

    return pontos, saldo

print("Gerando features...")

for _, row in df.iterrows():
    home = row["home_team"]
    away = row["away_team"]

    home_recent_points, home_recent_goal_diff = calcular_forma(home)
    away_recent_points, away_recent_goal_diff = calcular_forma(away)

    resultado = resultado_partida(row["home_score"], row["away_score"])

    rows.append({
        "date": row["date"],
        "home_team": home,
        "away_team": away,
        "neutral": row["neutral"],
        "elo_home": row["elo_home"],
        "elo_away": row["elo_away"],
        "elo_diff": row["elo_diff"],
        "home_recent_points": home_recent_points,
        "away_recent_points": away_recent_points,
        "home_recent_goal_diff": home_recent_goal_diff,
        "away_recent_goal_diff": away_recent_goal_diff,
        "resultado": resultado
    })

    home_goals = row["home_score"]
    away_goals = row["away_score"]

    if home_goals > away_goals:
        home_points = 3
        away_points = 0
    elif home_goals < away_goals:
        home_points = 0
        away_points = 3
    else:
        home_points = 1
        away_points = 1

    historico[home].append({
        "pontos": home_points,
        "saldo": home_goals - away_goals
    })

    historico[away].append({
        "pontos": away_points,
        "saldo": away_goals - home_goals
    })

dataset = pd.DataFrame(rows)

dataset.to_csv("data/model_dataset.csv", index=False)

print("Dataset final criado em data/model_dataset.csv")
print(dataset.head())
print(dataset.shape)