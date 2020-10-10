# Import the libraries
from nsepy import get_history
from datetime import date
import pandas as pd
import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Add a title and an image
st.write("""
# Stock Market Web Application
**Visually** show data of a stock designed by Arunava Datta
""")

# Set the Background black
st.markdown("""
<style>
body {
    background-color: #46484a;
    color: white;
}
</style>
    """, unsafe_allow_html=True)

# Create a sidebar header
st.markdown(
    """
<style>
.sidebar .sidebar-content {
    background-image: linear-gradient(#315168,#315168);
    color: white;
}
</style>
""",
    unsafe_allow_html=True,
)

# Create a function to get use inputs
st.sidebar.header('User Input')
stock_symbol = st.sidebar.text_input('NSE Stock Symbol:', "")
start_date = st.sidebar.date_input('Start date (YYYY/MM/DD)')
end_date = st.sidebar.date_input('End date (YYYY/MM/DD)')

# Load data
df = get_history(symbol=stock_symbol, start=start_date, end=end_date)

# Disply the Close Price 
st.header ("Close Price History Chart of " + stock_symbol)
st.set_option('deprecation.showPyplotGlobalUse', False)
plt.figure(figsize = (16,6))
plt.title('Close Price History Chart of ' + stock_symbol)
plt.plot(df['Close'], label='Close')
plt.xticks(rotation=45) 
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.grid(True)
st.pyplot()

# Calculate the MACD and Signal Line indicators
# Calculate the short term exponential moving average (EMA)
ShortEMA = df.Close.ewm(span=12, adjust=False).mean()
#Calculate the long term exponential moving average (EMA)
LongEMA = df.Close.ewm(span=26, adjust=False).mean()
# Calculate the MACD line 
MACD = ShortEMA- LongEMA
#Calculate the Signal line
Signal = MACD.ewm(span=9, adjust=False).mean()

# Plot the MACD & Signal chart
st.header ("MACD & Signal Chart of " + stock_symbol)
plt.figure(figsize=(16,6))
plt.title('MACD & Signal Chart of ' + stock_symbol)
plt.grid(True)
plt.plot(df.index, MACD, label=' MACD Line', color= 'blue')
plt.plot(df.index, Signal, label='Signal Line', color= 'red')
plt.xticks(rotation=45)
plt.legend(loc='upper left')
st.pyplot()

# Create the simple moving average with a 30 day window
SMA30 = pd.DataFrame()
SMA30['Close'] = df['Close'].rolling(window=30).mean()

# Create the simple moving average with a 100 day window
SMA100 = pd.DataFrame()
SMA100['Close'] = df['Close'].rolling(window=100).mean()

# Visually show the dual moving averages
st.header ("Close Price, SMA 30 & SMA 100 Chart of " + stock_symbol)
plt.figure(figsize=(20,8))
plt.title('Close Price, SMA 30 & SMA 100 Chart of' + stock_symbol)
plt.grid(True)
plt.plot(df['Close'], label='Close')
plt.plot(SMA30['Close'], label='SMA30')
plt.plot(SMA100['Close'], label='SMA100')
plt.xticks(rotation=45)
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend(loc='upper right')
st.pyplot()

# Calculate the three moving averages
# Calculate the short / fast exponential moving average
ShortEMA = df.Close.ewm(span=5, adjust= False).mean()
# Calculate the middle / medium exponential moving average
MiddleEMA = df.Close.ewm(span=21, adjust= False).mean()
# Calculate the long / slow exponential moving average
LongEMA = df.Close.ewm(span=63, adjust= False).mean()

# Visualize the closing price and the exponential moving averages
st.header ("Close Price, Three Exponential Moving Average of " + stock_symbol)
plt.figure(figsize=(16,6))
plt.grid(True)
plt.plot(df['Close'], label='Close Price', color ='blue')
plt.plot(ShortEMA, label='ShortEMA', color = 'red')
plt.plot(MiddleEMA, label='MiddleEMA', color= 'orange')
plt.plot(LongEMA, label='LongEMA', color= 'green')
plt.xticks(rotation=45)
plt.title('Close Price, Three Exponential Moving Average of ' + stock_symbol)
plt.xlabel('Date')
plt.ylabel('Price')
plt.legend(loc='upper right')
st.pyplot()

# Prepare the date to Calculate RSI
# Get the difference in price from the previous day
delta = df['Close'].diff(1)

# Get rid of Nan
delta = delta.dropna()

# Get the positive gains (UP) and the negative gains (Down)
up = delta.copy()
down = delta.copy()

up[up<0] = 0
down[down>0] = 0

# Get the time period
period = 14
# Average gain and average loss
Avg_Gain = up.rolling(window=period).mean()
Avg_Loss = abs(down.rolling(window=period).mean())

# Calculate the RSI

# Calculate the Realtive Strength (RS)
RS = Avg_Gain / Avg_Loss
# Calculate the Realtive Strength Index (RSI)
RSI = 100.0 - (100.0 / (1.0 + RS))

