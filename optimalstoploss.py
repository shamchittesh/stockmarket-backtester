from modules import *

start_date  = "1999-08-15"
end_date    = "2024-08-14"
stock       = "QQQ"
TPT         = 2 #Time of trade AKA no of days trading session active else take closing price of nth day

csv_loc = f'./data/{stock}.csv'
df = pd.read_csv(csv_loc, sep=',', header=0)
df = df.set_index("Date")

df = df[(df.index >= start_date) & (df.index <= end_date)]

# Remove 'Adj Close' and 'Volume' columns
df = df.drop(['Adj Close', 'Volume'], axis=1)
# Reset the index to make 'Date' a column (optional)
df = df.reset_index()

# Create a new DataFrame to store the results
new_df = pd.DataFrame(columns=df.columns)

print(df)
print(new_df)


for i in range(0, len(df), TPT): 
    chunk = df.iloc[i:i + TPT]

    # Ensure the chunk has rows (in case of the last incomplete group)
    if len(chunk) > 0:
        # Calculate the new row based on the chunk
        new_row = {
            'Date': chunk.iloc[0]['Date'],  # Take the date from the first row
            'Open': chunk.iloc[0]['Open'],  # Opening price from the first row
            'High': chunk['High'].max(),    # Highest 'High' in the chunk
            'Low': chunk['Low'].min(),      # Lowest 'Low' in the chunk
            'Close': chunk.iloc[-1]['Close'],  # Closing price from the last row
            'D': chunk.iloc[0]['Open'] - chunk['Low'].min(),  # find absolute loss
            'P': chunk.iloc[-1]['Close'] - chunk.iloc[0]['Open'] # Profit loss
        }
        
        # Append the new row to the new DataFrame using pd.concat
        new_df = pd.concat([new_df, pd.DataFrame([new_row])], ignore_index=True)

# Calculate statistics on column D
average_D = new_df['D'].mean()
smallest_D = new_df['D'].min()
highest_D = new_df['D'].max()

print(new_df)
print(f"\nAverage of D: {average_D}")
print(f"Smallest value of D: {smallest_D}")
print(f"Highest value of D: {highest_D}")

finding_nemo = []

for X in np.arange(2.6, 3.2, 0.01):
    # Calculate the new column 'tx' based on the value of X
    count = 0
    new_df['tx'] = new_df.apply(lambda row: row['P'] if X > row['D'] else -X, axis=1)    # Calculate the new column 'tx' based on the value of X
    # Count the number of times X < row['D']
    for _, row in new_df.iterrows():
        if X < row['D']:
            count += 1
    new_df['balance_tx'] = new_df['tx'].cumsum()
    last_balance_tx = new_df['balance_tx'].iloc[-1]
    finding_nemo.append({'X': X, 'sum_balance_tx': last_balance_tx, 'SL_hits': count})

print(new_df)
finding_nemo = pd.DataFrame(finding_nemo)

# Finding the highest value of last_balance_tx and its corresponding X
max_index = finding_nemo['sum_balance_tx'].idxmax()  # Index of the max balance_tx
max_value = finding_nemo['sum_balance_tx'].max()     # Maximum balance_tx value
corresponding_X = finding_nemo.loc[max_index, 'X']    # Corresponding X value
SL_hits = finding_nemo.loc[max_index, 'SL_hits']  # Corresponding Count X < D

# Print the result
print(f"\nHighest Sum balance_tx: {max_value:.4f} at X = {corresponding_X:.4f} with SL Hits = {SL_hits}")


print(finding_nemo)
