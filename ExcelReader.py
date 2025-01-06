import pandas as pd
import re

class ExcelReader():

    def __init__(self, path:str):

        #init empty global variables
        self.dataframe = pd.DataFrame([])
        self.unique_vendors:list = []


        self.read_file_to_dataframe(path)
        self.add_id_as_index()

        #check if index has been changed correctly and is thus unique
        assert(self.check_index_unique())


    def read_file_to_dataframe(self, path:str) -> None:
        dataframe = pd.read_excel(path, index_col='Rentedatum')
        self.dataframe = dataframe


    def add_id_as_index(self) -> None:
        self.dataframe['id'] =  self.dataframe.reset_index().index
        self.dataframe.set_index('id', inplace=True)
    

    def check_index_unique(self) -> bool:
        df = self.dataframe
        return df[df.index.duplicated()].empty 

    
    def get_dataframe(self):
        return self.dataframe
    

    def print_n_rows_of_column(self, data:pd.DataFrame=None, column_name:str='Omschrijving', rowcount:int = 1):

        if data == None:
            data = self.get_dataframe()[column_name]

        l = data.head(rowcount).squeeze().tolist()
        [print(f"{item} \n") for item in l]
            

    def split_str_on_whitespace(self, row:str, spaces:int = 2):
        return re.split(r'\s{'+str(spaces)+',}', row)

    def get_index_of_list(self, row:str, index:int=0):
        return row[index]
    
    def get_temp_splitted_omschrijving_column(self):
        df = self.dataframe
        df['temp_splitted_omschrijving'] = df['Omschrijving'].apply(self.split_str_on_whitespace)

    def get_paymenttype_column(self):
        df = self.dataframe

        # df['PaymentType'] = df['Omschrijving'].apply(self.split_str_on_whitespace).apply(self.get_index_of_list, args=(0,))

        df['PaymentType'] = df['temp_splitted_omschrijving'].apply(self.get_index_of_list, args=(0,))

        print(df.groupby(['PaymentType'], as_index=False)['PaymentType'].value_counts().sort_values('count').to_string())

    def get_vendor_on_paymentmethod(self, row:pd.Series):
    
        payment_method:str = row['PaymentType']

        match payment_method:
            
            case "BEA, Betaalpas":
                self.dataframe['Vendor'] = self.dataframe['temp_splitted_omschrijving'].apply(self.get_vendor_with_prefix_BEA_betaalpas)
                return 
            
            case "SEPA Overboeking":
                return
            
            case "SEPA iDEAL":
                return
            
            #wildcard on all SEPA Incasso algemeen doorlopend
            case ['SEPA Incasso algemeen doorlopend', *_]:
                return

        


        
        pass

    def get_vendor_with_prefix_BEA_betaalpas(self):
        pass
    
    def get_vendor_with_prefix_SEPA_Overboeking(self):
        pass

    def get_vendor_with_prefix_SEPA_iDEAL(self):
        pass

    def get_vendor_with_prefix_SEPA_Icasso_algemeen_doorlopend(self):
        pass


    def get_vendor(self):
        # get every row starting with a card payment
        data = self.dataframe[self.dataframe['Omschrijving'].str.startswith('BEA, Betaalpas')]['Omschrijving']
        vendor_column = data.apply(self.split_str_column)
        self.dataframe['Vendor'] = data.apply(self.split_str_column)


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
    
    def get_unparsed_vendors(self):
        df = self.dataframe
        res = df[df['Vendor'].isnull()]['Omschrijving']
        self.print_n_rows_of_column(res, 100)
        print(f'Rowcount: {res.count()}')


    def clean_omschrijving(self):
        self.dataframe['Omschrijving'] = self.dataframe['Omschrijving'].apply(lambda x : ",".join(re.split(r'\s{'+str(3)+',}', x)))

    def run(self):
        er.get_temp_splitted_omschrijving_column()
        er.get_paymenttype_column()

        



with open('filepaths.txt', 'r') as file:
    path = file.read().replace('\n', '')

er =  ExcelReader(path)




df = er.get_dataframe()
# er.clean_omschrijving()

# df = df[df['Omschrijving'].str.startswith('BEA, Betaalpas')]
# df = df[df['Omschrijving'].str.startswith('SEPA Overboeking')]
# df = df[df['Omschrijving'].str.startswith('SEPA Incasso algemeen doorlopend Incassant: NL03ZZZ301243580000')]
# print(df.head(10).to_string(justify='left').replace('\n', '\n\n'))

# print(er.get_omschrijving_when_vendor_nan())


er.run()