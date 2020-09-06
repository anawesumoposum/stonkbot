from pyalgotrade import strategy
from pyalgotrade.barfeed import quandlfeed

class CheatCodes(strategy.BacktestingStrategy):
    def __init__(self, feed, instrument):
        super(CheatCodes, self).__init__(feed)
        self.__instrument = instrument

    def onBars(self, bars):
        bar = bars[self.__instrument]
        self.info(bar.getClose())

feed = quandlfeed.Feed()
feed.addBarsFromCSV("orcl", "WIKI-ORCL-2015-quandl.csv")

# Evaluate the strategy with the feed's bars.
strat = CheatCodes(feed, "orcl")
strat.run()