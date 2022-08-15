import streamlit as st
import pandas as pd
import io


st.title("Data Analysis ")

#uploaded_file =st.file_uploader("Choose a file")

df = st.session_state['df'] 

if df is not None:
    #dataframe = pd.read_csv(uploaded_file,encoding= 'utf-8')
    #st.write(dataframe.head(25))
    sideb = st.sidebar
    click1 = sideb.button('Click here for a summary of your data')
    click2 = sideb.button('Click to see the columns')
    click3 = sideb.button ('Click to see missing values')
    click4 = sideb.button('Click to see a preview')
    data_types = sideb.button ("Show data types")
    if click1:
        #buffer = io.StringIO()
        #dataframe.info(buf=buffer)
        #s = buffer.getvalue()
        #st.text(s)
        st.write(df.describe().T)
    if click2:
        columns = df.columns
        st.write(columns)
    if click3:
        st.write(df.isnull().sum())
    if data_types:
        st.write(df.dtypes.astype(str))
    if click4:
        st.write(df.head(30))






