import time
import pandas as pd
import numpy as np
import matplotlib

matplotlib.use('Agg')
from matplotlib import pyplot as plt
from collections import defaultdict
from config import config
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

    def get_min_max(self):
        prices = self.df["Close"]
        try:
            smooth_prices = prices['Close'].rolling(window=config.SMOOTHING).mean().dropna()
        except KeyError:
            smooth_prices = prices.rolling(window=config.SMOOTHING).mean().dropna()
        local_max = argrelextrema(smooth_prices.values, np.greater)[0]
        local_min = argrelextrema(smooth_prices.values, np.less)[0]
        price_local_max_dt = []
        for i in local_max:
            if (i > config.WINDOW_RANGE) and (i < len(prices) - config.WINDOW_RANGE):
                price_local_max_dt.append(prices.iloc[i - config.WINDOW_RANGE:i + config.WINDOW_RANGE].idxmax())
        price_local_min_dt = []
        for i in local_min:
            if (i > config.WINDOW_RANGE) and (i < len(prices) - config.WINDOW_RANGE):
                price_local_min_dt.append(prices.iloc[i - config.WINDOW_RANGE:i + config.WINDOW_RANGE].idxmin())
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

    def find_patterns(self):
        for i in range(5, len(self.max_min)):
            window = self.max_min.iloc[i - 5:i]
            a, b, c, d, e = window.iloc[0:5]
            # IHS
            if b > a > c and c < e and c < d and e < d and abs(b - d) <= np.mean([b, d]) * 0.02 and abs(
                    a - e) <= np.mean([a, e]) * 0.02:
                self.patterns['IHS'].append((window.index[0], window.index[-1]))
            # HS
            if a > b and c > a and c > e and d < a and e > d and abs(b - d) <= np.mean([b, d]) * 0.02 and abs(
                    a - e) <= np.mean([a, e]) * 0.02:
                self.patterns['HS'].append((window.index[0], window.index[-1]))
            # AT
            if a > b and b < d < e and abs(a - c) <= np.mean([a, c]) * 0.01 and abs(a - e) <= np.mean(
                    [a, e]) * 0.01:
                self.patterns['AT'].append((window.index[0], window.index[-1]))

    def find_supp_lines(self):
        supp_lines = []
        for i in range(5, len(self.max_min)):
            window = self.max_min.iloc[i - 5:i]
            a, b, c, d, e = window.iloc[0:5]
            if c < b and c < d < e and b < a:
                supp_lines.append(c)
        return supp_lines

    def find_res_lines(self):
        res_lines = []
        for i in range(5, len(self.max_min)):
            window = self.max_min.iloc[i - 5:i]
            a, b, c, d, e = window.iloc[0:5]
            if c > b and c > d > e and b > a:
                res_lines.append(c)
        return res_lines

    def plot_minmax_patterns(self, sma=False, resistance_levels=False, formations=False):
        if len(self.patterns) == 0 or not formations:
            prices = self.df["Close"]
            image_timestamp = str(time.time()).split(".")[0]
            image_dir = f"./temp/img/no-patterns-{image_timestamp}.png"
            prices.plot(label="Price")
            plt.title(self.symbol)
            plt.legend()
            plt.ylabel("Price [USD]")
            if sma:
                price_avg = prices.rolling(window=7).mean()
                price_avg.plot(color='m', linestyle=':', label="SMA")
                plt.legend(["Price", "SMA"])
            if resistance_levels:
                res_lines = self.find_res_lines()
                supp_lines = self.find_supp_lines()
                counter = 0
                for line in supp_lines:
                    if counter == 0:
                        plt.axhline(y=line, color='b', linestyle=':', label="Support line")
                    else:
                        plt.axhline(y=line, color='b', linestyle=':')
                    counter += 1
                counter = 0
                for line in res_lines:
                    if counter == 0:
                        plt.axhline(y=line, color='r', linestyle=':', label="Resistance line")
                    else:
                        plt.axhline(y=line, color='r', linestyle=':')
                    counter += 1
                plt.ylabel("Price [USD]")
                plt.title(self.symbol)
                plt.legend()
            plt.savefig(image_dir)
            plt.close()
            return image_dir, 0

        else:
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
            axes[0].set_xlabel("Date")
            axes[1].plot(prices_)
            axes[1].set_xlabel("Day number")
            if sma:
                price_avg = prices_.rolling(window=7).mean()
                axes[1].plot(price_avg)
                plt.legend(["Price", "SMA"])
            for name, end_day_nums in self.patterns.items():
                for i, tup in enumerate(end_day_nums):
                    sd = tup[0]
                    ed = tup[1]
                    axes[1].scatter(max_min.loc[sd:ed].index,
                                    max_min.loc[sd:ed].values,
                                    s=200, alpha=.3, label=name)
                    plt.yticks([])
            plt.tight_layout()
            plt.title(self.symbol)
            if sma:
                price_avg = prices_.rolling(window=7).mean()
                price_avg.plot(color='m', linestyle=':', label="SMA")
            if resistance_levels:
                res_lines = self.find_res_lines()
                supp_lines = self.find_supp_lines()
                counter = 0
                for line in supp_lines:
                    if counter == 0:
                        plt.axhline(y=line, color='b', linestyle=':', label="Support line")
                    else:
                        plt.axhline(y=line, color='b', linestyle=':')
                    counter += 1
                counter = 0
                for line in res_lines:
                    if counter == 0:
                        plt.axhline(y=line, color='r', linestyle=':', label="Resistance line")
                    else:
                        plt.axhline(y=line, color='r', linestyle=':')
                    counter += 1

            plt.title(self.symbol)
            plt.legend()
            plt.ylabel("Price [USD]")
            image_timestamp = str(time.time()).split(".")[0]
            image_dir = f"./temp/img/{image_timestamp}.png"
            plt.savefig(image_dir)
            plt.close()
            return image_dir, num_pat
