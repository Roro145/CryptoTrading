#importing the various libraries that this program uses
from datetime import datetime
import numpy as np
import pandas as pd
import time
from decimal import *
from stockstats import StockDataFrame
import stockstats
import math


#converts the database time into a more understandable time
def ConvertTime(CurrentTime):
    CurrentTime = datetime.fromtimestamp(int(CurrentTime/1000))
    return CurrentTime

#Gets the price from the trading platform dataframe
def GetPrice(ticker):
    data = client.get_ticker(symbol=ticker)
    Price = data['lastPrice']
    return Price

#Gets historical data about the specific cryptocurrency to assemble accurate indicators
def GetData(ticker, TimeFrame):
    df = pd.DataFrame(columns = ['time','open','low','high','close','price'])
    klines = client.get_historical_klines(ticker, client.KLINE_INTERVAL_1MINUTE, TimeFrame)
    delta = len(klines)
    for x in range(0,delta):
        data = klines[x]
        CurrentTime = ConvertTime(int(data[0]))
        Open = data[1]
        Low = data[2]
        High = data[3]
        Close = data[4]
        getcontext().prec = 10
        Price = GetPrice(ticker)
        df.loc[x] = [CurrentTime, Open, Low, High, Close, Price]
    return df

#Potential markers for buy/sell trades
class PotentialTrade:
    #Checks if the current price is below the lower bollinger band
    def BollingerLowerCheck(newdf, CurrentPrice):
        newdf['boll_lb'] = newdf.get('boll_lb')
        newdf['median'] = newdf.get('boll')
        newdf['boll_ub'] = newdf.get('boll_ub')
        CurrentDf = newdf[['time','price','boll_lb','median','boll_ub']].tail(1)
        BMin = CurrentDf['boll_lb'].iloc[0]
        if(BMin > Decimal(CurrentPrice)):
            return True
        else:
            return False

    #Checks if the current price is above the upper bollinger band
    def BollingerUpperCheck(newdf, CurrentPrice):
        newdf['boll_lb'] = newdf.get('boll_lb')
        newdf['median'] = newdf.get('boll')
        newdf['boll_ub'] = newdf.get('boll_ub')
        CurrentDf = newdf[['time','price','boll_lb','median','boll_ub']].tail(1)
        BUpper = CurrentDf['boll_ub'].iloc[0]
        if(Decimal(CurrentPrice) > BUpper):
            return True
        else:
            return False

    #MACD = Moving Average Convergence Divergence
    #Checks if the MACD indicator has crossed -> signaling a transition from a bear market
    #to a bull market
    def MACDCrossCheck(df, CurrentPrice):
        df['signaldata'] = df.get('macds')
        newdf = df[['time','signaldata','macd']]
        newdf = newdf.tail(2)
        MACD = Decimal(newdf['macd'].iloc[1])
        SignalData = Decimal(newdf['signaldata'].iloc[1])
        PrevSignalData = Decimal(newdf['signaldata'].iloc[0])
        PrevMACD = Decimal(newdf['macd'].iloc[0])
        #Checking if there's a crossover
        if(MACD > SignalData and PrevSignalData > PrevMACD):
            return True
        else:
            return False

    #Checks if the Simple moving average is in a bear position or bull position
    def SMACheck(df):
        df.get('dma')
        CurrentDf = df[['time','price','close_10_sma','close_50_sma', 'dma']]
        #print(CurrentDf)
        CurrentDf = CurrentDf.tail(1)
        close_10 = CurrentDf['close_10_sma'].iloc[0]
        close_50 = CurrentDf['close_50_sma'].iloc[0]
        if(close_10 > close_50):
            return False
        else:
            return True

    #Checks if the MACD reflects a bull state or bear state
    def MACDAboveCheck(df,CurrentPrice):
        df['signaldata'] = df.get('macds')
        newdf = df[['time','signaldata','macd']]
        newdf = newdf.tail(1)
        MACD = Decimal(newdf['macd'].iloc[0])
        SignalData = Decimal(newdf['signaldata'].iloc[0])
        if(MACD > SignalData):
            return True
        else:
            return False

    #Calculates the difference between the MACD and Signal Data -> the More + the better the buy
    #vice versa, the more negative the higher tendency for the asset to decrease in value
    def MACDDifference(df):
        df['signaldata'] = df.get('macds')
        newdf = df[['time','signaldata','macd']]
        newdf = newdf.tail(1)
        MACD = Decimal(newdf['macd'].iloc[0])
        SignalData = Decimal(newdf['signaldata'].iloc[0])
        Difference = MACD - SignalData
        return Difference

    #Trix = Triple smoothed moving average; less susceptible to random changes in market values
    #Trix value increasing signals a very good buy signal
    def TrixIncreasing(df):
        df.get('trix')
        df = df['trix']
        df = df.tail(3)
        TrixNow = df.iloc[2]
        TrixBefore = df.iloc[1]
        TrixFirst = df.iloc[0]
        if(TrixNow > TrixBefore > TrixFirst):
            return True
        else:
            return False

    #Trix value decreasing signals a very strong sell signal
    def TrixDecreasing(df):
        df.get('trix')
        df = df['trix']
        df = df.tail(3)
        TrixNow = df.iloc[2]
        TrixBefore = df.iloc[1]
        TrixFirst = df.iloc[0]
        if(TrixNow < TrixBefore < TrixFirst):
            return True
        else:
            return False

    #Checks if simple moving average is increasing
    #SMA increasing is a buy signal, but happens too often to be reliable
    def SMAIncreasing(df):
        df.get('dma')
        CurrentDf = df['dma']
        CurrentDf = CurrentDf.tail(3)
        SMANow = CurrentDf.iloc[2]
        SMABefore = CurrentDf.iloc[1]
        SMAFirst = CurrentDf.iloc[0]
        if(SMANow > SMABefore > SMAFirst):
            return True
        else:
            return False

    #gets current Trix Value
    #Positive Trix Value is seen by some as a potential buy signal
    def GetTrix(df):
        df.get('trix')
        df = df['trix']
        df = df.tail(1)
        Trix = df.iloc[0]
        return Trix
        
    #checks if the current price is a high or not
    #Prices that are at a current high are often not a good buy
    def CurrentHigh(df, CurrentPrice):
        df = df[['price']]
        df = df.tail(2)
        CurrentPrice = Decimal(CurrentPrice)
        PriceBefore = Decimal(df['price'].iloc[1])
        PriceEarlier = Decimal(df['price'].iloc[0])
        if(CurrentPrice > PriceBefore > PriceEarlier):
            return True
        else:
            return False



#Buy order/sell order functions
#when the criteria are met these simulation trades are engaged
class Actions:
    def InitiateBuy(value, balance, amount):
        print("Ideal Buy Conditions met, initiating simulation buy")
        secondAsset = balance/(value*amount)
        return secondAsset
    
    def InitiateSell(value, balance, amount):
        print("Ideal Sell conditions met, initiating simulation sell")
        firstAsset = amount * value
        return firstAsset

