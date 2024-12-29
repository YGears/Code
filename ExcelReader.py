import pandas as pd

class ExcelReader():

    def __init__(self):
        self.dataframe = pd.DataFrame([])
        
    def get_dataframe(self):
        return self.dataframe

    def read_file_to_dataframe(self, path:str):
        dataframe = pd.read_excel(path, index_col='Rentedatum')
        self.dataframe = dataframe
        return dataframe
    
    def get_vendor(self):
        data = self.dataframe['Omschrijving']
        vendor_column = data.apply(str.split)
        print(vendor_column)

    def split_str_column(self, row):
        return row.split()

    
er =  ExcelReader()


with open('filepaths.txt', 'r') as file:
    path = file.read().replace('\n', '')
    
data = er.read_file_to_dataframe(path)
print(data)
er.get_vendor()


