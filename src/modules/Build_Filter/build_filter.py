import os
# import re
# import importlib
import sys
import pandas as pd
# from pandas.api.types import is_numeric_dtype
from modules.Build_Filter.patterns import patterns

class build_filter():
    # Contructor
    def __init__(self, _dataframe, _filter_list):
        self.__check_and_handle_arguments(_dataframe,_filter_list)

    #Return dataframe
    def getResult(self):
        result_df = self.__data
        for item in self.__filter_list:
            result_df = self.__call_function(result_df, item)
        return result_df

    def __call_function(self, _dataframe, _filter_name):
        result_df = getattr(patterns, _filter_name)(_dataframe)
        return result_df

    def __check_and_handle_arguments(self, _dataframe, _filter_list):
        if isinstance(_dataframe, pd.DataFrame):
            if isinstance(_filter_list, list):
                # if not set(_filter_list).issubset(_dataframe.columns):
                #     raise Exception('Filter list must be in Dataframe')
                self.__is_data_checked = True
                self.__data = _dataframe
                self.__filter_list = _filter_list
            else:
                raise Exception('Filter List must be List type')
        else:
            raise Exception('Data must be Panda Dataframe type')
        