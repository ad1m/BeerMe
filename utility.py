__author__ = 'Adamlieberman'

import pandas as pd
import re
import pickle

def load_data(link,features=None):
    df = pd.read_csv(link)
    if features:
        df = df[features]
    return df


def string_handler(row):
    row = str(row)
    try:
        row = row.encode('utf-8').decode('utf-8').lower()
    except UnicodeDecodeError:
        row = row.lower()
    return row



def preprocess(df):
    dtypes = list(df.dtypes)
    cols = df.columns

    #remove rows that have NaNs
    df.dropna(axis=0)

    for i in range(len(dtypes)):
        if dtypes[i] == object:
            #Make Strings and Lowercase all letters
            df[cols[i]] = df[cols[i]].apply(lambda j: string_handler(j))
        elif dtypes[i] == 'float64':
            #Make all numbers floats
            df[cols[i]] = df[cols[i]].apply(lambda k: float(k))
    return df

def mapping(df,col,name,reverse=False):
    '''
    Some columns have string values, create dict and replace for numerical values
    Additionally remap the dataframe to these values
    '''
    vals = df[col].values
    d = dict(zip(vals,range(len(vals))))
    df[col] = df[col].apply(lambda i: d[i])
    if reverse:
        reverse_d = {v: k for k, v in d.items()}
        #pickle reverse_dictionary
        with open(name,'wb') as f:
            pickle.dump(reverse_d,f)
        return d, reverse_d, df
    else:
        return d, df





if __name__ == "__main__":

    #Load Data
    print('Loading Data...')
    link = 'https://query.data.world/s/cqa9clje3ye4un611s1nw5fo3'
    features = ['beer_name','brewery_name','review_overall','review_aroma','review_appearance','beer_style','review_palate','review_taste']
    df = load_data(link,features)

    #Preprocess Data
    print('Preprocessing Data...')
    df = preprocess(df)
    print(df.head(5))


    #Mappings
    print('Remapping Data...')
    dict_brewery, reverse_dict_brewery, df = mapping(df,'brewery_name','reverse_dict_brewery.p',reverse=True)
    dict_style, reverse_dict_style, df = mapping(df,'beer_style','reverse_dict_style.p',reverse=True)
    dict_name, reverse_dict_name, df = mapping(df,'beer_name','reverse_dict_name.p',reverse=True)
    print(df.head(5))

    #Feature Generation - Use what we have but groupby and take mean
    features = df.groupby(['beer_name']).mean()
    namez = features.copy()
    namez.reset_index(level=0,inplace=True)
