import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import feedparser
import yfinance as yf
import requests
from datetime import datetime
import re

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="Pro Market Intelligence 2025",
    page_icon="📈",
    layout="wide"
)

# Robust CSS for better scannability
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { 
        background-color: #1c2128; 
        padding: 20px; 
        border-radius: 12px; 
        border: 1px solid #30363d;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .news-card {
        padding: 15px;
        border-bottom: 1px solid #30363d;
    }
    img { border-radius: 10px; object-fit: cover; }
    </style>
    """, unsafe_allow_html=True)

# =================================================
# ADVANCED NEWS ENGINE
# =================================================
def get_browser_session():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    return session

def extract_image(entry):
    if hasattr(entry, 'media_content'): return entry.media_content[0]['url']
    if hasattr(entry, 'media_thumbnail'): return entry.media_thumbnail[0]['url']
    if hasattr(entry, 'enclosures') and entry.enclosures: return entry.enclosures[0]['url']
    desc = entry.get('summary', '') or entry.get('description', '')
    img_match = re.search(r'<img [^>]*src="([^"]+)"', desc)
    if img_match: return img_match.group(1)
    return "https://via.placeholder.com/400x250?text=Market+News"

@st.cache_data(ttl=900)
def fetch_market_news(market_type):
    # Multiple sources to ensure Forex news is never empty
    sources = {
        "Forex": ["https://www.investing.com/rss/news_1.rss", "https://www.dailyfx.com/feeds/forex-news"],
        "Crypto": ["https://feeds.feedburner.com/CoinDesk"]
    }
    
    session = get_browser_session()
    all_entries = []
    
    for url in sources.get(market_type, []):
        try:
            response = session.get(url, timeout=10)
            feed = feedparser.parse(response.content)
            all_entries.extend(feed.entries)
        except: continue
        
    return all_entries[:12]

# =================================================
# DATA & INDICATORS
# =================================================
def calculate_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

@st.cache_data(ttl=300)
def get_market_data(symbol, period):
    try:
        df = yf.download(symbol, period=period, interval="1d", progress=False)
        if df.empty: return None
        if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.get_level_values(0)
        
        df['SMA20'] = df['Close'].rolling(window=20).mean()
        df['SMA50'] = df['Close'].rolling(window=50).mean()
        df['RSI'] = calculate_rsi(df['Close'])
        return df.reset_index()
    except: return None

# =================================================
# UI LAYOUT
# =================================================
st.sidebar.title("💎 Terminal Settings")
market_choice = st.sidebar.radio("Market Selection", ["Forex", "Crypto"])
tf = st.sidebar.selectbox("History Period", ["1mo", "3mo", "6mo", "1y", "2y"], index=1)

if market_choice == "Forex":
    st.title("💹 Forex Command Center")
    c1, c2 = st.sidebar.columns(2)
    base = c1.selectbox("Base", ["USD", "EUR", "GBP", "JPY", "AUD", "CAD"])
    quote = c2.selectbox("Quote", ["EUR", "USD", "GBP", "JPY", "CHF", "NZD"], index=1)
    symbol = f"{base}{quote}=X"
else:
    st.title("₿ Crypto Intelligence")
    asset = st.sidebar.selectbox("Asset", ["BTC-USD", "ETH-USD", "SOL-USD", "XRP-USD", "BNB-USD"])
    symbol = asset

# Fetch Data
data = get_market_data(symbol, tf)

if data is not None and len(data) > 0:
    # --- FIX: Safe check for metrics ---
    cur = data['Close'].iloc[-1]
    
    # Check if we have at least 2 rows to calculate 'prev' and 'diff'
    if len(data) >= 2:
        prev = data['Close'].iloc[-2]
        diff = cur - prev
        pct = (diff / prev) * 100
    else:
        prev = cur
        diff = 0
        pct = 0
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Live Price", f"{cur:,.4f}" if market_choice == "Forex" else f"${cur:,.2f}", f"{diff:.4f}")
    m2.metric("Daily Change", f"{pct:.2f}%")
    
    # Safe RSI check
    last_rsi = data['RSI'].iloc[-1] if not pd.isna(data['RSI'].iloc[-1]) else 50
    m3.metric("RSI (14)", f"{last_rsi:.1f}")
    
    # Safe SMA check
    last_sma = data['SMA20'].iloc[-1]
    sma_gap = ((cur/last_sma)-1)*100 if not pd.isna(last_sma) else 0
    m4.metric("SMA 20 Gap", f"{sma_gap:.2f}%")

    # Main Candlestick Chart
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=data['Date'], open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name='Price'))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['SMA20'], name='SMA 20', line=dict(color='#ff9900', width=1.5)))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['SMA50'], name='SMA 50', line=dict(color='#00d4ff', width=1.5)))
    fig.update_layout(template="plotly_dark", height=500, xaxis_rangeslider_visible=False, margin=dict(l=10, r=10, t=30, b=10))
    st.plotly_chart(fig, use_container_width=True)

    # Secondary Charts
    col_a, col_b = st.columns(2)
    with col_a:
        fig_rsi = px.line(data, x='Date', y='RSI', title="Relative Strength Index")
        fig_rsi.add_hline(y=70, line_dash="dash", line_color="red")
        fig_rsi.add_hline(y=30, line_dash="dash", line_color="green")
        fig_rsi.update_layout(template="plotly_dark", height=300)
        st.plotly_chart(fig_rsi, use_container_width=True)
    with col_b:
        fig_vol = px.bar(data, x='Date', y='Volume' if market_choice == "Crypto" else 'Close', title="Activity/Volume")
        fig_vol.update_layout(template="plotly_dark", height=300)
        st.plotly_chart(fig_vol, use_container_width=True)
else:
    st.error("No data available for this selection. Try a different timeframe.")

# News Section
st.header(f"📰 Latest {market_choice} Headlines")
news_entries = fetch_market_news(market_choice)

if not news_entries:
    st.info("🔄 Connecting to news servers...")
else:
    for entry in news_entries:
        with st.container():
            img_col, text_col = st.columns([1, 3])
            with img_col:
                st.image(extract_image(entry), use_container_width=True)
            with text_col:
                st.subheader(entry.get('title', 'No Title'))
                st.caption(f"📅 {entry.get('published', 'Recently')}")
                st.markdown(f"[View Full Report]({entry.link})")
            st.divider()

st.caption(f"Terminal Status: Online • Analysis: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")