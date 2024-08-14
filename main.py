import pandas as pd
import altair as alt
import os
import numpy as np
import streamlit as st
from datetime import datetime
from urllib.error import URLError

#get file names from data/
def get_filenames(directory):
    # List all files in the directory
    files = os.listdir(directory)
    
    # Filter and remove the .csv extension
    filenames = [os.path.splitext(file)[0] for file in files if file.endswith('.csv')]
    
    return filenames

directory = './data'
filenames = get_filenames(directory)

#select box with stock names from filenames
stock = st.selectbox(
    "Please select the stock for quant analysis:",
    (filenames),
)

# st.write("You selected:", stock)
stock = "QQQ"

def get_data(stock):
    csv_loc = f'./data/{stock}.csv'
    df = pd.read_csv(csv_loc, sep=',', header=0)
    df['Date'] = pd.to_datetime(df['Date'])
    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()
    return df.set_index("Date"), min_date, max_date

df, min_date, max_date = get_data(stock)

print(min_date.year, min_date.month, min_date.day)
print(max_date.year, max_date.month, max_date.day)
#select data range to display on chart/ perform operations with selected range.. default always 0% 100%
start_time = st.slider(
    "Select date range: ",
    value=(
            datetime(min_date.year, min_date.month, min_date.day), 
            datetime(max_date.year, max_date.month, max_date.day)
           ),
    format="YYYY/MM/DD",
)
st.write("Start time:", start_time)

#table with usefull information, avg annual rate, std deviation.. check porfolio analyser

