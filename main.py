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
        resistance_lines = request.form.get("resistance_levels")
        formations = request.form.get("formations")
        sma = request.form.get("sma")
        print(f"resistance: {resistance_lines} formations: {formations} sma: {sma}")
        current_stock = Stock(stock_symbol, timestamp)

        smoothing = 2
        window_range = 20

        current_stock.get_min_max(smoothing, window_range)
        current_stock.find_inverse_head_and_shoulders()
        image_dir, patterns_num = current_stock.plot_minmax_patterns(window_range, smoothing)
        return render_template("index.html", image_dir=image_dir, pattern_num=patterns_num)
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
