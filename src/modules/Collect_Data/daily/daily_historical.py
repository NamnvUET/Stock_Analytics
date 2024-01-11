import datetime as datetime
import csv
from vnstock import *
import os

class DailyHistorical():
    def __init__(self, _arguments: dict() = []):
        #Today
        self.today_formated = datetime.today().strftime('%Y-%m-%d')
        self.arguments = _arguments

    #Update Data that exist in excel file Function
    def specify_stock_update(self, csv_file_path: str, stock_name: str):
        with open(csv_file_path, 'a+', newline='') as file:
            # Kiểm tra vị trí hiện tại con trỏ của tệp.
            # Nếu con trỏ đang không ở đầu tệp thì chuyển nó về đầu tệp để đọc dữ liệu đã có.
            if file.tell() != 0:
                file.seek(0)
            #Đọc vào dữ liệu đã có. Lấy ngày cuối cùng đã có dữ liệu ở dòng cuối cùng của tệp.
            reader = csv.reader(file)
            rows = list(reader)
            last_date = rows[-1][0]
            try:
                last_date_convert_datetime = datetime.strptime(last_date, '%Y-%m-%d')
            except:
                last_date_convert_datetime = datetime.strptime(last_date, '%m/%d/%Y')
            next_date = last_date_convert_datetime + timedelta(days=1)
            next_date_formated = next_date.strftime('%Y-%m-%d')

            if next_date_formated == self.today_formated:
                print(f"Mã {stock_name} đã được chạy cập nhật !")
            else:
                #Get new data to append file
                try:
                    append_data = stock_historical_data(stock_name, next_date_formated, self.today_formated, resolution='1D', type='stock')
                    if append_data.empty :
                        print(f"Mã {stock_name} từ ngày {next_date_formated} đến ngày {self.today_formated} không có giao dịch !")
                    else:
                        # Chuyển DataFrame thành danh sách các hàng
                        rows_to_append = append_data.values.tolist()
                        #Append data to file and save
                        writer = csv.writer(file)
                        writer.writerows(rows_to_append)
                except:
                    print (f"Lấy dữ liệu của mã {stock_name} từ ngày {next_date_formated} đến ngày {self.today_formated} thất bại !")
        return 0
    
    def all_stocks_update(self, dataFolder_path):
        for filename in os.listdir(dataFolder_path):
            extract_name= filename.split('.csv')[0]
            full_path = os.path.join(dataFolder_path, filename)
            print(f'Cập nhật dữ liệu của mã {extract_name}')
            self.specify_stock_update(csv_file_path=full_path, stock_name=extract_name)
        return 0
