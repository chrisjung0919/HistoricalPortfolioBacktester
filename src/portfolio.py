import pandas as pd
import numpy as np


def equal_weight_portfolio(daily_returns, tickers, initial_investment):
    """
    Calculate the value of an equal-weight portfolio over time.
    """

    number_of_stocks = len(tickers)

    weights = [1 / number_of_stocks] * number_of_stocks

    portfolio_returns = daily_returns.dot(weights)

    portfolio_value = (
        1 + portfolio_returns
    ).cumprod() * initial_investment

    return portfolio_returns, portfolio_value

def inverse_variance_weights(daily_returns):
    """
    Calculate inverse-variance portfolio weights.
    """

    covariance_matrix = daily_returns.cov()

    variances = np.diag(covariance_matrix)

    inverse_variances = 1 / variances

    weights = inverse_variances / inverse_variances.sum()

    return weights

def inverse_variance_portfolio(daily_returns, initial_investment):
    """
    Calculate portfolio performance using inverse-variance weights.
    """

    weights = inverse_variance_weights(daily_returns)

    portfolio_returns = daily_returns.dot(weights)

    portfolio_value = (
        1 + portfolio_returns
    ).cumprod() * initial_investment

    return portfolio_returns, portfolio_value, weights