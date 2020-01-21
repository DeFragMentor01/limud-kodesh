import xml.etree.cElementTree as ET
import os
import re
import configparser
import pyodbc
from hebrew_numbers import int_to_gematria

config = configparser.ConfigParser()
config.read(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'settings.ini'))

current_dir_path = config.get('XML','current_dir')
tanakh_dir_list = os.listdir(current_dir_path)
server = config.get("SQL", "server")
table_names = config.get("SQL", "table_names")
database_name = config.get("SQL", "database_name")
csv_file_name = config.get("CSV", "csv_file_name")

if os.path.exists(os.path.join(os.path.abspath(os.path.dirname(__file__)), csv_file_name)):
    os.remove(os.path.join(os.path.abspath(os.path.dirname(__file__)), csv_file_name))
    
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=' + server + ';'
                                           'Database=' + database_name + ';'
                                                                         'Trusted_Connection=yes;',
                      autocommit=True, encoding='utf-8')

def execute_query(query):
    with conn:
        cursor = conn.cursor()
        cursor.execute(query)
    return cursor


execute_query(f"USE {database_name};")


def write_csv_file(file_name, textline):
    
    """
    This function will write a new line into csv file in order to Bulk insert into TBL_MASSECHET_WORD table.
    :param file_name: the csv file name
    :param textline: the string that will be appended to the csv file
    """
    with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), file_name), "a", encoding='utf-8') as f:
        f.write(f"{textline}\r")  
        
          

def get_xml_word_and_attributes(xml):
        
        tree = ET.ElementTree(file=current_dir_path + '\\' + xml)
        
        for elem in tree.findall('Word'):
            
            attributes = elem.attrib
            print(attributes)
            
            perek_pasuk_id = ''
            
            word_position = attributes.get('WordSequence') 

            if attributes.get('Ktiv') == 'true':
                isKtiv = 1
            else:
                isKtiv = 0
            if attributes.get('Kri') == 'true':
                isKri = 1
            else:
                isKri = 0  
                  
            word = elem.text
            
            word = re.sub('[\[\]\(\)]+','',elem.text)
            
            
      
            textline = f"|{perek_pasuk_id}|{word_position}|{isKtiv}|{isKri}|{word}"   
        
            write_csv_file(csv_file_name,textline)    
            
            
for xml in tanakh_dir_list:

    get_xml_word_and_attributes(xml) 



def bulk_insert_to_tbl(csv_file_path, tbl_name):
    execute_query(f"SET IDENTITY_INSERT {table_names[3]} ON;")
    query = f"BULK INSERT {tbl_name} \
            FROM '{csv_file_path}' \
            WITH \
                (  \
                     FIELDTERMINATOR ='|' \
                    , ROWTERMINATOR ='\r' \
                    ,CODEPAGE = '65001' \
                );"
    execute_query(f"SET IDENTITY_INSERT {table_names[3]} OFF;")

    execute_query(query)


