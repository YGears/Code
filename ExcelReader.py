import pandas as pd

class ExcelReader():
        
    def read_file_to_dataframe(self, path:str):
        data = pd.read_excel(path, index_col=0 )
        return data

er =  ExcelReader()


path = "C:/Users/Youri/Desktop/Data/XLS240610232047.xlsx"
er.read_file_to_dataframe(path)