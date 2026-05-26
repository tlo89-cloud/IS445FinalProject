CREATE DATABASE IF NOT EXISTS macro_db;
USE macro_db;

CREATE TABLE IF NOT EXISTS assets (
    ticker VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100),
    category VARCHAR(50),
    is_etf BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS prices (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ticker VARCHAR(10) NOT NULL,
    price_date DATE NOT NULL,
    open DECIMAL(10,2),
    high DECIMAL(10,2),
    low DECIMAL(10,2),
    close DECIMAL(10,2),
    volume BIGINT,
    FOREIGN KEY (ticker) REFERENCES assets(ticker),
    UNIQUE KEY unique_ticker_date (ticker, price_date)
);
