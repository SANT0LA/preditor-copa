import streamlit as st
import pandas as pd
import joblib

model = joblib.load("models/model.pkl")
features = joblib.load("models/features.pkl")

elos = pd.read_csv("data/current_elos.csv")
dataset = pd.read_csv("data/model_dataset.csv")

st.set_page_config(page_title="Preditor da Copa", page_icon="⚽")

st.title("⚽ Preditor de Partidas da Copa do Mundo")

st.write("Escolha duas seleções e veja a previsão com base em Elo e forma recente.")

selecoes = sorted(elos["team"].unique())

col_home, col_away = st.columns(2)

with col_home:
    home_team = st.selectbox("Seleção mandante", selecoes, key="home_team")

with col_away:
    away_team = st.selectbox("Seleção visitante", selecoes, key="away_team")

st.caption("Para inverter as seleções, troque manualmente os campos acima.")

neutral = st.checkbox("Campo neutro?", value=True)

def get_current_elo(team):
    return float(elos.loc[elos["team"] == team, "elo"].iloc[0])

def get_recent_form(team):
    jogos = dataset[
        (dataset["home_team"] == team) | 
        (dataset["away_team"] == team)
    ].tail(5)

    pontos = 0
    saldo = 0

    for _, jogo in jogos.iterrows():
        resultado = jogo["resultado"]

        if jogo["home_team"] == team:
            if resultado == "Vitória mandante":
                pontos += 3
                saldo += 1
            elif resultado == "Empate":
                pontos += 1
                saldo += 0
            else:
                saldo -= 1

        else:
            if resultado == "Vitória visitante":
                pontos += 3
                saldo += 1
            elif resultado == "Empate":
                pontos += 1
                saldo += 0
            else:
                saldo -= 1

    return pontos, saldo

elo_home = get_current_elo(home_team)
elo_away = get_current_elo(away_team)

home_recent_points, home_recent_goal_diff = get_recent_form(home_team)
away_recent_points, away_recent_goal_diff = get_recent_form(away_team)

col1, col2 = st.columns(2)

with col1:
    st.subheader(home_team)
    st.metric("Elo", f"{elo_home:.0f}")
    st.metric("Forma recente", f"{home_recent_points} pts")
    st.metric("Saldo recente", home_recent_goal_diff)

with col2:
    st.subheader(away_team)
    st.metric("Elo", f"{elo_away:.0f}")
    st.metric("Forma recente", f"{away_recent_points} pts")
    st.metric("Saldo recente", away_recent_goal_diff)

st.divider()

if elo_home > elo_away:
    favorito = home_team
    diferenca_elo = elo_home - elo_away
elif elo_away > elo_home:
    favorito = away_team
    diferenca_elo = elo_away - elo_home
else:
    favorito = "Equilíbrio total"
    diferenca_elo = 0

if diferenca_elo == 0:
    st.info("Jogo equilibrado pelo Elo.")
else:
    st.info(f"Favorito pelo Elo: {favorito} (+{diferenca_elo:.0f} pontos de Elo)")

if home_team == away_team:
    st.warning("Escolha seleções diferentes.")
else:
    input_data = pd.DataFrame([{
        "neutral": neutral,
        "elo_home": elo_home,
        "elo_away": elo_away,
        "elo_diff": elo_home - elo_away,
        "home_recent_points": home_recent_points,
        "away_recent_points": away_recent_points,
        "home_recent_goal_diff": home_recent_goal_diff,
        "away_recent_goal_diff": away_recent_goal_diff
    }])

    input_data = input_data[features]

    if st.button("Prever resultado"):
        prediction = model.predict(input_data)[0]
        probabilities = model.predict_proba(input_data)[0]

        st.subheader(f"Resultado previsto: {prediction}")

        prob_df = pd.DataFrame({
            "Resultado": model.classes_,
            "Probabilidade": probabilities
        })

        prob_df["Probabilidade (%)"] = prob_df["Probabilidade"] * 100

        st.bar_chart(
            prob_df.set_index("Resultado")["Probabilidade (%)"]
        )

        prob_df["Probabilidade"] = prob_df["Probabilidade"].apply(
            lambda x: f"{x:.2%}"
        )

        st.table(prob_df[["Resultado", "Probabilidade"]])