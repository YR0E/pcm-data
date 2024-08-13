import numpy as np
import pandas as pd
import streamlit as st


@st.cache_data(max_entries=1)
def reading_data(uploaded, is_sample):
    ''' read csv file with experimental data
    '''

    data = pd.read_csv(uploaded, sep=';', decimal=',',
                       encoding='cp1251', engine='python')
    return data


@st.cache_data(max_entries=1)
def processing_data(df):
    ''' process csv file with weather data
    '''

    # renaming columns
    df = df.drop(columns=['Время'])
    new_columns = [f'T{i}' for i in range(1, len(df.columns)+1)]
    df.columns = new_columns
    df.index.name = 'seconds'

    # replace missing data
    df = df.replace(['Нет'], np.nan)
    df = df.replace(['Таймаут'], np.nan)

    # select valid columns
    df = df.astype('float')
    valid_columns = df.columns[df.max() > -1000].to_list()
    invalid_columns = df.columns[~(df.max() > -1000)].to_list()
    
    return df[valid_columns], invalid_columns

if __name__ == '__main__':
    print('processing file')