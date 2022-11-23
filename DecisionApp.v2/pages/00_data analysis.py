import streamlit as st
import pandas as pd
import numpy as np
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns
import io

st.title("Data Analysis ")

#uploaded_file =st.file_uploader("Choose a file")

df = st.session_state['df']


if df is not None:
    #dataframe = pd.read_csv(uploaded_file,encoding= 'utf-8')
    #st.write(dataframe.head(25))
    #sideb = st.sidebar
    click3,description,click4 ,click1, click5= st.tabs(['Preview of your data','Description','Distribution','Summary',"What's next?"])
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

        all_columns_names1 = df.columns.tolist()
        sel_colum = st.selectbox('Select Column to get Summary', all_columns_names1)
        if df[sel_colum].dtype == 'float64' or df[sel_colum].dtype == 'int64':
            st.write(df[sel_colum].describe(datetime_is_numeric =True).T)
        else:
            df_summary = pd.DataFrame(df.columns,columns=['Column Name'])
            df_summary['Column Name'] =df[sel_colum].name
            df_summary['count'] =df[sel_colum].count()
            df_summary['unique'] =len(df[sel_colum].unique())
            df_summary['top'] =df[sel_colum].mode()
            df_summary['freq'] = df[sel_colum].value_counts()[0]
            sel_df = df_summary.iloc[:1,:]
            st.write(sel_df.astype(str))
        observe_1 = st.text_input('Observation(e.g, zero variance,range of values make no sense)',)
        st.write(observe_1)

    with click3:
        number = st.slider("Select No of Rows", 1, df.shape[0])
        st.write(df.head(number))
        st.write('Attribute Information:')
        observe_4 = st.text_input('Attribute: Attribute Range',)
        st.write(observe_4)

    with description:
        st.write('Total No. Columns:', len(df.columns))
        st.write('Total No. Records:', len(df))
        all_columns_names = df.columns.tolist()
        sel_colum = st.selectbox('Select column to get description', all_columns_names)
        df_description =pd.DataFrame(df.columns,columns=['Column Name'])
        df_description['Column Name'] =df[sel_colum].name
        df_description['Data Type'] =df[sel_colum].dtype
        df_description['Number of non-null values'] =df[sel_colum].notna().sum()
        df_description['Number of null values'] =df[sel_colum].isna().sum()
        sel_df = df_description.iloc[:1,:]
        st.write(sel_df.astype(str))
        observe_2 = st.text_input('Observation(e.g, inconsistent datatype,missing values)',)
        st.write(observe_2)

    with click4:
        all_columns_names = df.columns.tolist()
        sel_colum = st.selectbox('Select colums to analyse', all_columns_names)
           # Plot By Streamlit
        if df[sel_colum].dtype == 'object':
            chart_data = df[sel_colum].value_counts()
            st.write('Number of Unique Values:',len(df[sel_colum].unique()))
            st.write(chart_data)
            st.bar_chart(chart_data)

        elif df[sel_colum].dtype =='int64' or df[sel_colum].dtype == 'float64':

            fig1 = plt.figure(figsize=(10, 4))
            sns.histplot(df[sel_colum])
            st.pyplot(fig1)

        observe_3 = st.text_input('Observation(e.g, Outliers,range of values make no sense)',)
        st.write(observe_3)

    with click5:

        observe_df = pd.DataFrame()
        observe_df['Column_name']=df.columns.tolist()
        observe_df['Observation']='NaN'
        observe_df['Action']='NaN'
        st.write(observe_df)
        #observation_lst = ['missing data','data errors','coding inconsistances']
        #for column in df.columns.tolist():
        #    observe_df['Column_name'] = observe_df['Column_name'].append(observe_df[column])
        #    Observation = observe_df['Observation'].append('missing data')
            #Observation = st.selectbox('Observed', observation_lst)
        #    if Observation == 'missing data':
        #        Action = 'Exlude rows or characteristics or, fill blanks with an estimated value'
        #    elif Observation == 'data errors':
        #        Action = 'use logic to manually discover errors and replace.Or exclude characteristics'
        #    elif Observation == 'coding inconsistances':
        #        Action = 'Decide upon a single coding scheme, then convert and replace values'
