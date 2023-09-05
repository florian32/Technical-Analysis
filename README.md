# Technical-Analysis
## Work in progress.


## About the project
### This project is meant to help investors with making decisions on wheather to buy or sell specific shares. The analysis functionality downloads current stock data from an external API, then processes it to the correct format and tries to find some patterns according to the technical analysis theory. The result of the analysis is an image showing stock prices chart with the technical analysis indicators.
### The whole project is build as a REST API using Flask and a PostgreSQL for user management (work in progress). For the analysis part the main modules used are: Pandas, Numpy, Matplotlib, SciPy.
## How does it work?
### The stock data is being received from the Yahoo API, then prepared for further analysis using Pandas. The technical indicators can be found by analysing the local min and max points on the chart.
### To find those spots I used a combination of NumPy and SciPy, and then save it in a Pandas Series. To find the indicators I iterate through these points using the sliding window approach and compare if the dependencies between the points match the theory criteria.
![image](https://github.com/florian32/Technical-Analysis/assets/97685387/e03a15c1-93ae-4769-9df1-e6c3072fa7ba)

![image](https://github.com/florian32/Technical-Analysis/assets/97685387/ca355197-2c5a-401b-ae76-1107287aefc6)

### If the algorithm finds a technical indicator the points on the chart will be stored with the indicator type. After the analysis finishes all the indicators are being added to the price chart.

![image](https://github.com/florian32/Technical-Analysis/assets/97685387/f84f8b17-b486-4079-b6d7-fab8744a8a63)

![image](https://github.com/florian32/Technical-Analysis/assets/97685387/a51eb04d-85f4-4355-855d-2bed4ec9b103)

## Endpoints
### Currentl endpoints:
### GET /api/news query params: symbol (stock symbol for the news), limit (how many articles should it show) - endpoint used to get stock news for investors using the marketaux API
### POST /api/analysis/<symbol> query params: timestamp (since when should it get the stock data), sma (should it plot the simple moving average), res(should it plot resistance levels), formations(should it plot formations) - endpoint used for creating image with the stock chart and the indicators included
### DELETE /api/delete query params: file_path: path to the unused image -  endpoint for deleting old plots
