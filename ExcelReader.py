import pandas as pd

class ExcelReader():

    def __init__(self):
        self.dataframe = pd.DataFrame([])
        
    def get_dataframe(self):
        return self.dataframe

    def read_file_to_dataframe(self, path:str):
        dataframe = pd.read_excel(path, index_col=1)
        self.dataframe = dataframe
        return dataframe
    
er =  ExcelReader()


with open('filepaths.txt', 'r') as file:
    path = file.read().replace('\n', '')
    
data = er.read_file_to_dataframe(path)
