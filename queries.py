#!/usr/bin/env python3
import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv("/Users/trevorlorenz/Desktop/IS 445/AD Hoc Project/.env")
password = os.getenv("DB_PASSWORD")
engine = create_engine(f"mysql+pymysql://root:{password}@localhost/macro_db")


def query1_cumulative_return():
    sql = """
        SELECT
            ticker,
            ROUND((last_close - first_close) / first_close * 100, 2) AS cumulative_return_pct
        FROM (
            SELECT
                ticker,
                MIN(CASE WHEN rn_asc  = 1 THEN close END) AS first_close,
                MIN(CASE WHEN rn_desc = 1 THEN close END) AS last_close
            FROM (
                SELECT
                    ticker, close,
                    ROW_NUMBER() OVER (PARTITION BY ticker ORDER BY price_date ASC)  AS rn_asc,
                    ROW_NUMBER() OVER (PARTITION BY ticker ORDER BY price_date DESC) AS rn_desc
                FROM prices
            ) ranked
            GROUP BY ticker
        ) summary
        ORDER BY cumulative_return_pct DESC
    """
    df = pd.read_sql(text(sql), engine)
    print("\n--- Query 1: Cumulative Return ---")
    print(df.to_string(index=False))
    return df


def query2_annualized_volatility():
    sql = """
        SELECT
            ticker,
            ROUND(STD(daily_return) * SQRT(252) * 100, 2) AS annualized_volatility_pct
        FROM (
            SELECT
                ticker,
                close,
                LAG(close) OVER (PARTITION BY ticker ORDER BY price_date) AS prev_close,
                (close - LAG(close) OVER (PARTITION BY ticker ORDER BY price_date))
                    / LAG(close) OVER (PARTITION BY ticker ORDER BY price_date) AS daily_return
            FROM prices
        ) returns
        WHERE daily_return IS NOT NULL
        GROUP BY ticker
        ORDER BY annualized_volatility_pct DESC
    """
    df = pd.read_sql(text(sql), engine)
    print("\n--- Query 2: Annualized Volatility ---")
    print(df.to_string(index=False))
    return df


def query3_max_drawdown():
    sql = """
        SELECT
            ticker,
            ROUND(MIN((close - running_max) / running_max) * 100, 2) AS max_drawdown_pct
        FROM (
            SELECT
                ticker,
                price_date,
                close,
                MAX(close) OVER (PARTITION BY ticker ORDER BY price_date
                                  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_max
            FROM prices
        ) dd
        GROUP BY ticker
        ORDER BY max_drawdown_pct ASC
    """
    df = pd.read_sql(text(sql), engine)
    print("\n--- Query 3: Maximum Drawdown ---")
    print(df.to_string(index=False))
    return df


def query4_annual_returns():
    sql = """
        SELECT
            ticker,
            yr,
            ROUND((last_close - first_close) / first_close * 100, 2) AS annual_return_pct
        FROM (
            SELECT
                ticker,
                yr,
                MIN(CASE WHEN rn_asc  = 1 THEN close END) AS first_close,
                MIN(CASE WHEN rn_desc = 1 THEN close END) AS last_close
            FROM (
                SELECT
                    ticker,
                    YEAR(price_date) AS yr,
                    close,
                    ROW_NUMBER() OVER (PARTITION BY ticker, YEAR(price_date) ORDER BY price_date ASC)  AS rn_asc,
                    ROW_NUMBER() OVER (PARTITION BY ticker, YEAR(price_date) ORDER BY price_date DESC) AS rn_desc
                FROM prices
            ) ranked
            GROUP BY ticker, yr
        ) summary
        ORDER BY ticker, yr
    """
    df = pd.read_sql(text(sql), engine)
    pivoted = df.pivot(index="ticker", columns="yr", values="annual_return_pct")
    pivoted.columns.name = None
    print("\n--- Query 4: Annual Returns by Year (%) ---")
    print(pivoted.to_string())
    return pivoted


if __name__ == "__main__":
    query1_cumulative_return()
    query2_annualized_volatility()
    query3_max_drawdown()
    query4_annual_returns()
