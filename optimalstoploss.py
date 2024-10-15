from modules import *

start_date  = "2021-10-30"
end_date    = "2022-10-30"
stock       = "QQQ"
TPT         = 1

results = pd.DataFrame(columns=['TPT (Days)', 'Optimal SL', 'SL_Hits', 'Trades #', 'PNL', '%SL Occurrence'])


while TPT <  10 :
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

    # print(df)
    # print(new_df)
    
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
    total_rows = new_df.shape[0]

    # print(new_df)
    # print(f"\nAverage of D: {average_D}")
    # print(f"Smallest value of D: {smallest_D}")
    # print(f"Highest value of D: {highest_D}")
    # print(f"Total nu of rows: {total_rows}")


    finding_nemo = []
    i = 1
    lowest_sl = 0
    highest_sl = highest_D

    while i >= 0.0001:
        # print(f"\nCurrent value of i: {i:.4f}")
        for X in np.arange(lowest_sl, highest_sl, i):
            SL_hits = 0
            # Count the number of times X < row['D']
            for _, row in new_df.iterrows():
                if X < row['D']:
                    SL_hits += 1

            # Calculate the new column 'tx' based on the value of X
            new_df['tx'] = new_df.apply(lambda row: row['P'] if X > row['D'] else -X, axis=1)    # Calculate the new column 'tx' based on the value of X
            new_df['balance_tx'] = new_df['tx'].cumsum()
            last_balance_tx = new_df['balance_tx'].iloc[-1]
            finding_nemo.append({'X': X, 'sum_balance_tx': last_balance_tx, 'SL_hits': SL_hits})

        finding_nemo = pd.DataFrame(finding_nemo)

        # Finding the highest value of last_balance_tx and its corresponding X
        max_index = finding_nemo['sum_balance_tx'].idxmax()  # Index of the max balance_tx
        max_value = finding_nemo['sum_balance_tx'].max()     # Maximum balance_tx value
        corresponding_X = finding_nemo.loc[max_index, 'X']    # Corresponding X value
        SL_hits = finding_nemo.loc[max_index, 'SL_hits']  # Corresponding Count X < D

        sl_occurrence = ( SL_hits / total_rows ) * 100
        # print(f"lowest sl: {lowest_sl:.4f} highest_sl: {highest_sl:.4f}")
        # print(f"Highest Sum balance_tx: {max_value:.4f} at X = {corresponding_X:.4f} with SL_Hits = {SL_hits} out of {total_rows} which is {sl_occurrence:.2f}% occurrence")

        lowest_sl = corresponding_X - i
        highest_sl = corresponding_X + i

        finding_nemo = []

        i /= 10
    # print(f"Time In Trade : {TPT} days")
    # print(f"Highest Sum balance_tx: {max_value:.4f} at X = {corresponding_X:.4f} with SL_Hits = {SL_hits} out of {total_rows} which is {sl_occurrence:.2f}% occurrence")
    # print(f"\nOptimal Stop Loss = {corresponding_X:.4f}")

    
    # Calculate the new row for results TPT (Days)', 'Optimal SL', 'SL_Hits', 'Trades #', 'PNL'])
    new_results_row = {
        'TPT (Days)': TPT,  
        'Optimal SL': corresponding_X,
        'Trades #': total_rows, 
        'SL_Hits': SL_hits,     
        'PNL': max_value,
        '%SL Occurrence': sl_occurrence, 
    }
    
    # Append the new row to the new DataFrame using pd.concat
    results = pd.concat([results, pd.DataFrame([new_results_row])], ignore_index=True)

    TPT += 1 

print(results)
# Assuming new_df is the DataFrame you want to store
# results.to_csv('osl.csv', index=False)
