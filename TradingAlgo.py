import MainFunctions

TimeFrame = "35 Minutes UTC"
ticker = "XLMBTC"
#First asset = asset buying, so in this case XLM
#Second asset = currency used to buy asset, so in this case BTC
first_asset = ticker[0:3]
second_asset = ticker[3:]
print("Analysis on: " + ticker)

i = 0
Action = 0
CurrentHoldings = False
TradeCount = 0
MACDConsecutiveBuy = 0
MACDConsecutiveSell = 0

#Gives the algorithim a simulation balance of 0.02 bitcoin
balance = 0.02

#prints out the starting asset balance
print("Starting balance: " + str(balance) + " " + str(second_asset))

#Building the database before starting
df = GetData(ticker, TimeFrame)


while(i < 400):
  #Gets data every 20 seconds, and then adds that data to the current dataframe
  newData = GetData(ticker,TimeFrame)
  newData = newData.tail(1)
  df = pd.concat([df, newData])
  df = df[['time','open','low','high','close','price']]
  df = StockDataFrame.retype(df)

  #Gives the current time in year-month-hour + time format
  CurrentTime = df['time'].tail(1)
  CurrentTime = CurrentTime.iloc[0]

  #calls the earlier function to get the current price
  CurrentPrice = GetPrice(ticker)

  #prints out data that helps create readable logs
  print("Attempt Number:" + str(i+1))
  print("Current Time: " + str(CurrentTime))
  print("Current Price: " + str(GetPrice(ticker)))

  #SMAInc = Checks if simple moving average value is increasing
  SMAInc = PotentialTrade.SMAIncreasing(df)

  #SMACheck = checks if the SMA currently signals a buy/sell
  SMACheck = PotentialTrade.SMACheck(df)

  #Currentholdings = false -> signals a buy position; currently holding BTC buying XLM
  if(CurrentHoldings == False):
    MACDCross = PotentialTrade.MACDCrossCheck(df, CurrentPrice)
#converts the simulation starting balance into the amount of other currency balance
#that it can afford
    PurchaseQuantity = Decimal(balance)/Decimal(CurrentPrice)
    x = Decimal(0.9)
    PurchaseQuantity = math.floor(PurchaseQuantity * x)
    print("Currently attempting to purchase.. " + str(PurchaseQuantity))

#The "Action" value is a point system -> Once it passes a threshold it's a good buy
#Different indicators have different weighting - ex: MACD Cross or crossed right before is +2

#if the asset is not at a current high over the past minute, then it gains a point
#this is to ensure that the algorithim doesn't think random spikes are good buys
    if(PotentialTrade.CurrentHigh(df, CurrentPrice) == False):
        Action += 1

#Checks if the MACD has recently signaled a good buy
    if(MACDPast == True):
        print("MACD before is True")
        MACDPast = False
        Action += 2

#MACD cross signal as good buy
    if(MACDCross == True):
        print("MACD Cross True")
        Action += 2
        MACDPast = True

#makes sure the asset hasn't gone above the upper bollinger band
    if(PotentialTrade.BollingerUpperCheck(df, CurrentPrice) == False):
        Action += 1

#Checks if the TRIX value is increasing
    if(PotentialTrade.TrixIncreasing(df) == True):
        print("Trix increasing")
        Action += 1

#Checks if the SMA value is increasing
    if(SMAInc == True):
      print("SMA increasing")
      Action += 1

#From running simulations, trix values below this threshold are often bad buys
    x = PotentialTrade.GetTrix(df)
    if(x < -.02):
        Action += 1

#The above conditions all work on a point system, so if enough of the criteria are met
#then the system initiates a simulation buy, in this case if point is at least 7
    if(Action >= 7):
      CurrentHoldings = True
      print("Iniating Buy order: " + str(CurrentPrice))
      FloatPrice = float(CurrentPrice)
      SecondAssetAmount = Actions.InitiateBuy(ticker, balance, PurchaseQuantity)
      PurchaseValue = Decimal(CurrentPrice)

    Action = 0

#If XLM/(second currency) is currently owned -> algorithim takes a sell position
#when it starts off in a sell position the indicators are mostly indicating buy
#therefore the sell action would be triggered if the indicators signalled a possible drop

  if(CurrentHoldings == True):
#i values are always reduced so that the program doesn't end when it's currently in a sell position
    i = i-1
    MACD = PotentialTrade.MACDAboveCheck(df, CurrentPrice)

#sells the current balance that was "purchased"
    SellAmount = balance

#starts checking the indicators if they still signal a strong hold
    TrixInc = PotentialTrade.TrixIncreasing(df)
    MACDAbove = PotentialTrade.MACDAboveCheck(df, CurrentPrice)
    print("Currently attempting to sell.." + str(SellAmount))

#if the SMA is not increasing it means the value could be dropping
    if(SMAInc == False):
        print("SMA is not increasing")
        Action -= 1

#Trix not increasing means the value of the asset is most likely about to decrease
    if(TrixInc == False):
        print("Trix is not increasing")
        Action -= 2

#MACD below signal line indicators a future bearish market (price is dropping soon)
    if(MACDAbove == False):
        print("MACD First Below")
        time.sleep(3)
        MACDSecondAbove = PotentialTrade.MACDAboveCheck(df, CurrentPrice)
        if(MACDSecondAbove == False):
          print("Second MACD Below")
          Action -= 1

#The above conditions all work on a point system, so if enough of the criteria are met
#then the system initiates a simulation sell
    if(Action <= -2):
        #Find the current value of the asset
        SellValue = Decimal(CurrentPrice)

        #Adds one to the final tradecount
        TradeCount += 1
        print("Iniating Sell order:" + str(CurrentPrice))
        FloatPrice = float(CurrentPrice)

#Initates the simulation sell order to calculate the new balance(so new BTC balance)
        newBalance = Actions.InitiateSell(CurrentPrice, balance , SecondAssetAmount)

#Calculates the percent profit from the buy/sell values for that simulation trade
        PercentProfit = (Decimal(SellValue) - Decimal(PurchaseValue))/Decimal(PurchaseValue)
        PercentProfit = PercentProfit * 100
        print("Percent Profit: " + str(PercentProfit))
        print("Total Simulation Trades:" + str(TradeCount))
        CurrentHoldings = False

  print("\n")
  Action = 0
  i = i+1
#program waits 20 seconds before sending another request for data and checking the indicators
#again, this is to ensure the public database doesn't flag for spamming requests too much
  time.sleep(20)

#end while loop

print("Final Trade Count:" + str(TradeCount))

#Gives overall statistics regarding buy/sell quantity; percent profit/loss
final_balance = Decimal(balance)
overall_profit = ((final_balance - starting_balance)/starting_balance) * 100
print("Final Amount: " +str(balance))
print("Overall profit: " + str(overall_profit))
