import numpy as np


def annualized_volatility(daily_returns):
    """
    Calculate annualized volatility from daily returns.
    """

    trading_days = 252

    volatility = (
        daily_returns.std()
        * np.sqrt(trading_days)
    ) * 100

    return volatility

def total_return(portfolio_value, initial_investment=10000):
    """
    Calculate the total percentage return of a portfolio.
    """

    final_value = portfolio_value.iloc[-1]

    total_return = (
        (final_value - initial_investment)
        / initial_investment
    ) * 100

    return final_value, total_return

def annualized_return(portfolio_value, years, initial_investment=10000):
    """
    Calculate the annualized return Compound Annual Growth Rate (CAGR).
    """

    final_value = portfolio_value.iloc[-1]

    annual_return = (
        (final_value / initial_investment) ** (1 / years) - 1
    ) * 100

    return annual_return

def sharpe_ratio(annual_return, annual_volatility, risk_free_rate=2):
    """
    Calculate the Sharpe Ratio.
    """

    sharpe = (
        annual_return - risk_free_rate
    ) / annual_volatility

    return sharpe

def maximum_drawdown(portfolio_value):
    """
    Calculate the maximum drawdown of a portfolio.
    """

    running_max = portfolio_value.cummax()

    drawdown = (
        portfolio_value - running_max
    ) / running_max

    max_drawdown = drawdown.min() * 100

    return max_drawdown

def beta(portfolio_returns, benchmark_returns):
    """
    Calculate portfolio beta relative to the benchmark.
    """

    covariance_matrix = np.cov(
        portfolio_returns,
        benchmark_returns
    )

    covariance = covariance_matrix[0, 1]

    benchmark_variance = covariance_matrix[1, 1]

    beta = covariance / benchmark_variance

    return beta