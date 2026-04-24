import pandas as pd
from collections import defaultdict

df = pd.read_csv("data/results.csv")
df["date"] = pd.to_datetime(df["date"])
df = df.sort_values("date")

ratings = defaultdict(lambda: 1500)

rows = []

K = 30
HOME_ADVANTAGE = 50

def expected_score(rating_a, rating_b):
    return 1 / (1 + 10 ** ((rating_b - rating_a) / 400))

for _, row in df.iterrows():
    home = row["home_team"]
    away = row["away_team"]

    home_rating = ratings[home]
    away_rating = ratings[away]

    if row["neutral"]:
        home_adj = home_rating
    else:
        home_adj = home_rating + HOME_ADVANTAGE

    expected_home = expected_score(home_adj, away_rating)

    if row["home_score"] > row["away_score"]:
        actual_home = 1
    elif row["home_score"] < row["away_score"]:
        actual_home = 0
    else:
        actual_home = 0.5

    rows.append({
        "date": row["date"],
        "home_team": home,
        "away_team": away,
        "elo_home": home_rating,
        "elo_away": away_rating,
        "elo_diff": home_rating - away_rating
    })

    ratings[home] = home_rating + K * (actual_home - expected_home)
    ratings[away] = away_rating + K * ((1 - actual_home) - (1 - expected_home))

elo_df = pd.DataFrame(rows)
elo_df.to_csv("data/match_elos.csv", index=False)

print("Arquivo data/match_elos.csv criado com sucesso.")
print(elo_df.head())



