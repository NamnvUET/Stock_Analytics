import os
import re
import importlib
import sys
import pandas as pd
from pandas.api.types import is_numeric_dtype

class build_dataframe():
    # Contructor
    def __init__(self, _dataframe, _signal_list, _ohlc = ['open', 'high', 'low', 'close']):
        self.__check_and_handle_arguments(_dataframe,_signal_list,_ohlc)
        self.__signal_list_imported = dict()
        self.__load_modules_by_name(self.__signal_list)
        
    #Regex function to convert classname to filename
    def __get_file_name(self, class_name):
        res = re.findall('[A-Z][^A-Z]*', class_name)
        return '_'.join([cur.lower() for cur in res])

    #Load modules need by modules name
    def __load_modules_by_name(self, modules_array):
        # Import path of current file into sys.path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.append(current_dir)

        for item in modules_array:
            marker, module_name = item.split('.')
            if item not in self.__signal_list_imported:
                # If it is candlestick module
                if marker == 'c':
                    file_name = self.__get_file_name(module_name)
                    module_path = 'Candlestick.patterns.' + file_name
                # If it is indicator module
                elif marker == 'i':
                    file_name = module_name.lower()
                    module_path = 'Indicator.patterns.' + file_name
                #Import module by importlib
                try:
                    module = importlib.import_module(module_path)
                    self.__signal_list_imported[item] = module
                except ImportError as e:
                    print(f"Lỗi khi import module {item}")
                    raise e

    #Return dataframe
    def getResult(self):
        result_df = self.__emulator_profit_and_loss()
        for item in self.__signal_list_imported:
            marker, module_name = item.split('.')
            result_df = self.__call_module(marker, result_df, module_name)
        return result_df

    #Call module to calculate signal
    def __call_module(self, _maker, _dataframe: pd.DataFrame, _module_name: str):
        module_name_in_list = f"{_maker}.{_module_name}"
        obj = getattr(self.__signal_list_imported[module_name_in_list], _module_name)()
        return obj.has_pattern(candles_df=_dataframe, ohlc=self.__default_ohlc, is_reversed = False)
    
    def __emulator_profit_and_loss(self):
        result_df = self.__data.copy()
        result_df['price_day(T)'] =  result_df[self.__open_column].shift(-1)
        result_df['T+5'] =   result_df[self.__low_column].shift(-6)
        result_df['T+10'] =  result_df[self.__low_column].shift(-11)
        result_df['T+30'] =  result_df[self.__low_column].shift(-31)
        result_df['T+120'] = result_df[self.__low_column].shift(-121)
        result_df['T+180'] = result_df[self.__low_column].shift(-181)
        result_df['+/- T+5'] = ((result_df['T+5'] - result_df['price_day(T)'])/result_df['price_day(T)'])*100
        result_df['+/- T+10'] = ((result_df['T+10'] - result_df['price_day(T)'])/result_df['price_day(T)'])*100
        result_df['+/- T+30'] = ((result_df['T+30'] - result_df['price_day(T)'])/result_df['price_day(T)'])*100
        result_df['+/- T+120'] = ((result_df['T+120'] - result_df['price_day(T)'])/result_df['price_day(T)'])*100
        result_df['+/- T+180'] = ((result_df['T+180'] - result_df['price_day(T)'])/result_df['price_day(T)'])*100

        return result_df
    #Validate arguments pass for class
    def __check_and_handle_arguments(self, _dataframe, _signal_list, _ohlc):

        if isinstance(_dataframe, pd.DataFrame):
            if _ohlc and len(_ohlc) == 4:
                if not set(_ohlc).issubset(_dataframe.columns):
                    raise Exception('Provided columns does not exist in given dataframe')
                self.__default_ohlc = _ohlc
                self.__open_column = _ohlc[0]
                self.__high_column = _ohlc[1]
                self.__low_column = _ohlc[2]
                self.__close_column = _ohlc[3]
            else:
                raise Exception('Provide list of four elements indicating columns in strings. '
                                'Default: [open, high, low, close]')

            self.__data = _dataframe.copy()

            if not is_numeric_dtype(self.__data[self.__close_column]):
                self.__data[self.__close_column] = pd.to_numeric(self.__data[self.__close_column])

            if not is_numeric_dtype(self.__data[self.__open_column]):
                self.__data[self.__open_column] = pd.to_numeric(self.__data[self.__open_column])

            if not is_numeric_dtype(self.__data[self.__low_column]):
                self.__data[self.__low_column] = pd.to_numeric(self.__data[self.__low_column])

            if not is_numeric_dtype(self.__data[self.__high_column]):
                self.__data[self.__high_column] = pd.to_numeric(self.__data[self.__high_column])

            self.__is_data_checked = True
        else:
            raise Exception('Data must be Panda Dataframe type')
        
        if isinstance(_signal_list, list):
            self.__signal_list = _signal_list
        else:
            raise Exception('Signal List must be List type')

