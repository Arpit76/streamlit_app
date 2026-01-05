import streamlit as st
import yfinance as yf
import pandas as pd
import time
import schedule

#from streamlit_autorefresh import st_autorefresh

nifty_50_stocks = [
    "ADANIENT.NS","ADANIPORTS.NS","APOLLOHOSP.NS","ASIANPAINT.NS","AXISBANK.NS",
    "BAJAJ-AUTO.NS","BAJFINANCE.NS","BAJAJFINSV.NS","BPCL.NS","BHARTIARTL.NS",
    "BRITANNIA.NS","CIPLA.NS","COALINDIA.NS","DIVISLAB.NS","DRREDDY.NS",
    "EICHERMOT.NS","GRASIM.NS","HCLTECH.NS","HDFCLIFE.NS","HDFCBANK.NS",
    "HEROMOTOCO.NS","HINDALCO.NS","HINDUNILVR.NS","ICICIBANK.NS","ITC.NS",
    "INDUSINDBK.NS","INFY.NS","JSWSTEEL.NS","KOTAKBANK.NS","LTIM.NS",
    "LT.NS","MARUTI.NS","M&M.NS","NESTLEIND.NS","NTPC.NS",
    "ONGC.NS","POWERGRID.NS","RELIANCE.NS","SBIN.NS","SHREECEM.NS",
    "SUNPHARMA.NS","TCS.NS","TATACONSUM.NS","TATAMOTORS.NS","TATASTEEL.NS",
    "TECHM.NS","TITAN.NS","ULTRACEMCO.NS","UPL.NS","WIPRO.NS"
]



if "last_update" not in st.session_state:
    st.session_state.last_update = 0

ticker_placeholder = st.empty()
table_placeholder = st.empty()

def loadTab5():    
    
    st.text("Welcome to Stock Price Movement ")
    
    ticker_placeholder = st.empty()
    table_placeholder = st.empty()
    
    maybe_update(ticker_placeholder, table_placeholder)

 




def stockPriceMovement(ticker_placeholder, table_placeholder):

    latest_nifty, nifty_change, df = fetch_prices()

    ticker_parts = [
        f"<b>NIFTY 50:</b> {latest_nifty:.2f} {color_and_arrow(nifty_change)}"
    ]

    for symbol, row in df.iterrows():
        ticker_parts.append(
            f"{symbol}: {row['Price']:.2f} {color_and_arrow(row['Change'])}"
        )

    ticker_text = " &nbsp;&nbsp; | &nbsp;&nbsp; ".join(ticker_parts)

    ticker_html = f"""
    <style>
    .ticker-wrap {{
        width: 100%;
        overflow: hidden;
        background: #000;
        padding: 8px 0;
    }}

    .ticker {{
        white-space: nowrap;
        animation: marquee 60s linear infinite;
        font-size: 20px;
        color: white;
    }}

    @keyframes marquee {{
        0% {{ transform: translateX(100%); }}
        100% {{ transform: translateX(-100%); }}
    }}
    </style>

    <div class="ticker-wrap">
        <div class="ticker">{ticker_text}</div>
    </div>
    """

    ticker_placeholder.markdown(ticker_html, unsafe_allow_html=True)

    styled_df = df.style.format({
        "Price": "{:.2f}",
        "Prev Close": "{:.2f}",
        "Change": "{:.2f}",
        "% Change": "{:.2f}%"
    })

    table_placeholder.dataframe(styled_df, width='stretch')

def fetch_prices():
    # Nifty Index
    nifty = yf.Ticker("^NSEI").history(period="2d")
    latest_nifty = nifty["Close"][-1]
    prev_nifty = nifty["Close"][-2]
    nifty_change = latest_nifty - prev_nifty

    # Nifty 50 stocks
    data = yf.download(nifty_50_stocks, period="2d")
    latest = data["Close"].iloc[-1]
    prev = data["Close"].iloc[-2]

    df = pd.DataFrame({
        "Price": latest,
        "Prev Close": prev,
        "Change": latest - prev,
        "% Change": ((latest - prev) / prev) * 100
    })

    return latest_nifty, nifty_change, df



def maybe_update(ticker_placeholder, table_placeholder):
    now = time.time()
  
    if now - st.session_state.last_update >= 30:
        stockPriceMovement(ticker_placeholder, table_placeholder)
        st.session_state.last_update = now

    time.sleep(40)
    maybe_update(ticker_placeholder, table_placeholder)

def color_and_arrow(change):
    if change > 0:
        return f"<span style='color:#00ff00;'>▲ {change:.2f}</span>"
    elif change < 0:
        return f"<span style='color:#ff4444;'>▼ {change:.2f}</span>"
    else:
        return "<span style='color:gray;'>• 0.00</span>"






