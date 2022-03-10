import numpy as np
from scipy.stats import norm

N = norm.cdf
Np = norm.pdf


def bs_price(S, K, T, R, sigma, option_type):
    d1 = (np.log(S / K) + (R + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == "C":
        price = S * N(d1) - K * np.exp(-R*T)* N(d2)
    elif option_type == "P":
        price = K*np.exp(-R*T)*N(-d2) - S*N(-d1)
    return price


def bs_delta(S, K, T, R, sigma, option_type):
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


def bs_theta(S, K, T, R, sigma, option_type):
    d1 = (np.log(S / K) + (R + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == "C":
        theta = -S * Np(d1) * sigma / (2 * np.sqrt(T)) - R * K * np.exp(-R * T) * N(d2)
    elif option_type == "P":
        theta = -S * Np(d1) * sigma / (2 * np.sqrt(T)) + R * K * np.exp(-R * T) * N(-d2)
    return theta / 365


def bs_rho(S, K, T, R, sigma, option_type):
    d1 = (np.log(S / K) + (R + sigma ** 2 / 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == "C":
        rho = K * T * np.exp(-R * T) * N(d2)
    elif option_type == "P":
        rho = -K * T * np.exp(-R * T) * N(-d2)
    return rho * 0.01
