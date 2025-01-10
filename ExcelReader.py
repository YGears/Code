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
            

    def split_str_on_whitespace(self, row:str, spaces:int = 2):
        return re.split(r'\s{'+str(spaces)+',}', row)

    def get_index_of_list(self, row:str, index:int=0):
        return row[index]
    
    def get_temp_splitted_omschrijving_column(self):
        """
        Creates temporary column temp_splitted_omschrijving

        Omschrijving by default is a list of ambiguous items with a schema that differs per payment method
        The items are splitted on whitespace, with distance a variable to keep matching columns
        This function splits the items on this whitespace and returns it a a new column with a list

        Although a bad practice for production, it is a great asset when peforming transformations with a dynamic list.
        We can extract information on a use-case basis and have common denominators as new columns
        Ex. payment_method and vendor, key columns when presenting data to the GUI.
        """    
        df = self.dataframe
        df['temp_splitted_omschrijving'] = df['Omschrijving'].apply(self.split_str_on_whitespace, args=(2,))

    def get_paymenttype_column(self):
        df = self.dataframe

        # df['PaymentType'] = df['Omschrijving'].apply(self.split_str_on_whitespace).apply(self.get_index_of_list, args=(0,))

        self.dataframe['PaymentType'] = df['temp_splitted_omschrijving'].apply(self.get_index_of_list, args=(0,))

        # print(df.groupby(['PaymentType'], as_index=False)['PaymentType'].value_counts().sort_values('count').to_string())

    def get_vendor_on_paymentmethod(self, row):
        payment_method:str = row['PaymentType']

        match payment_method:
            
            case "BEA, Betaalpas":
                vendor_with_cardnumber = row['temp_splitted_omschrijving'][1]
                vendor = vendor_with_cardnumber.split(',')[0]
                if '*' in vendor:
                    vendor = vendor.split('*')[1]

                return self.clean_string(vendor)
            
            case "BEA, Apple Pay":
                vendor_with_cardnumber = row['temp_splitted_omschrijving'][1]
                vendor = vendor_with_cardnumber.split(',')[0]
                if '*' in vendor:
                    vendor = vendor.split('*')[1]

            case "SEPA Overboeking":
                vendor_with_naam_prefix = row['temp_splitted_omschrijving'][3]
                vendor = vendor_with_naam_prefix.split(': ')[1]
            
                return self.clean_string(vendor)
            
            case "SEPA iDEAL":
                vendor_with_naam_prefix = row['temp_splitted_omschrijving'][3]
                vendor = vendor_with_naam_prefix.split(': ')[1]
            
                return self.clean_string(vendor)
            
            case "RENTE EN/OF KOSTEN":
                vendor = row['temp_splitted_omschrijving'][1]          
                
                return self.clean_string(vendor)
            
            #wildcard on all SEPA Incasso algemeen doorlopend
            case x if x.startswith('SEPA Incasso algemeen doorlopend'):
                vendor_with_naam_prefix = row['temp_splitted_omschrijving'][1]
                vendor = vendor_with_naam_prefix.split(': ')[1]                
                
                return self.clean_string(vendor)
            
            case x if x.startswith('/TRTP/'):
                splitted_cell:list = row['temp_splitted_omschrijving'][0].split('/')
                index_of_name = splitted_cell.index("NAME")+1
                return self.clean_string(splitted_cell[index_of_name])
            
            case "ABN AMRO Bank N.V.":
                return "Geldautomaat"
            
            case "GEA, Betaalpas":
                return "Geldautomaat Amerika"


            case _:
                print(f'Found else: {payment_method}')

    def clean_string(self, string_value) ->str:
       return str.upper(re.sub(r"[^a-zA-Z0-9]+", ' ', string_value)).strip()
    
    def get_unparsed_vendors(self):
        df = self.dataframe
        res = df[df['Vendor'].isnull()]['Omschrijving']
        print(res.head(100))
        print(f'Rowcount: {res.count()}')


    def clean_omschrijving(self):
        self.dataframe['Omschrijving'] = self.dataframe['Omschrijving'].apply(lambda x : ", ".join(re.split(r'\s{'+str(2)+',}', x)))
    
    def drop_temp_columns(self):
        self.dataframe.drop(columns=['temp_splitted_omschrijving'], inplace=True)

    def run(self):
        self.get_temp_splitted_omschrijving_column()
        self.get_paymenttype_column()
        
        self.dataframe['Vendor'] = self.dataframe.apply(self.get_vendor_on_paymentmethod, axis='columns')

        #drop temp columns
        self.drop_temp_columns()

    

        



with open('filepaths.txt', 'r') as file:
    path = file.read().replace('\n', '')

er =  ExcelReader(path)
er.run()

# print(er.get_dataframe()[er.get_dataframe()['Vendor'].isnull()]['PaymentType'].unique())
# # # print(er.dataframe.loc[er.dataframe['Vendor'].notnull()], ['Vendor'].count)
[print(f'{k:25}:{v}') for k, v in er.dataframe.groupby('Vendor')['Vendor'].count().sort_values().to_dict().items()]
# # # print(er.dataframe['Vendor'].unique())
# # print(er.get_dataframe()['Vendor'].nunique())
# print(er.get_dataframe())
# print(er.get_unparsed_vendors())

##Testing code to identify rows that start with a certain payment method
# df = er.get_dataframe()
# er.clean_omschrijving()
# df = df[df['Omschrijving'].str.startswith('')]
# print(df.head(10).to_string(justify='left').replace('\n', '\n\n'))


print(er.get_dataframe().head(100))
print("END")