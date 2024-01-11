import pandas as pd
    
def MorningStar(_dataframe: pd.DataFrame):
    result_df = _dataframe[_dataframe['MorningStar'] == True]
    return result_df
    
def Stochrsi(_dataframe: pd.DataFrame):
    dataframe = _dataframe[
                    (_dataframe['Stochrsi'] < 80) & (_dataframe['%K_StochRSI'] > 20) & 
                    (_dataframe['%K_StochRSI'] > _dataframe['%D_StochRSI']) & 
                    (_dataframe['%K_StochRSI'].shift(1) < _dataframe['%D_StochRSI'].shift(1))]
    return dataframe

def Ema(_dataframe: pd.DataFrame):
    dataframe = _dataframe[(_dataframe['Ema50'] > _dataframe['Ema200']) &
                           (_dataframe['Ema50'].shift(1) < _dataframe['Ema200'].shift(1))]
    return dataframe