from Indicator.patterns.indicator_finder import IndicatorFinder
import talib as ta
class Stochrsi(IndicatorFinder):
    def __init__(self, target=None):
        super().__init__(self.get_class_name(), 14, target=target)

    def logic(self):
        rsi = ta.RSI(self.data[self.close_column], timeperiod=14)
        highest_rsi = rsi.rolling(14).max()
        lowest_rsi = rsi.rolling(14).min()
        self.data[self.target] = (rsi - lowest_rsi)/(highest_rsi-lowest_rsi)*100
        self.data['%K_StochRSI'] = self.data[self.target].rolling(3).mean()
        self.data['%D_StochRSI'] = self.data['%K_StochRSI'].rolling(3).mean()