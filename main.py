import pandas as pd
csv_loc = './data/QQQ.csv'
df = pd.read_csv(csv_loc, sep=',', header=0)

#Print all dates where closing price was between 100 and 200

# Filtering the DataFrame for 'Close' values between 40 and 50
filtered_df = df[(df['Close'] >= 41) & (df['Close'] <= 42)]

# Printing the corresponding 'Date' values
print(filtered_df['Date'].tolist())
