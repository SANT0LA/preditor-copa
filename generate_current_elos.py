import pandas as pd

df = pd.read_csv("data/match_elos.csv")

home = df[["date", "home_team", "elo_home"]].rename(
    columns={"home_team": "team", "elo_home": "elo"}
)

away = df[["date", "away_team", "elo_away"]].rename(
    columns={"away_team": "team", "elo_away": "elo"}
)

elos = pd.concat([home, away])
elos["date"] = pd.to_datetime(elos["date"])

current_elos = (
    elos.sort_values("date")
    .groupby("team")
    .tail(1)
    .sort_values("team")
)

current_elos.to_csv("data/current_elos.csv", index=False)

print(current_elos.head())
print("Arquivo data/current_elos.csv criado.")