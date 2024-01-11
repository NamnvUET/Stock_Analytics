import os
import re
import importlib
import sys

__builders = dict()

# Lấy module_path để chuẩn bị import module động
def __get_module_path(class_name):
    res = re.findall('[A-Z][^A-Z]*', class_name)
    if 'Daily' in res:
        return 'daily.' + '_'.join([cur.lower() for cur in res])
    elif 'Intraday' in res:
        return 'intraday.' + '_'.join([cur.lower() for cur in res])

#Import module động bằng importlib
def __load_module(_module_path):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    if current_dir not in sys.path:
        sys.path.append(current_dir)
    try:
        module = importlib.import_module(_module_path)
        return module
    except ImportError as e:
        raise e

#Trả về class cần tìm theo tên truyền vào. Import động module nếu cần
def __get_class_by_name(class_name):
    module_path = __get_module_path(class_name)
    module_name = 'collect_data.' + module_path
    if module_name not in __builders:
        module = __load_module(module_path)
        __builders[module_name]  = module
    else:
        module = __builders[module_name]
    return getattr(module, class_name)

#Trả về object của class
def __create_object(class_name, arguments):
    return __get_class_by_name(class_name)(_arguments = arguments)


def daily_historical(_raw_datafolder_path: str, arguments: dict() = []):
    daily_his = __create_object('DailyHistorical', arguments)
    #Update all cổ phiếu trong folder path
    daily_his.all_stocks_update(_raw_datafolder_path)
    return 0
