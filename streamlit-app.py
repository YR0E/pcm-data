import streamlit as st
# import pandas as pd
# import numpy as np
from datetime import date

from data_processing import reading_data, processing_data
from plotting import plot_data



st.title('PCM experimental data processing')


uploaded_file = st.file_uploader('Choose experimental data file', type='csv')
is_sample = st.checkbox('Use sample data', value=True*(uploaded_file is None),
                        help='As an example, data from 2024_05_28.csv will be used. Use when no data is uploaded')
if (is_sample) and (uploaded_file is None):
    uploaded_file = './data/2024_05_28.csv'


st.markdown('***')


if uploaded_file is not None:
    # read uploaded file and process data
    df_raw = reading_data(uploaded_file, is_sample)
    df, invalid_columns = processing_data(df_raw)


    ### SECTION 1
    st.subheader('Looking at raw data')

    # expander 1
    with st.expander("See uploaded data"):
        st.dataframe(df_raw, height=280)

        # note 1
        st.markdown(f'''Note further:
- Channels renamed `T1`, `T2`, `T3`, etc.  
- Channels with no data: {', '.join(invalid_columns)}.''')
    

    # plot 1
    plot_data(df)



    ### SECTION 2
    st.markdown('***')
    st.subheader('Processing data')


    # multiselect
    options = st.multiselect('Select parameters:', options=df.columns, default=['T1', 'T2', 'T3'])
    
    
    col1, col2 = st.columns([1, 3])
    # interpolate and naming
    today = date.today().strftime("%d_%m_%Y")
    is_interp = col1.checkbox('Interpolate data', value=True)
    if is_interp:
        df = df.interpolate()
        filename = f"experimental_data_{today}_interp.csv"
    else:
        filename = f"experimental_data_{today}.csv"

    # time range
    interval = col2.slider('Select time range, seconds:', min_value=0, max_value=df.index[-1], value=(0, df.index[-1]))
    df_processed = df[options].loc[interval[0]:interval[1]].copy()

    # plot 2
    plot_data(df_processed)


    # expander 2
    with st.expander("See processed data"):
        # reset index
        is_reset_index = st.checkbox('Reset index', value=True)
        if is_reset_index:
            df_processed = df_processed.reset_index(drop=True)
            df_processed.index.name = 'seconds'

        # preview
        st.dataframe(df_processed, height=280)


    # download
    st.download_button(
    label="Download processed data as CSV",
    data=df_processed.to_csv(),
    file_name=filename,
    mime="text/csv", )