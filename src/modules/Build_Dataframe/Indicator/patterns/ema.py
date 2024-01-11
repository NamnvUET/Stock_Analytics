from Indicator.patterns.indicator_finder import IndicatorFinder
import talib as ta
class Ema(IndicatorFinder):
    def __init__(self, target=None):
        super().__init__(self.get_class_name(), 50, target=target)

    def logic(self):
        self.data['Ema20'] = ta.EMA(self.data[self.close_column], timeperiod=20)
        self.data['Ema50'] = ta.EMA(self.data[self.close_column], timeperiod=50)
        self.data['Ema200'] = ta.EMA(self.data[self.close_column], timeperiod=200)
        