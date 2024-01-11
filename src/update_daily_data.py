from time import time
import datetime as datetime
import pandas as pd
import os
from modules.Collect_Data import collect_data

list_companies_file_path = "D:/0.Stock_Data/1.Danh_sach_ma_chung_khoan.xlsx"
raw_datafolder_path = "D:/0.Stock_Data/0.VNStocks_Historical_Data_From_2000"
build_dataframe_result_path = "D:/5.Stocks_Code/My_Project/data/builded_dataframe"
filtered_dataframe_result_path = "D:/5.Stocks_Code/My_Project/data/filtered_dataframe"

#---------------------------------------------------
#------------------MAIN FUNCTION--------------------
#---------------------------------------------------
def main():
    t_start = time()
    collect_data.daily_historical(raw_datafolder_path)
    t_end = time()
    print(f'Success! Process took %.3f second' % (t_end - t_start) )

if __name__ == "__main__":
    main()