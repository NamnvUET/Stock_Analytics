from Indicator.patterns.indicator_finder import IndicatorFinder
import talib as ta
class Rsi(IndicatorFinder):
    def __init__(self, target=None):
        super().__init__(self.get_class_name(), 14, target=target)

    def logic(self):
        self.data[self.target] = ta.RSI(self.data[self.close_column], timeperiod=14)
