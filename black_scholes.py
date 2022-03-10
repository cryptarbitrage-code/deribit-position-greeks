import numpy as np
from scipy.stats import norm

N = norm.cdf
Np = norm.pdf

S = 3000
K = 2000
T = 0.5692439751395231
R = 0
sigma = 0.9578
option_type = "P"


def option_profit(premium, strike, chart_low, chart_high, option_type="C"):
    profit_list = []
    steps = 100
    step = (chart_high - chart_low) / steps
    count = 0
    if option_type == "C":
        while count < steps + 1:
            if chart_low + (count * step) < strike:
                profit_list.append(0 - premium)
            else:
                profit_list.append((chart_low + (count * step)) - strike - premium)
            count = count + 1
    else:
        while count < steps + 1:
            if chart_low + (count * step) < strike:
                profit_list.append(strike - (chart_low + (count * step)) - premium)
            else:
                profit_list.append(0 - premium)
            count = count + 1
    return profit_list


def inverse_option_profit(premium, strike, chart_low, chart_high, option_type="C"):
    profit_list = []
    steps = 100
    step = (chart_high - chart_low) / steps
    count = 0
    if option_type == "C":
        while count < steps + 1:
            if chart_low + (count * step) < strike:
                profit_list.append(0 - premium)
            else:
                profit_list.append(((chart_low + (count * step)) - strike)/(chart_low + (count * step)) - premium)
            count = count + 1
    else:
        while count < steps + 1:
            if chart_low + (count * step) < strike:
                profit_list.append((strike - (chart_low + (count * step)))/(chart_low + (count * step)) - premium)
            else:
                profit_list.append(0 - premium)
            count = count + 1
    return profit_list


def bs_price(S, K, T, R, sigma, option_type="C"):
    d1 = (np.log(S / K) + (R + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == "C":
        price = S * N(d1) - K * np.exp(-R*T)* N(d2)
    elif option_type == "P":
        price = K*np.exp(-R*T)*N(-d2) - S*N(-d1)
    return price


def bs_delta(S, K, T, R, sigma, option_type="C"):
    d1 = (np.log(S / K) + (R + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    if option_type == "C":
        delta = N(d1)
    elif option_type == "P":
        delta = N(d1) - 1
    return delta


def bs_gamma(S, K, T, R, sigma):
    d1 = (np.log(S / K) + (R + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))

    gamma = Np(d1) / (S * sigma * np.sqrt(T))
    return gamma


def bs_vega(S, K, T, R, sigma):
    d1 = (np.log(S / K) + (R + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))

    vega = S * Np(d1) * np.sqrt(T)
    return vega * 0.01


def bs_theta(S, K, T, R, sigma, option_type="C"):
    d1 = (np.log(S / K) + (R + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == "C":
        theta = -S * Np(d1) * sigma / (2 * np.sqrt(T)) - R * K * np.exp(-R * T) * N(d2)
    elif option_type == "P":
        theta = -S * Np(d1) * sigma / (2 * np.sqrt(T)) + R * K * np.exp(-R * T) * N(-d2)
    return theta / 365


def bs_rho(S, K, T, R, sigma, option_type="C"):
    d1 = (np.log(S / K) + (R + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == "C":
        rho = K * T * np.exp(-R * T) * N(d2)
    elif option_type == "P":
        rho = -K * T * np.exp(-R * T) * N(-d2)
    return rho * 0.01
