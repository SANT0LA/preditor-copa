# ⚽ Preditor de Partidas da Copa do Mundo

Projeto de Machine Learning para previsão de resultados de partidas de futebol (vitória, empate ou derrota), utilizando dados históricos e métricas avançadas como Elo Rating e forma recente das seleções.

---

## 🚀 Demonstração

Acesse o app:
👉 [Acessar o app](https://preditor-copa.streamlit.app/)

---

## 🧠 Como funciona

O modelo prevê o resultado com base em:

- 📊 **Elo Rating** (força das seleções)
- 📈 **Forma recente** (últimos 5 jogos)
- 🏟️ **Campo neutro ou não**

### Variáveis utilizadas:

- `elo_home`
- `elo_away`
- `elo_diff`
- `home_recent_points`
- `away_recent_points`
- `home_recent_goal_diff`
- `away_recent_goal_diff`
- `neutral`

---

## 🏗️ Tecnologias utilizadas

- Python
- Pandas
- Scikit-learn
- Streamlit

---

## 📂 Estrutura do projeto
preditor-copa/
│
├── app.py
├── train_model.py
├── generate_elo.py
├── generate_features.py
├── generate_current_elos.py
├── requirements.txt
│
├── data/
│ ├── results.csv
│ ├── match_elos.csv
│ ├── model_dataset.csv
│ └── current_elos.csv
│
├── models/
│ ├── model.pkl
│ └── features.pkl

---

## ⚙️ Como rodar localmente

```bash
git clone https://github.com/seu-usuario/preditor-copa.git
cd preditor-copa

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

streamlit run app.py

```
---

## 📊 Modelo

 modelo utilizado é:

- RandomForestClassifier

Treinado com:

- Dados históricos de partidas internacionais
- Elo dinâmico calculado por jogo
- Estatísticas de desempenho recente

---

## 🔥 Próximas melhorias
- Simulação completa de torneios
- Previsão de placar
- Integração com API de dados ao vivo
- Deploy com banco de dados

---

## 👤 Autor
João Victor Santos


---
