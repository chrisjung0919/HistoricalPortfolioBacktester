from data_loader import download_stock_data
from portfolio import equal_weight_portfolio, inverse_variance_weights, inverse_variance_portfolio
from metrics import (total_return, annualized_return, annualized_volatility, 
                     sharpe_ratio, maximum_drawdown, beta)
from datetime import datetime
from report import create_pdf_report

import matplotlib.pyplot as plt

print("Historical Portfolio Backtester")

tickers_input = input(
    "Enter stock tickers (comma separated): "
)

portfolio_tickers = [
    ticker.strip().upper()
    for ticker in tickers_input.split(",")
]

benchmark_ticker = input(
    "Enter benchmark ticker: "
).upper()

start_date = input(
    "Enter start date (YYYY-MM-DD): "
)

end_date = input(
    "Enter end date (YYYY-MM-DD): "
)

initial_investment = float(
    input(
        "Enter initial investment: "
    )
)

# Download historical stock prices
stock_data = download_stock_data(
    portfolio_tickers,
    start_date,
    end_date
)

benchmark_data = download_stock_data(
    [benchmark_ticker],
    start_date,
    end_date
)

benchmark_close = benchmark_data["Close"]

benchmark_returns = benchmark_close.pct_change().dropna()

benchmark_value = (
    1 + benchmark_returns.squeeze()
).cumprod() * initial_investment

# Keep only the closing prices
close_prices = stock_data["Close"]

# Calculate daily percentage returns
daily_returns = close_prices.pct_change()

# Remove the first row containing NaN values
daily_returns = daily_returns.dropna()

portfolio_returns, portfolio_value = equal_weight_portfolio(daily_returns, portfolio_tickers, initial_investment)

inverse_returns, inverse_value, inverse_weights = (
    inverse_variance_portfolio(daily_returns, initial_investment)
)

start = datetime.strptime(start_date, "%Y-%m-%d")
end = datetime.strptime(end_date, "%Y-%m-%d")

years = (end - start).days / 365.25

inverse_final_value, inverse_total_return = total_return(
    inverse_value,
    initial_investment
)

inverse_annual_return = annualized_return(
    inverse_value,
    years,
    initial_investment
)

inverse_volatility = annualized_volatility(
    inverse_returns
)

inverse_sharpe = sharpe_ratio(
    inverse_annual_return,
    inverse_volatility
)

inverse_drawdown = maximum_drawdown(
    inverse_value
)

inverse_beta = beta(
    inverse_returns,
    benchmark_returns.squeeze()
)

final_portfolio_value, portfolio_total_return = total_return(
    portfolio_value
    ,initial_investment
)

final_benchmark_value, benchmark_total_return = total_return(
    benchmark_value,
    initial_investment
)

portfolio_annual_return = annualized_return(
    portfolio_value,
    years,
    initial_investment
)

benchmark_annual_return = annualized_return(
    benchmark_value,
    years,
    initial_investment
)

portfolio_volatility = annualized_volatility(
    portfolio_returns
)

benchmark_volatility = annualized_volatility(
    benchmark_returns.squeeze()
)

portfolio_sharpe = sharpe_ratio(
    portfolio_annual_return,
    portfolio_volatility
)

benchmark_sharpe = sharpe_ratio(
    benchmark_annual_return,
    benchmark_volatility
)

portfolio_drawdown = maximum_drawdown(
    portfolio_value
)

benchmark_drawdown = maximum_drawdown(
    benchmark_value
)

portfolio_beta = beta(
    portfolio_returns,
    benchmark_returns.squeeze()
)



print()

print("=" * 95)
print("                    Portfolio Strategy Comparison")
print("=" * 95)

print(
    f"{'Metric':<22}"
    f"{'Equal Weight':>18}"
    f"{'Inverse Variance':>22}"
    f"{'SPY':>18}"
)

print("-" * 95)

print(
    f"{'Final Value':<22}"
    f"{('$' + format(final_portfolio_value, ',.2f')):>18}"
    f"{('$' + format(inverse_final_value, ',.2f')):>22}"
    f"{('$' + format(final_benchmark_value, ',.2f')):>18}"
)

print(
    f"{'Total Return':<22}"
    f"{portfolio_total_return:>17.2f}%"
    f"{inverse_total_return:>21.2f}%"
    f"{benchmark_total_return:>17.2f}%"
)

print(
    f"{'Annual Return':<22}"
    f"{portfolio_annual_return:>17.2f}%"
    f"{inverse_annual_return:>21.2f}%"
    f"{benchmark_annual_return:>17.2f}%"
)

print(
    f"{'Volatility':<22}"
    f"{portfolio_volatility:>17.2f}%"
    f"{inverse_volatility:>21.2f}%"
    f"{benchmark_volatility:>17.2f}%"
)

print(
    f"{'Sharpe Ratio':<22}"
    f"{portfolio_sharpe:>17.2f}"
    f"{inverse_sharpe:>21.2f}"
    f"{benchmark_sharpe:>17.2f}"
)

print(
    f"{'Max Drawdown':<22}"
    f"{portfolio_drawdown:>17.2f}%"
    f"{inverse_drawdown:>21.2f}%"
    f"{benchmark_drawdown:>17.2f}%"
)

print(
    f"{'Beta':<22}"
    f"{portfolio_beta:>17.2f}"
    f"{inverse_beta:>21.2f}"
    f"{1.00:>17.2f}"
)

print("=" * 95)

print()

print("Inverse Variance Portfolio Weights")

for ticker, weight in zip(portfolio_tickers, inverse_weights):
    print(f"{ticker:<8}: {weight*100:.2f}%")



plt.figure(figsize=(12, 6))

plt.plot(
    portfolio_value,
    label="Equal Weight",
    linewidth=2
)

plt.plot(
    inverse_value,
    label="Inverse Variance",
    linewidth=2
)

plt.plot(
    benchmark_value,
    label="S&P 500",
    linewidth=2
)

plt.title(
    f"Portfolio Performance ({start_date} to {end_date})"
)

plt.xlabel("Date")

plt.ylabel("Portfolio Value ($)")

plt.legend()

plt.grid(True)

plt.savefig("../data/portfolio_comparison.png", dpi=300)

plt.show()

create_pdf_report(
    portfolio_tickers,
    benchmark_ticker,
    start_date,
    end_date,
    initial_investment,
    final_portfolio_value,
    inverse_final_value,
    final_benchmark_value,
    portfolio_total_return,
    inverse_total_return,
    benchmark_total_return,
    portfolio_annual_return,
    inverse_annual_return,
    benchmark_annual_return,
    portfolio_volatility,
    inverse_volatility,
    benchmark_volatility,
    portfolio_sharpe,
    inverse_sharpe,
    benchmark_sharpe,
    portfolio_drawdown,
    inverse_drawdown,
    benchmark_drawdown,
    portfolio_beta,
    inverse_beta,
    inverse_weights
)