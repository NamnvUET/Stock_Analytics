Cách dùng:

Cập nhật toàn bộ daily historical data:
    collect_data.daily_historical()

Build Dataframe với list các tín hiệu giao dịch:
    <Tham số đầu vào cần: list các tín hiệu giao dịch + dataframe dữ liệu của cổ phiếu>
    signal_list = ["i.Stochrsi", "c.MorningStar", "c.Hammer", "i.Rsi"]
    return build_dataframe(data_dataframe, signal_list).getResult()
    
Filter Dataframe với list các điều kiện filter:
    <Tham số đầu vào cần: list các điều kiện filter + dataframe chứa dữ liệu đã build các điều kiện của cổ phiếu>    
    filter_list = ["Stochrsi"]
    return build_filter(temp_df, filter_list).getResult()