import pandas as pd

data = pd.read_csv("../lyrics.csv")

print(data.info())
print(data.head())

print(data.groupby("artist").size())