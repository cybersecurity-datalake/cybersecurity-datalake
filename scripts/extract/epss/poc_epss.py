import pandas as pd

arquivo = "../../../datalake/raw/epss/samples/epss_sample.csv"
df = pd.read_csv(
    arquivo,
    comment="#"
)

print("Colunas encontradas:")
print(df.columns.tolist())

print(f"Total de registros: {len(df)}")

print("\nPrimeiras linhas:")
print(df.head())

top = df.sort_values(
    by="epss",
    ascending=False
)

print("\nTop EPSS:")
print(top[["cve", "epss"]].head(10))