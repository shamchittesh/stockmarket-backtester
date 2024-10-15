from modules import *

RRR = 2
SL = 7
start_date  = "1998-10-30"
end_date    = "2022-10-30"
stock       = "QQQ"

csv_loc = f'./data/{stock}.csv'
df = pd.read_csv(csv_loc, sep=',', header=0)
df = df.set_index("Date")

df = df[(df.index >= start_date) & (df.index <= end_date)]

# Remove 'Adj Close' and 'Volume' columns
df = df.drop(['Adj Close', 'Volume'], axis=1)
# Reset the index to make 'Date' a column (optional)
df = df.reset_index()

# Input variable X
X = SL
PT = RRR * SL

# Initialize new columns
df['SL'] = df['Open'] - X
df['PT'] = df['Open'] + PT
df['Sell Price'] = 0
df['Highest'] = df['High']
df['Lowest'] = df['Low']
df['Days in Trade'] = 0

# Initialize variables to hold previous state
prev_highest = df.at[0, 'High']
prev_lowest = df.at[0, 'Low']
prev_SL = df.at[0, 'SL']
prev_PT = df.at[0, 'PT']
days_in_trade = 0

# Initialize counters for statistics
total_trades = 0
closed_at_PT = 0
closed_at_SL = 0
trade_durations = []  # List to store trade durations

# Simulate trading conditions
for i in range(1, len(df)):
    # Carry forward the previous values unless a reset condition occurs
    df.at[i, 'SL'] = prev_SL
    df.at[i, 'PT'] = prev_PT
    df.at[i, 'Highest'] = prev_highest
    df.at[i, 'Lowest'] = prev_lowest
    
    # Increment days in trade
    days_in_trade += 1
    df.at[i, 'Days in Trade'] = days_in_trade
    
    # Check the trading conditions
    if df.at[i, 'SL'] > df.at[i, 'Lowest']:
        df.at[i, 'Sell Price'] = -X
        closed_at_SL += 1  # Closed at Stop Loss
        trade_durations.append(days_in_trade)  # Track trade duration
    elif df.at[i, 'PT'] < df.at[i, 'Highest']:
        df.at[i, 'Sell Price'] = PT
        closed_at_PT += 1  # Closed at Profit Target
        trade_durations.append(days_in_trade)  # Track trade duration
    else:
        df.at[i, 'Sell Price'] = 0
    
    # If a trade occurred (Sell Price != 0)
    if df.at[i, 'Sell Price'] != 0:
        total_trades += 1
        
        # Reset on non-zero sell price
        prev_highest = df.at[i, 'High']
        prev_lowest = df.at[i, 'Low']
        prev_SL = df.at[i, 'Open'] - X
        prev_PT = df.at[i, 'Open'] + PT
        days_in_trade = 0  # Reset the days in trade counter
    else:
        # Update highest/lowest based on current values if no reset
        prev_highest = max(prev_highest, df.at[i, 'High'])
        prev_lowest = min(prev_lowest, df.at[i, 'Low'])

# Sum of Sell Price
total_sell_price = df['Sell Price'].sum()

# Calculate trade duration statistics
min_days_in_trade = min(trade_durations) if trade_durations else 0
max_days_in_trade = max(trade_durations) if trade_durations else 0
avg_days_in_trade = sum(trade_durations) / len(trade_durations) if trade_durations else 0

# Display the results
print(f"Total Sell Price: {total_sell_price}")
print(f"Total Trades Entered: {total_trades}")
print(f"Number of Trades Closed at PT: {closed_at_PT}")
print(f"Number of Trades Closed at SL: {closed_at_SL}")
print(f"Lowest Days in Trade: {min_days_in_trade}")
print(f"Highest Days in Trade: {max_days_in_trade}")
print(f"Average Days in Trade: {avg_days_in_trade:.2f}")

# Optional: Display the updated DataFrame
print(df[['Date', 'Open', 'SL', 'PT', 'Highest', 'Lowest', 'Sell Price', 'Days in Trade']])


# df.to_csv('tradingsim.csv', index=False)
 