from re import A
import streamlit as st
import pandas as pd
import category_encoders as ce

df = st.session_state['df'] 



st.title("Data Cleaning")

#st.write(df.head(25))

tab0, tab1,tab_null, tab2, tab3 = st.tabs(['Data Shape','Columns exploration','Check for null values','Encode values', 'Customize your plot'])
if df is not None:
   
    with tab0:
        st.write(df.shape)
    with tab1:
        all_columns_names = df.columns.tolist()
        sel_colum = st.selectbox('Select colums to analyse', all_columns_names)
        st.write(df[sel_colum].unique())
    with tab_null:
        st.write(df.isna().sum())
        #st.write(df.isnull().any(axis=1))

        # Select a column to treat missing values
        col_option = st.selectbox("Select Column to treat missing values", df.columns) 

        # Specify options to treat missing values
        missing_values_clear = st.selectbox("Select Missing values treatment method", ("Replace with Mean", "Replace with Median", "Replace with Mode"),key = A)

        if missing_values_clear == "Replace with Mean":
            replaced_value = df[col_option].mean()
            st.write("Mean value of column is :", replaced_value)
        elif missing_values_clear == "Replace with Median":
            replaced_value = df[col_option].median()
            st.write("Median value of column is :", replaced_value)
        elif missing_values_clear == "Replace with Mode":
            replaced_value = df[col_option].mode()
            st.write("Mode value of column is :", replaced_value)

        Replace = st.selectbox("Replace values of column?", ("Yes", "No"),key = 'B')
        if Replace == "Yes":
            df[col_option] = df[col_option].fillna(replaced_value)
            st.write("Null values replaced")
        elif Replace == "No":
            st.write("No changes made")

    with tab2:

        obj_df = df.select_dtypes(include=['object']).copy() 
        all_columns_names2 = obj_df.columns.tolist()
        
        sel_colum2 = st.selectbox('Choose your columns to encode', all_columns_names2, key = 2)
        st.write(df[sel_colum2].value_counts())

        encode_methods = ['Categorical encoding','Ordinal encoding', 'date-time conversion']
        sel_column3 = st.selectbox ('Choose the encding method: ',encode_methods, key =3)


        


        