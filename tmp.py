import pandas as pd
df = pd.read_csv('data/ca_fires.csv')

selected_range = [1995,2001]

start = selected_range[0]
end = selected_range[1]
year_list = list(range(start, end+1))

filtered_df = pd.DataFrame()
for year in year_list:
    new_df=df[df.fire_year == year]
    filtered_df = filtered_df.append(new_df)
print(list(filtered_df))
print(type(df.fire_year))