from time import time
import datetime as datetime
import pandas as pd
import os
from modules.Collect_Data import collect_data
from modules.Build_Dataframe.build_dataframe import build_dataframe
from modules.Build_Filter.build_filter import build_filter
from utils import csv_handle_functions

list_companies_file_path = "D:/0.Stock_Data/1.Danh_sach_ma_chung_khoan.xlsx"
raw_datafolder_path = "D:/0.Stock_Data/0.VNStocks_Historical_Data_From_2000"
build_dataframe_result_path = "D:/5.Stocks_Code/My_Project/data/builded_dataframe"
filtered_dataframe_result_path = "D:/5.Stocks_Code/My_Project/data/filtered_dataframe"

#---------------------------------------------------
#---------------------FUNCTION----------------------
#---------------------------------------------------
def get_conditions_string(_condition_list_name: str, _condition_list: dict()):
    conditions_string = ''

    for idx, key in enumerate(_condition_list):
        if len(_condition_list) == 1:
            conditions_string = key + ' == ' + '@' + _condition_list_name + '[' + "'" + key + "'"+ ']'
        else:
            if idx == len(_condition_list) - 1:
                conditions_string += key + ' == ' + '@' + _condition_list_name + '[' + "'" + key + "'"+ ']'
            else:
                conditions_string += key + ' == ' + '@' + _condition_list_name + '[' + "'" + key + "'"+ ']' + ' and '

    return conditions_string

def build_fold_name(_list):
    return '_'.join([item for item in _list])
#---------------------------------------------------
#------------------MAIN FUNCTION--------------------
#---------------------------------------------------
def main():
    t_start = time()

    signal_list = ["c.MorningStar"]
    filter_list = ["MorningStar"]
    # Điều kiện lọc dataset cho nhóm ngân hàng tài chính
    dataset_conditions = {
        'comGroupCode': ['HOSE', 'HNX'],
        'comTypeCode': ['NH', 'CK']
    }

    conditions_string = get_conditions_string('dataset_conditions', dataset_conditions)
    list_companies = pd.read_excel(list_companies_file_path)
    dataset_df = list_companies.query(conditions_string)

    #Định nghĩa Dataframe kết quả tổng
    column_names  = ['Ticker', '+/- T+5', '+/- T+10', '+/- T+30', '+/- T+120', '+/- T+180']
    column_types  = ['string', 'string', 'string', 'string', 'string', 'string']
    data_types = {column_names[i]: column_types[i] for i in range(len(column_names))}

    result_df = pd.DataFrame(columns=data_types.keys()).astype(data_types)

    #Create Folder for Result
    builded_fold_name = build_fold_name(signal_list)
    filtered_fold_name = build_fold_name(filter_list)
    
    for item in dataset_df['ticker']:
        file_path = os.path.join(raw_datafolder_path, item + '.csv')
        raw_df = pd.read_csv(file_path)
        builded_df = build_dataframe(raw_df, signal_list).getResult()
        csv_handle_functions.save_to_csv(builded_df, build_dataframe_result_path, item)
        filtered_df = build_filter(builded_df, filter_list).getResult()
        csv_handle_functions.save_to_csv(filtered_df, filtered_dataframe_result_path, item)

        if filtered_df.empty:
            append_data = {
                'Ticker': item,
                'MatchCount': 0,
                '+/- T+5': 'None',
                '+/- T+10': 'None',
                '+/- T+30': 'None',
                '+/- T+120': 'None',
                '+/- T+180': 'None'
            }
        else:
            append_data = {
                'Ticker': item,
                'MatchCount': int(len(filtered_df)),
                '+/- T+5': f"{round((len(filtered_df[filtered_df['+/- T+5'] > 0])/len(filtered_df[filtered_df['+/- T+5'].notnull()])*100), 3)} %",
                '+/- T+10': f"{round((len(filtered_df[filtered_df['+/- T+10'] > 0])/len(filtered_df[filtered_df['+/- T+10'].notnull()])*100), 3)} %",
                '+/- T+30': f"{round((len(filtered_df[filtered_df['+/- T+30'] > 0])/len(filtered_df[filtered_df['+/- T+30'].notnull()])*100), 3)} %",
                '+/- T+120': round((len(filtered_df[filtered_df['+/- T+120'] > 0])/len(filtered_df[filtered_df['+/- T+120'].notnull()])*100), 3) if len(filtered_df[filtered_df['+/- T+120'].notnull()]) !=0 else "None",
                '+/- T+180': round((len(filtered_df[filtered_df['+/- T+180'] > 0])/len(filtered_df[filtered_df['+/- T+180'].notnull()])*100), 3) if len(filtered_df[filtered_df['+/- T+180'].notnull()]) !=0 else "None",
            }
        result_df = pd.concat([result_df, pd.DataFrame([append_data])], ignore_index=True)

    csv_handle_functions.save_to_csv(result_df, filtered_dataframe_result_path, 'Thống_kê_xác_suất_lãi_theo_T+_MorningStar')

    t_end = time()
    print(f'Success! Process took %.3f second' % (t_end - t_start) )

if __name__ == "__main__":
    main()