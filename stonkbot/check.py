from __future__ import print_function

from pyalgotrade import strategy
from pyalgotrade import plotter
from pyalgotrade.barfeed import quandlfeed
from pyalgotrade.technical import rsi
from pyalgotrade.technical import bollinger
from pyalgotrade.stratanalyzer import sharpe
from pyalgotrade import broker as basebroker


class BBands(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument, bBandsPeriod, overBoughtThreshold, overSoldThreshold):
        super(BBands, self).__init__(feed)
        self.__instrument = instrument
        self.__bbands = bollinger.BollingerBands(feed[instrument].getCloseDataSeries(), bBandsPeriod, 2)
        self.__rsi = rsi.RSI(feed[instrument].getCloseDataSeries(), 14)
        self.overBoughtThreshold = overBoughtThreshold
        self.overSoldThreshold = overSoldThreshold

    def getRSI(self):
        return self.__rsi

    def getBollingerBands(self):
        return self.__bbands

    def onOrderUpdated(self, order):
        if order.isBuy():
            orderType = "Buy"
        else:
            orderType = "Sell"
        self.info("%s order %d updated - Status: %s" % (
            orderType, order.getId(), basebroker.Order.State.toString(order.getState())
        ))

    def onBars(self, bars):
        lower = self.__bbands.getLowerBand()[-1]
        upper = self.__bbands.getUpperBand()[-1]
        mid = self.__bbands.getMiddleBand()[-1]
        if lower is None:
            return
        rsi = self.getRSI()[-1]

        temp = (upper - mid) / 2
        hup = upper - temp
        temp = (mid - lower) / 2
        hlow = lower + temp
        temp = (upper - mid) / 4
        qup = upper - temp
        temp = (mid - lower) / 4
        qlow = lower + temp

        shares = self.getBroker().getShares(self.__instrument)
        bar = bars[self.__instrument]
        if shares == 0 and bar.getClose() < hlow and rsi < 30: #great rsi, good bbands
            sharesToBuy = (int(self.getBroker().getCash(False) - 50) / bar.getClose())
            self.info("Placing buy market order for %s shares" % sharesToBuy)
            self.marketOrder(self.__instrument, sharesToBuy)
        elif shares > 0 and bar.getClose() > hup and rsi > 70:
            self.info("Placing sell market order for %s shares" % shares)
            self.marketOrder(self.__instrument, -1*shares)
        elif shares == 0 and bar.getClose() < qlow and rsi < 35:
            sharesToBuy = (int(self.getBroker().getCash(False) - 50) / bar.getClose())
            self.info("Placing buy market order for %s shares" % sharesToBuy)
            self.marketOrder(self.__instrument, sharesToBuy)
        elif shares > 0 and bar.getClose() > qup and rsi > 65: #not sure that I need this case
            self.info("Placing sell market order for %s shares" % shares)
            self.marketOrder(self.__instrument, -1*shares)
        


def main(plot):
    instrument = "AMD" #"orcl" 
    bBandsPeriod = 40
    overBoughtThreshold = 70
    overSoldThreshold = 30

    # Download the bars.
    feed = quandlfeed.Feed()
    feed.addBarsFromCSV("AMD", "WIKI-AMD-2016-quandl.csv")

    strat = BBands(feed, instrument, bBandsPeriod, overBoughtThreshold, overSoldThreshold)
    strat.getBroker().setCash(1000)
    sharpeRatioAnalyzer = sharpe.SharpeRatio()
    strat.attachAnalyzer(sharpeRatioAnalyzer)
    start = strat.getBroker().getEquity()

    if plot:
        plt = plotter.StrategyPlotter(strat, True, True, True)
        plt.getInstrumentSubplot(instrument).addDataSeries("upper", strat.getBollingerBands().getUpperBand())
        plt.getInstrumentSubplot(instrument).addDataSeries("middle", strat.getBollingerBands().getMiddleBand())
        plt.getInstrumentSubplot(instrument).addDataSeries("lower", strat.getBollingerBands().getLowerBand())
        plt.getOrCreateSubplot("rsi").addDataSeries("RSI", strat.getRSI())
        plt.getOrCreateSubplot("rsi").addLine("Overbought", overBoughtThreshold)
        plt.getOrCreateSubplot("rsi").addLine("Oversold", overSoldThreshold)

    strat.run()
    print("Sharpe ratio: %.2f" % sharpeRatioAnalyzer.getSharpeRatio(0.05))

    final = strat.getBroker().getEquity()
    print("Net: "+str(final-start))

    if plot:
        plt.plot()

if __name__ == "__main__":
    main(True)