import pandas as pd
df = pd.read_csv('data/ca_fires.csv')

df['plot_date'] = df['plot_date'].astype('datetime64[ns]')

df['plot_date'] = df['plot_date'].dt.date

print(df.plot_date)


