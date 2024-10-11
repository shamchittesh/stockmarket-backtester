from modules import *

start_date  = "1999-08-11"
end_date    = "2003-08-11"
stock       = "QQQ"
TPT         = 2

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

print(new_df)



# Columns:
# Trade number
# X stop loss
# D (absolute lowest price)
# P (Closing price)
# Balance (Culmulative P)
# Tx (if x > D, P, -x)
# Balance Tx culmulative tx

# Further upgrades: P = 2X
# Trading Time in days (start with default intra day trading to decide closing price)

# Inputs: df, starting amount=0, tpt=1, rrr(P)=closing price, 
# outputs: X, final amount, trade number, 

# Process:
# current dataframe:
# Date,Open,High,Low,Close,Adj Close,Volume

# D=Low, 

# transformed dataframe:
# Date(TPT),Open(TPT),High(TPT),D=Low(TPT),P=Close(TPT),tx,balance_tx