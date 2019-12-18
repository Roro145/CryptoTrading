Overall Summary of Cryptocurrency Trading Algorithm:

    Program Last Updated: August 2018

    First, the program collects historical data (ex: past 35 minutes) to attain values
which can be passed through indicators to determine the current state of the market.
From there, the program runs the data through various indicators such as Moving Average
Convergence Divergence(MACD), Triple Smoothed Moving Average(TRIX), Simple Moving Average(SMA),
and Bollinger Bands.

   The program collects live data every 20 seconds, and this data is then processed using
different stock indicators. The indicators are mathematical quantities which financial
analysts use to determine the current state of the stock, such as whether it's expected
to go up or down. After the program uses various indicators(~6 indicators) on a point
system so if a certain number of the criteria are met (ex: 4 indicators signal a good buy),
then the program will initiate a simulation buy order. After purchasing the new asset, the
program moves into a sell position. In this position, the program continues to collect data
at the 20-second interval and process it using indicators. Similar to the buy position, the
sell position works on a point system, meaning that once a certain number of the indicators(2)
signal a strong sell, the program initiates a simulation sell order.

   After completing this first buy/sell cycle, the program records data such
as percent gained/loss from that individual trade, and then moves back into a buy position. At
the conclusion of the program (runs for a certain time interval), data is printed out which
includes the number of trades, and the percent gained/loss overall.

-- Below the Program is a sample output trading logs
*Although the program attains live data, the trades themselves are simulated
*data pulled from public source
