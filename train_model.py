import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib
import os

print("Carregando dataset final...")

df = pd.read_csv("data/model_dataset.csv")

features = [
    "neutral",
    "elo_home",
    "elo_away",
    "elo_diff",
    "home_recent_points",
    "away_recent_points",
    "home_recent_goal_diff",
    "away_recent_goal_diff"
]

X = df[features]
y = df["resultado"]

print("Dividindo treino/teste...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

print("Treinando modelo...")

model = RandomForestClassifier(
    n_estimators=150,
    max_depth=12,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

print("Avaliando modelo...")

pred = model.predict(X_test)

print(classification_report(y_test, pred))

print("Salvando modelo...")

os.makedirs("models", exist_ok=True)

joblib.dump(model, "models/model.pkl")
joblib.dump(features, "models/features.pkl")

print("Modelo atualizado com Elo + forma recente.")