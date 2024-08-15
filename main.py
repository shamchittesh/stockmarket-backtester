import pandas as pd
import altair as alt
import os, re
import numpy as np
import streamlit as st
from datetime import date
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

def get_date(stock):
    csv_loc = f'./data/{stock}.csv'
    df = pd.read_csv(csv_loc, sep=',', header=0)
    df['Date'] = pd.to_datetime(df['Date'])
    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()
    return min_date, max_date

min_date, max_date = get_date(stock)
#select data range to display on chart/ perform operations with selected range.. default always 0% 100%
date_range = st.slider(
    "Select date range: ",
    value=(
            date(min_date.year, min_date.month, min_date.day), 
            date(max_date.year, max_date.month, max_date.day)
           ),
    format="YYYY/MM/DD",
)
st.write("Date Range:",  (', '.join(str(dt) for dt in date_range)))
st.write("Date Range:",  (date_range[0]))
st.write("Date Range:",  (date_range[1]))

#table with usefull information, avg annual rate, std deviation.. check porfolio analyser

def stock_data():
    csv_loc = f'./data/{stock}.csv'
    df = pd.read_csv(csv_loc, sep=',', header=0)
    return df.set_index("Date")

csv_loc = './data/QQQ.csv'

# Specify the date range
start_date = f'{date_range[0]}'
end_date = f'{date_range[1]}'

# Function to filter rows based on date range
def filter_date_range(df, start_date, end_date):
    return df[(df.index >= start_date) & (df.index <= end_date)]

# Read the CSV file and parse dates
df = pd.read_csv(
    csv_loc,
    sep=',',
    parse_dates=['Date'],  # Replace 'Date' with the name of your date column
    header=0,
    skiprows=0
)
print(df)
df_filtered = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)]
print(df_filtered)
st.line_chart(df_filtered, x="Date", y="Close")

