#!/usr/bin/env python3
import os
import yfinance as yf
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv("/Users/trevorlorenz/Desktop/IS 445/AD Hoc Project/.env")
password = os.getenv("DB_PASSWORD")
engine = create_engine(f"mysql+pymysql://root:{password}@localhost/macro_db")

TICKERS = ["SPY", "USO", "XLE", "GLD", "TLT"]

ASSET_META = [
    ("SPY", "S&P 500 ETF", "Equity"),
    ("USO", "United States Oil Fund", "Commodity"),
    ("XLE", "Energy Select Sector SPDR", "Equity-Energy"),
    ("GLD", "SPDR Gold Shares", "Commodity"),
    ("TLT", "iShares 20+ Year Treasury Bond ETF", "Fixed Income"),
]


def load_assets():
    with engine.connect() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM assets")).scalar()
    if count > 0:
        print(f"assets table already has {count} rows — skipping load")
        return
    rows = [{"ticker": t, "name": n, "category": c, "is_etf": True} for t, n, c in ASSET_META]
    df = pd.DataFrame(rows)
    df.to_sql("assets", engine, if_exists="append", index=False)
    with engine.connect() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM assets")).scalar()
    print(f"assets loaded: {count} rows")


def load_prices():
    with engine.connect() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM prices")).scalar()
    if count > 0:
        print(f"prices table already has {count} rows — skipping load")
        return

    tickers = list(dict.fromkeys(TICKERS))
    raw = yf.download(tickers, start="2021-05-01", end="2026-05-01", auto_adjust=True)
    print(f"Downloaded raw shape: {raw.shape}")

    # Stack from wide (MultiIndex columns: field x ticker) to long
    df = raw.stack(level=1).reset_index()
    df.columns = ["price_date", "ticker", "close", "high", "low", "open", "volume"]
    df = df.dropna()
    df["price_date"] = pd.to_datetime(df["price_date"]).dt.date
    df["volume"] = df["volume"].astype("int64")
    print(f"Reshaped prices rows: {len(df)}")

    df.to_sql("prices", engine, if_exists="append", index=False, chunksize=500)
    with engine.connect() as conn:
        count = conn.execute(text("SELECT COUNT(*) FROM prices")).scalar()
    print(f"prices loaded: {count} rows")


if __name__ == "__main__":
    load_assets()
    load_prices()
