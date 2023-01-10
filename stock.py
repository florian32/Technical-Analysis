import time
import pandas as pd
import numpy as np
import matplotlib

matplotlib.use('Agg')
from matplotlib import pyplot as plt
from collections import defaultdict
from scipy.signal import argrelextrema
import cufflinks as cf
from pandas_datareader import data
import requests
import sys
import yfinance as yf


class Stock:
    def __init__(self, symbol, timestamp):
        self.max_min = None
        self.symbol = symbol
        self.timestamp = timestamp
        self.df = yf.download(tickers=self.symbol, period=timestamp)
        self.patterns = defaultdict(list)

    def get_min_max(self, smoothing, window_range):
        prices = self.df["Close"]
        try:
            smooth_prices = prices['Close'].rolling(window=smoothing).mean().dropna()
        except KeyError:
            smooth_prices = prices.rolling(window=smoothing).mean().dropna()
        local_max = argrelextrema(smooth_prices.values, np.greater)[0]
        local_min = argrelextrema(smooth_prices.values, np.less)[0]
        price_local_max_dt = []
        for i in local_max:
            if (i > window_range) and (i < len(prices) - window_range):
                price_local_max_dt.append(prices.iloc[i - window_range:i + window_range].idxmax())
        price_local_min_dt = []
        for i in local_min:
            if (i > window_range) and (i < len(prices) - window_range):
                price_local_min_dt.append(prices.iloc[i - window_range:i + window_range].idxmin())
        maxima = pd.DataFrame(prices.loc[price_local_max_dt])
        minima = pd.DataFrame(prices.loc[price_local_min_dt])
        max_min = pd.concat([maxima, minima]).sort_index()
        max_min.index.name = 'Date'
        max_min = max_min.reset_index()
        max_min = max_min[~max_min.Date.duplicated()]
        p = prices.reset_index()
        max_min['day_num'] = p[p['Date'].isin(max_min.Date)].index.values
        try:
            self.max_min = max_min.set_index('day_num')['Close']
        except KeyError:
            self.max_min = max_min.set_index('day_num')

    def find_inverse_head_and_shoulders(self, stock_symbol=None):
        # Window range is 5 units
        for i in range(5, len(self.max_min)):
            window = self.max_min.iloc[i - 5:i]
            if stock_symbol:
                window = window[stock_symbol]

            # Pattern must play out in less than n units
            if window.index[-1] - window.index[0] > 100:
                continue
            a, b, c, d, e = window.iloc[0:5]

            # IHS
            if a < b and c < a and c < e and c < d and e < d and abs(b - d) <= np.mean([b, d]) * 0.02:
                self.patterns['IHS'].append((window.index[0], window.index[-1]))

    def plot_minmax_patterns(self, window, ema, sma=False, resistance_levels=False, formations=False):
        if len(self.patterns) == 0 or (not sma and not resistance_levels and not formations):
            print("dziala if")
            prices = self.df["Close"]
            image_timestamp = str(time.time()).split(".")[0]
            image_dir = f"./static/img/no-patterns-{image_timestamp}.png"
            prices.plot()
            plt.savefig(image_dir)
            plt.close()
            return image_dir, 0

        else:
            incr = str((self.df.index[1] - self.df.index[0]).seconds / 60)
            max_min = self.max_min
            num_pat = len([x for x in self.patterns.items()][0][1])
            f, axes = plt.subplots(1, 2, figsize=(16, 5))
            axes = axes.flatten()
            try:
                prices_ = self.df.reset_index()['Close']
            except KeyError:
                prices_ = self.df.reset_index()[self.symbol]
                max_min = self.max_min[self.symbol]
            axes[0].plot(self.df["Close"])
            axes[1].plot(prices_)
            for name, end_day_nums in self.patterns.items():
                for i, tup in enumerate(end_day_nums):
                    sd = tup[0]
                    ed = tup[1]
                    axes[1].scatter(max_min.loc[sd:ed].index,
                                    max_min.loc[sd:ed].values,
                                    s=200, alpha=.3)
                    plt.yticks([])
            plt.tight_layout()
            plt.title('{}: {}: EMA {}, Window {} ({} patterns)'.format(self.symbol, incr, ema, window, num_pat))
            image_timestamp = str(time.time()).split(".")[0]
            image_dir = f"./static/img/{image_timestamp}.png"
            plt.savefig(image_dir)
            plt.close()
            return image_dir, num_pat
