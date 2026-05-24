import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="AFRIMACRO Intelligence", layout="wide")
st.title("AFRIMACRO Intelligence — Financial Dashboard")

DATA_PATH = Path(__file__).parent / "data" / "sample_data.csv"

@st.cache_data
def load_data():
    if DATA_PATH.exists():
        df = pd.read_csv(DATA_PATH, parse_dates=["Date"])
        return df
    # fallback: try to fetch sample tickers if yfinance is available
    try:
        import yfinance as yf
        tickers = ["AAPL", "MSFT", "^GSPC"]
        df = yf.download(tickers, period="1y")["Adj Close"].reset_index()
        df = df.melt(id_vars="Date", var_name="Ticker", value_name="Adj Close")
        return df
    except Exception:
        # generate synthetic sample data
        dates = pd.date_range(end=pd.Timestamp.today(), periods=12, freq='M')
        df = pd.DataFrame({
            "Date": dates,
            "Close": (100 + (pd.np.random.rand(len(dates)) * 10).cumsum()).round(2)
        })
        return df

df = load_data()

if "Ticker" in df.columns:
    tickers = df["Ticker"].unique().tolist()
    sel = st.multiselect("Tickers", tickers, default=tickers[:2])
    filt = df[df["Ticker"].isin(sel)]
    import plotly.express as px
    fig = px.line(filt, x="Date", y="Adj Close", color="Ticker", title="Adjusted Close")
    st.plotly_chart(fig, use_container_width=True)
else:
    import plotly.express as px
    fig = px.line(df, x="Date", y="Close", title="Sample Close")
    st.plotly_chart(fig, use_container_width=True)

st.sidebar.header("Data Preview")
st.sidebar.write(df.head())
