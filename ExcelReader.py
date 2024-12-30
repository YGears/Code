import pandas as pd

class ExcelReader():

    def __init__(self):
        self.dataframe = pd.DataFrame([])
        
    def get_dataframe(self):
        return self.dataframe

    def read_file_to_dataframe(self, path:str) -> None:
        dataframe = pd.read_excel(path, index_col='Rentedatum')
        self.dataframe = dataframe
    
    def get_vendor(self):
        data = self.dataframe['Omschrijving']
        data = data.head(3)
        vendor_column = data.apply(self.split_str_column)
        # print(vendor_column)
        print(data.iloc[0])
        x:str = data.iloc[0]
        # print(x.split(', '))
        print(x.split("    "))
        
        # print(vendor_column)
        

    def split_str_column(self, row):
        print(type(row))
        return row.split()

    
er =  ExcelReader()


with open('filepaths.txt', 'r') as file:
    path = file.read().replace('\n', '')
    
er.read_file_to_dataframe(path)
er.get_vendor()


# print(er.get_dataframe())

# print(er.get_dataframe()['Omschrijving'])


