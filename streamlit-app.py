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
    options = st.multiselect('Select parameters:', options=df.columns, default=df.columns[:3].tolist())

    # store new labels in session state
    if 'new_labels' not in st.session_state:
        st.session_state.new_labels = options

    
    col1, col2 = st.columns([1, 3])
    # interpolate
    today = date.today().strftime("%d_%m_%Y")
    is_interp = col1.checkbox('Interpolate data', value=True)
    if is_interp:
        df = df.interpolate()
        filename = f"experimental_data_{today}_interp.csv"
    else:
        filename = f"experimental_data_{today}.csv"

    # rangeslider visible and reset index
    is_reset_index = col1.checkbox('Reset time', value=True)
    is_rangeslider = col1.checkbox('Show rangeslider', value=True)

    # time range
    interval = col2.slider('Select time range, seconds:', min_value=0, max_value=df.index[-1], value=(0, df.index[-1]))


    col1, col2, col3 = st.columns([3, 7.5, 1.5], vertical_alignment="bottom")

    # Text input for renaming labels
    labels = col2.text_input("Rename parameters", value=', '.join(st.session_state.new_labels),
                            help='Enter new parameter names separated by commas (e.g., `T1, T2, T3`)')
    # Reset button to clear labels with one click
    if col3.button("Reset", use_container_width=True):
        st.session_state.new_labels = options  # Reset labels to original
        labels = ', '.join(st.session_state.new_labels)  # Update the text input field
    st.session_state.new_labels = labels.split(', ')


    df_processed = df[options].loc[interval[0]:interval[1]].copy()
    df_processed = df_processed.rename(columns=dict(zip(options, st.session_state.new_labels)))
    if is_reset_index:
        df_processed = df_processed.reset_index(drop=True)
        df_processed.index.name = 'seconds'

    # plot 2
    plot_data(df_processed, rangesliderBool=is_rangeslider)


    # expander 2
    with st.expander("See processed data"):
        # preview
        st.dataframe(df_processed, height=280)


    # download
    st.download_button(
    label="Download processed data as CSV",
    data=df_processed.to_csv(),
    file_name=filename,
    mime="text/csv", )