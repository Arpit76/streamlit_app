import streamlit as st
import yfinance as yf
import pandas as pd
import time
import schedule


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




def loadTab5():    
    st.text("Welcome to Stock Price Movement ")

def stockPriceMovement():
    st.text(nifty_50_stocks)
    latest_nifty, nifty_change, df = fetch_prices()

    ticker_parts = []

    # Add Nifty itself
    ticker_parts.append(
        f"<b>NIFTY 50:</b> {latest_nifty:.2f} {color_and_arrow(nifty_change)}"
    )

    # Add stocks
    for symbol, row in df.iterrows():
        ticker_parts.append(
            f"{symbol}: {row['Price']:.2f} {color_and_arrow(row['Change'])}"
            
        )
        print(symbol + ": " + str(row["Price"]))
    
    ticker_text = " &nbsp;&nbsp; | &nbsp;&nbsp; ".join(ticker_parts)

    ticker_html = f"""
    <style>
    .ticker-wrap {{
    width: 100%;
    overflow: hidden;
    background: #000;
    padding: 8px 0;
    }}

    .ticker_bk {{
    display: flex;
    width: max-content;
    animation: scroll 40s linear infinite;
    }}
    .ticker span {{
        white-space: nowrap;
        padding-right: 60px;
        font-size: 20px;
        color: white;
        }}
    .ticker {{
    display: inline-block;
    white-space: nowrap;
    animation: marquee 100s linear infinite;
    font-size: 20px;
    color: white;
    }}
    @keyframes marquee {{
    0%   {{ transform: translateX(100%); }}
    100% {{ transform: translateX(-100%); }}
    }}
    @keyframes scroll {{
    from    {{ transform: translateX(0); }}
    t0 {{ transform: translateX(-50%);}}
    }}
    </style>

    <div class="ticker-wrap">
    <div class="ticker">
        {ticker_text}
            
    </div>
    </div>
    """

    # -----------------------------------
    #         DISPLAY TICKER
    # -----------------------------------
    st.markdown(ticker_html, unsafe_allow_html=True)

    # -----------------------------------
    #        DISPLAY TABLE
    # -----------------------------------
    st.subheader("📊 Nifty 50 Latest Stock Prices")
    st.subheader({time.strftime('%H:%M:%S')})
    #st.dataframe(df.style.format({
    #    "Price": "{:.2f}",
    #    "Prev Close": "{:.2f}",
    #    "Change": "{:.2f}",
    #    "% Change": "{:.2f}%"
    #}))

    #print(df)

    styled_df = df.style.format({
        "Price": "{:.2f}",
        "Prev Close": "{:.2f}",
        "Change": "{:.2f}",
        "% Change": "{:.2f}%"
    })


    row_height = 35
    st.dataframe(styled_df, height=(row_height * len(df)) + 60)

    #time.sleep(30)
    #stockPriceMovement()
    #st_autorefresh(interval=3000, key="ticker_refresh")


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

def color_and_arrow(change):
    if change > 0:
        return f"<span style='color:#00ff00;'>▲ {change:.2f}</span>"
    elif change < 0:
        return f"<span style='color:#ff4444;'>▼ {change:.2f}</span>"
    else:
        return "<span style='color:gray;'>• 0.00</span>"






