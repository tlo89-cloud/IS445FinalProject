#!/usr/bin/env python3
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv("/Users/trevorlorenz/Desktop/IS 445/AD Hoc Project/.env")
password = os.getenv("DB_PASSWORD")
engine = create_engine(f"mysql+pymysql://root:{password}@localhost/macro_db")

os.makedirs("outputs", exist_ok=True)

RISK_FREE_DAILY = 0.02 / 252


def load_prices():
    sql = "SELECT ticker, price_date, close FROM prices ORDER BY ticker, price_date"
    df = pd.read_sql(text(sql), engine)
    df["price_date"] = pd.to_datetime(df["price_date"])
    return df


def sharpe_ratios(df):
    returns = df.groupby("ticker")["close"].pct_change()
    df = df.copy()
    df["daily_return"] = returns
    sharpe = (
        df.groupby("ticker")["daily_return"]
        .apply(lambda r: (r.mean() - RISK_FREE_DAILY) / r.std() * np.sqrt(252))
        .sort_values(ascending=False)
        .rename("sharpe_ratio")
        .round(4)
    )
    print("\n--- Sharpe Ratios (annualized, rf=2%) ---")
    print(sharpe.to_string())
    return sharpe


def correlation_matrix(df):
    wide = df.pivot(index="price_date", columns="ticker", values="close")
    returns = wide.pct_change().dropna()
    corr = returns.corr().round(4)
    print("\n--- Correlation Matrix (daily returns) ---")
    print(corr.to_string())
    return corr


def plot_cumulative_returns(df):
    wide = df.pivot(index="price_date", columns="ticker", values="close")
    cum_ret = wide / wide.iloc[0] - 1

    fig, ax = plt.subplots(figsize=(12, 6))
    for ticker in cum_ret.columns:
        ax.plot(cum_ret.index, cum_ret[ticker] * 100, label=ticker, linewidth=1.5)

    ax.set_title("Cumulative Returns by Asset Class (May 2021 – May 2026)", fontsize=14)
    ax.set_xlabel("Date")
    ax.set_ylabel("Cumulative Return (%)")
    ax.legend(title="Ticker")
    ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
    fig.tight_layout()
    fig.savefig("outputs/cumulative_returns.png", dpi=150)
    plt.close(fig)
    print("Saved outputs/cumulative_returns.png")


def plot_correlation_heatmap(corr):
    fig, ax = plt.subplots(figsize=(7, 5))
    sns.heatmap(
        corr,
        annot=True,
        fmt=".2f",
        cmap="RdYlGn",
        vmin=-1,
        vmax=1,
        linewidths=0.5,
        ax=ax,
    )
    ax.set_title("Asset Return Correlation Matrix", fontsize=14)
    fig.tight_layout()
    fig.savefig("outputs/correlation_matrix.png", dpi=150)
    plt.close(fig)
    print("Saved outputs/correlation_matrix.png")


def plot_drawdown(df):
    wide = df.pivot(index="price_date", columns="ticker", values="close")
    running_max = wide.cummax()
    drawdown = (wide - running_max) / running_max * 100

    fig, ax = plt.subplots(figsize=(12, 6))
    for ticker in drawdown.columns:
        ax.plot(drawdown.index, drawdown[ticker], label=ticker, linewidth=1.5)

    ax.set_title("Rolling Drawdown by Asset Class (May 2021 – May 2026)", fontsize=14)
    ax.set_xlabel("Date")
    ax.set_ylabel("Drawdown (%)")
    ax.legend(title="Ticker")
    ax.axhline(0, color="black", linewidth=0.8, linestyle="--")
    fig.tight_layout()
    fig.savefig("outputs/drawdown_chart.png", dpi=150)
    plt.close(fig)
    print("Saved outputs/drawdown_chart.png")


if __name__ == "__main__":
    df = load_prices()
    sharpe_ratios(df)
    corr = correlation_matrix(df)
    plot_cumulative_returns(df)
    plot_correlation_heatmap(corr)
    plot_drawdown(df)
