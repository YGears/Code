import pandas as pd
import re

class ExcelReader():

    def __init__(self):
        self.dataframe = pd.DataFrame([])
        self.unique_vendors:list = []    


    def get_dataframe(self):
        return self.dataframe


    def read_file_to_dataframe(self, path:str) -> None:
        dataframe = pd.read_excel(path, index_col='Rentedatum')
        self.dataframe = dataframe
    

    def get_vendor(self):
        # get every row starting with a card payment
        data = self.dataframe[self.dataframe['Omschrijving'].str.startswith('BEA, Betaalpas')]['Omschrijving']
        vendor_column = data.apply(self.split_str_column)
        self.dataframe['Vendor'] = data.apply(self.split_str_column)


    def get_duplicate_index(self):
        df = self.dataframe
        return df[df.index.duplicated()] 


    def add_id_index(self) -> None:
        self.dataframe['id'] =  self.dataframe.reset_index().index
        self.dataframe.set_index('id', inplace=True)


    def print_n_rows(self, data:pd.DataFrame, amount:int = 1):
        l = data.head(amount).squeeze().tolist()
        [print(f"{item} \n") for item in l]
    

    def split_str_on_whitespace(self, row:str, spaces:int = 2):
        return re.split(r'\s{'+str(spaces)+',}', row)
    

    def split_str_column(self, row:str):
        # split row on whitespace if more than 2 characters
        row_split_on_whitespace = self.split_str_on_whitespace(row=row, spaces=3)

        # get pair with vendor and split off ,
        vendor = row_split_on_whitespace[1].split(',')[0]

        # some contain a prefix with *, which will be removed
        if '*' in vendor:
            vendor = vendor.split('*')[1]

        # check if vendor in self.unique vendors, add if not    
        if vendor not in self.unique_vendors:
            self.unique_vendors.append(vendor)
        return vendor
    
    def get_omschrijving_when_vendor_nan(self):
        df = self.dataframe
        res = df[df['Vendor'].isnull()]['Omschrijving']
        self.print_n_rows(res, 100)
        print(f'Rowcount: {res.count()}')

    def get_distinct_omschrijving_prefix(self):
        
        
        pass
    
er =  ExcelReader()


with open('filepaths.txt', 'r') as file:
    path = file.read().replace('\n', '')
    
er.read_file_to_dataframe(path)
er.add_id_index()
er.get_vendor()


# er.print_n_rows(20)

print(er.get_omschrijving_when_vendor_nan())