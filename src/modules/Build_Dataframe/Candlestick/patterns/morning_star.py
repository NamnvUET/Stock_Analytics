from Candlestick.patterns.candlestick_finder import CandlestickFinder

class MorningStar(CandlestickFinder):
    def __init__(self, target=None):
        super().__init__(self.get_class_name(), 3, target=target)

    def logic(self, idx):
        candle = self.data.iloc[idx]
        prev_candle = self.data.iloc[idx + 1 * self.multi_coeff]
        b_prev_candle = self.data.iloc[idx + 2 * self.multi_coeff]

        close = candle[self.close_column]
        open = candle[self.open_column]
        high = candle[self.high_column]
        low = candle[self.low_column]

        prev_close = prev_candle[self.close_column]
        prev_open = prev_candle[self.open_column]
        prev_high = prev_candle[self.high_column]
        prev_low = prev_candle[self.low_column]

        b_prev_close = b_prev_candle[self.close_column]
        b_prev_open = b_prev_candle[self.open_column]
        b_prev_high = b_prev_candle[self.high_column]
        b_prev_low = b_prev_candle[self.low_column]

        if (b_prev_open > b_prev_close) and (close > open):
            body_b_prev_candle = (b_prev_open - b_prev_close) / (b_prev_high - b_prev_low)
            # body_prev_candle = (abs(prev_close - prev_open)) / (prev_high - prev_low)
            body_candle = (close-open) / (high-low)

            condition1 = body_b_prev_candle >= 0.7
            # condition2 = ((prev_high-prev_low) < (b_prev_open-b_prev_low)*0.15)
            condition3 = (body_candle >= body_b_prev_candle/2) and (close > (b_prev_high-b_prev_low)/2)

            return (condition1 and condition3)
        else:
            return False