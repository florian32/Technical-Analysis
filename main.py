import requests
import pandas as pd
import matplotlib.pyplot as plt
from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from stock import Stock

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        stock_symbol = request.form.get("stock-name")
        timestamp = request.form.get("timestamp")
        current_stock = Stock(stock_symbol, timestamp)

        smoothing = 2
        window_range = 20

        current_stock.get_min_max(smoothing, window_range)
        current_stock.find_inverse_head_and_shoulders()
        current_stock.plot_minmax_patterns(window_range, smoothing)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
