import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

# Stock dictionary
STOCKS = {
    "Alphabet (GOOGL)": "GOOGL",
    "Nvidia (NVDA)": "NVDA",
    "Microsoft (MSFT)": "MSFT",
    "Nvidia": "NVDA",
    "Bayerische Motoren Werke Aktiengesellschaft": "BMW.DE",
    "London Stock Exchange Group plc": "LSEG.L",
    "RIO Tinto": "RIO.AX",
    "Sasol": "SOL.JO",
    "Satrix 40 ETF": "STX40.JO",
    "CLP Holdings Ltd": "0002.HK",
    "GameStop Corp": "GME",
    "Alphabet Inc": "GOOG",
    "Tesla": "TSLA",
    "Amazon.com Inc": "AMZN",
    "Naspers Ltd.": "NPN.JO",
    "Bitcoin": "BTC-USD",
    "Anglo American Plc": "AGL.JO",
    "Capitec Bank": "CPI.JO",
    "Pik n Pay": "PIK.JO",
    "Shoprite Holdings Ltd": "SHP.JO",
    "Ethereum": "ETH-USD",
    "BHP Group Limited": "BHP.AX",
    "Anglo American Platinum": "AMS.JO"
}

st.title("Stock Time Series Visualization")

# User inputs
selected_stock = st.selectbox("Choose a stock:", STOCKS)
start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

if st.button("Fetch Data"):
    df = yf.download(STOCKS[selected_stock], start=start_date, end=end_date)
    dividends = yf.Ticker(STOCKS[selected_stock]).dividends
    
    if df.empty:
        st.warning("No data available for the selected period.")
    else:
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(df.index, df["Adj Close"], label="Adjusted Closing Price", color="blue")
        ax.set(title=f"{selected_stock} Stock Prices", xlabel="Date", ylabel="Price (USD)")
        ax.legend()
        ax.grid()
        st.pyplot(fig)
        
        if not dividends.empty:
            st.write("## Dividend Data")
            st.dataframe(dividends)
        else:
            st.write("No dividend data available.")

if st.button("Download Data"):
    df = yf.download(STOCKS[selected_stock], start=start_date, end=end_date)
    dividends = yf.Ticker(STOCKS[selected_stock]).dividends
    
    if df.empty:
        st.warning("No data available for the selected period.")
    else:
        df["Dividends"] = dividends.reindex(df.index, fill_value=0)
        
        # Convert dataframe to CSV for download
        csv = df.to_csv().encode('utf-8')
        st.download_button(
            label="Download Data as CSV",
            data=csv,
            file_name=f"{STOCKS[selected_stock]}_stock_data.csv",
            mime="text/csv"
        )
