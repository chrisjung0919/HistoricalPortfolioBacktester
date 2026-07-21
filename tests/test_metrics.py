import numpy as np
import pandas as pd

from src.metrics import (
    annualized_volatility,
    total_return,
    annualized_return,
    sharpe_ratio,
    maximum_drawdown,
    beta,
)


def test_annualized_volatility():
    daily_returns = pd.Series([0.01, -0.02, 0.03, -0.01, 0.02])

    expected = daily_returns.std() * np.sqrt(252) * 100
    result = annualized_volatility(daily_returns)

    assert np.isclose(result, expected)


def test_total_return():
    portfolio_value = pd.Series([10000, 11000, 12000])

    final_value, return_percentage = total_return(portfolio_value)

    assert final_value == 12000
    assert return_percentage == 20.0


def test_total_return_with_custom_initial_investment():
    portfolio_value = pd.Series([5000, 5500, 6000])

    final_value, return_percentage = total_return(
        portfolio_value,
        initial_investment=5000,
    )

    assert final_value == 6000
    assert return_percentage == 20.0


def test_annualized_return():
    portfolio_value = pd.Series([10000, 12100])

    result = annualized_return(
        portfolio_value,
        years=2,
    )

    assert np.isclose(result, 10.0)


def test_sharpe_ratio():
    result = sharpe_ratio(
        annual_return=12,
        annual_volatility=10,
        risk_free_rate=2,
    )

    assert result == 1.0


def test_maximum_drawdown():
    portfolio_value = pd.Series([100, 120, 80, 140])

    result = maximum_drawdown(portfolio_value)

    assert np.isclose(result, -33.33333333333333)


def test_beta():
    portfolio_returns = pd.Series([0.01, 0.02, -0.01, 0.03, 0.01])
    benchmark_returns = pd.Series([0.005, 0.015, -0.02, 0.025, 0.01])

    covariance_matrix = np.cov(
        portfolio_returns,
        benchmark_returns,
    )

    expected = (
        covariance_matrix[0, 1]
        / covariance_matrix[1, 1]
    )

    result = beta(
        portfolio_returns,
        benchmark_returns,
    )

    assert np.isclose(result, expected)