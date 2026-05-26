# Macro Asset Class Analysis (IS 445 Final Project)

Pulls 5 years of daily ETF price data from Yahoo Finance, stores it in a MySQL database, and analyzes macro asset class performance from May 2021 to May 2026.

## Assets Tracked

| Ticker | Name | Category |
|--------|------|----------|
| SPY | S&P 500 ETF | Equity |
| XLE | Energy Select Sector SPDR | Equity-Energy |
| GLD | SPDR Gold Shares | Commodity |
| USO | United States Oil Fund | Commodity |
| TLT | iShares 20+ Year Treasury Bond ETF | Fixed Income |

## Project Structure

macro_project/
├── pipeline.py      # Downloads data from yfinance and loads into MySQL
├── queries.py       # SQL analysis queries (returns, volatility, drawdown)
├── analysis.py      # Python analysis (Sharpe ratio, correlation, charts)
├── schema.sql       # MySQL database and table definitions
└── outputs/
├── cumulative_returns.png
├── correlation_matrix.png
└── drawdown_chart.png



## Setup

**1. Clone the repo and enter the project folder**
```bash
git clone <your-repo-url>
cd "macro project"
2. Create and activate the virtual environment


python3 -m venv .venv
source .venv/bin/activate
pip install yfinance pandas sqlalchemy pymysql python-dotenv seaborn matplotlib numpy
3. Create a .env file with your MySQL password (do not commit this file):


DB_PASSWORD=your_password_here
4. Create the database


mysql -u root -p < schema.sql
5. Run the pipeline


python pipeline.py    # loads 6,275 rows across 5 tickers
python queries.py     # prints SQL analysis results
python analysis.py    # prints stats and saves charts to outputs/
Key Findings (May 2021 – May 2026)
Cumulative Return
Ticker	Return
USO	+234%
XLE	+183%
GLD	+152%
SPY	+84%
TLT	-27%
Annualized Volatility
Ticker	Volatility
USO	35.6%
XLE	26.0%
GLD	17.9%
SPY	17.1%
TLT	15.9%
Maximum Drawdown
Ticker	Max Drawdown
TLT	-43.7%
USO	-36.2%
XLE	-26.0%
SPY	-24.5%
GLD	-21.0%
Sharpe Ratio (rf = 2%)
Ticker	Sharpe
GLD	1.02
XLE	0.86
USO	0.80
SPY	0.69
TLT	-0.45
Tech Stack
Python 3.14, pandas, yfinance, SQLAlchemy, pymysql, seaborn, matplotlib
MySQL 8
python-dotenv for credential management
Notes
Database credentials are loaded from a .env file and never hardcoded
Both tables are protected against duplicate loads (skips if data already exists)
Price data uses auto_adjust=True to account for splits and dividends


A few things worth noting before you paste this into GitHub:

- Add a `.gitignore` that includes `.env` and `.venv/` so you don't accidentally commit your password or the entire virtual environment folder
- The `outputs/` PNGs can either be committed (so people see the charts) or gitignored — up to you
