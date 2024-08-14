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

#table with usefull information, avg annual rate, std deviation.. check porfolio analyser

def stock_data():
    csv_loc = f'./data/{stock}.csv'
    df = pd.read_csv(csv_loc, sep=',', header=0)
    return df.set_index("Date")

csv_loc = './data/QQQ.csv'
chart_data = pd.read_csv(csv_loc, sep=',')

st.line_chart(chart_data, x="Date", y="Close")

