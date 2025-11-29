import pandas as pd

df = pd.read_csv('population.csv')
print("Unique Gender:", df['성별'].unique())
print("Unique Age:", df['연령별'].unique())
print("Unique Year:", df['시점'].unique())
print("Unique Region:", df['행정구역별(시군구)'].unique())