# Put all together
# Create a new data frame
new_df = pd.DataFrame()
new_df['Close'] = df['Close']
new_df['RSI'] = RSI

# Visually show the Close Price and RSI

# Plot the Close Price
st.header ("RSI Plot of " + stock_symbol)
plt.figure(figsize=(20,8))
plt.title('RSI Plot of '+ stock_symbol)
plt.plot(new_df.index, new_df['RSI'])
plt.grid(True)
plt.xticks(rotation=45)
plt.axhline(0, linestyle='--', alpha= 0.5, color = 'grey')
plt.axhline(10, linestyle='--', alpha= 0.5, color = 'orange')
plt.axhline(20, linestyle='--', alpha= 0.5, color = 'green')
plt.axhline(30, linestyle='--', alpha= 0.5, color = 'red')
plt.axhline(70, linestyle='--', alpha= 0.5, color = 'red')
plt.axhline(80, linestyle='--', alpha= 0.5, color = 'green')
plt.axhline(90, linestyle='--', alpha= 0.5, color = 'orange')
plt.axhline(100, linestyle='--', alpha= 0.5, color = 'grey')
st.pyplot()

# Prepare the date to Calculate MFI
# Calculate the typical price
typical_price = (df['Close'] + df['High'] + df['Low'])

# Calculate the money flow
money_flow = typical_price * df['Volume']

# Get all of the positive and negative money flows
positive_flow = []
negative_flow = []

# Loop through the typical price
for i in range(1, len(typical_price)):
    if typical_price[i] > typical_price[i-1]:
        positive_flow.append(money_flow[i-1])
        negative_flow.append(0)
    elif typical_price[i] < typical_price[i-1]:
        negative_flow.append(money_flow[i-1])
        positive_flow.append(0)
    else:
        positive_flow.append(0)
        negative_flow.append(0)

# Get all the postive and negative money flows within the time period
positive_mf = []
negative_mf = []

for i in range(period-1, len(positive_flow)):
    positive_mf.append(sum(positive_flow[i+1-period : i+1]))
for i in range(period-1, len(negative_flow)):
    negative_mf.append(sum(negative_flow[i+1-period : i+1]))

# Calculate the money flow index
mfi = 100 * (np.array(positive_mf) / (np.array(positive_mf) + np.array(negative_mf)))

# Visually show the money flow index
df2 = pd.DataFrame()
df2 = df[period:]
df2['MFI'] = mfi

# Create the plot
st.header ("MFI Plot of " + stock_symbol)
plt.figure(figsize=(20,8))
plt.title('MFI Plot of ' + stock_symbol)
plt.plot(df2['MFI'], label = 'MFI')
plt.grid(True)
plt.xlabel('Date')
plt.ylabel('MFI Values')
plt.xticks(rotation=45)
plt.axhline(10, linestyle='--', color = 'orange')
plt.axhline(20, linestyle='--', color = 'blue')
plt.axhline(80, linestyle='--', color = 'blue')
plt.axhline(90, linestyle='--', color = 'orange')
st.pyplot()

# Define each and everything to perform the operation
def PPSR(df):  
    PP = pd.Series((df['High'] + df['Low'] + df['Close']) / 3).round(decimals=2)
    R1 = pd.Series(2 * PP - df['Low']).round(decimals=2)    
    S1 = pd.Series(2 * PP - df['High']).round(decimals=2)    
    R2 = pd.Series(PP + df['High'] - df['Low']).round(decimals=2)    
    S2 = pd.Series(PP - df['High'] + df['Low']).round(decimals=2)    
    R3 = pd.Series(df['High'] + 2 * (PP - df['Low'])).round(decimals=2)    
    S3 = pd.Series(df['Low'] - 2 * (df['High'] - PP)).round(decimals=2)    
    psr = {'R1':R1, 'R2':R2, 'R3':R3, 'PP':PP, 'S1':S1, 'S2':S2, 'S3':S3} 
    PSR = pd.DataFrame(psr)
    df= df.join(PSR)  
    return df

# Compute and print the data
PD=PPSR(df)
df2 = PD.drop(columns = ['Symbol','Series','Prev Close', 'Open','High','Low','VWAP','Last','Volume','Turnover','Trades','Deliverable Volume','%Deliverble'])
df2['Close'] = df2['Close'].map('{0:g}'.format)
df2['R1'] = df2['R1'].map('{0:g}'.format)
df2['R2'] = df2['R2'].map('{0:g}'.format)
df2['R3'] = df2['R3'].map('{0:g}'.format)
df2['PP'] = df2['PP'].map('{0:g}'.format)
df2['S1'] = df2['S1'].map('{0:g}'.format)
df2['S2'] = df2['S2'].map('{0:g}'.format)
df2['S3'] = df2['S3'].map('{0:g}'.format)
# Display the Pivot Chart
st.header ("Pivot Chart of " + stock_symbol)
st.write(df2.tail(10))
