import streamlit as st
import pandas as pd
import io


st.title("Data Analysis ")

#uploaded_file =st.file_uploader("Choose a file")

df = st.session_state['df'] 


if df is not None:
    #dataframe = pd.read_csv(uploaded_file,encoding= 'utf-8')
    #st.write(dataframe.head(25))
    #sideb = st.sidebar
    click1,click2, click3,data_types = st.tabs(['Show summary of your data','Show Column Names','Preview of your data','Data types',])
    #click2 = st.tabs('Click to see the columns')
    #click3 = st.tabs('Click to see a preview of your data')
    #click4 = st.tabs('Click to see a preview')
    #data_types = st.tabs("Show data types")
    #data_table = sideb.button('')
    with click1:
        #buffer = io.StringIO()
        #dataframe.info(buf=buffer)
        #s = buffer.getvalue()
        #st.text(s)
        #st.write(df.describe().T)
        df_types = pd.DataFrame(df.dtypes, columns=['Data Type'])
        numerical_cols = df_types[~df_types['Data Type'].isin(['object', 'bool'])].index.values

        df_types['Count'] = df.count()
        df_types['Unique Values'] = df.nunique()
        df_types['Min'] = df[numerical_cols].min()
        df_types['Max'] = df[numerical_cols].max()
        df_types['Average'] = df[numerical_cols].mean()
        df_types['Median'] = df[numerical_cols].median()
        df_types['St. Dev.'] = df[numerical_cols].std()

        #st.subheader('Summary of ' + selected_option + '\'s Data')
        st.write(df_types.astype(str))
        st.write(df.info())
    with click2:
        columns = df.columns
        st.write(columns)
    with click3:
        number = st.slider("Select No of Rows", 1, df.shape[0])
        st.write(df.head(number))
    with data_types:
        st.write(df.dtypes.astype(str))
   






