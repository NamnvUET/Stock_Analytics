import os
import pandas as pd
import string

#Save dataframe to csv file
def save_to_csv(dataframe: pd.DataFrame, save_path: string, file_name: string):
    completedName = os.path.join(save_path, file_name) + '.csv'
    dataframe.to_csv(completedName, index=False)
    return 0