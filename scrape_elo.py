import pandas as pd

url = "https://www.eloratings.net/"

tables = pd.read_html(url)

print(f"Tabelas encontradas: {len(tables)}")

df = tables[0]

print(df.head())
print(df.columns)