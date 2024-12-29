import pandas as pd

class ExcelReader():
        
    def read_file_to_dataframe(self, path:str):
        data = pd.read_excel(path, index_col=0 )
        return data

er =  ExcelReader()


with open('filepaths.txt', 'r') as file:
    path = file.read().replace('\n', '')
    
data = er.read_file_to_dataframe(path)
print(data)