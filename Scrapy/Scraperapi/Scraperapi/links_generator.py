from datetime import datetime
import pandas as pd

def links_generator(): 
    
    SKUS_file = 'skus.json'
    df = pd.read_json(SKUS_file)
    
    lista = []
    
    for i in range(df.shape[0]):  
        lista.extend((list(df.iloc[i]))[0]) 
   
    not_duplicate_list = pd.unique(lista) 
    not_duplicate_list = list(not_duplicate_list) 
    
    url_amazon = []
   
    for sku in not_duplicate_list:
        url_amazon.append('https://amazon.com/-/es/dp/' + sku + '/')
    
    return url_amazon  
