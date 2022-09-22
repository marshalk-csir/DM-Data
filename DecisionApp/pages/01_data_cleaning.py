from re import A
import streamlit as st
import numpy as np
import pandas as pd
import category_encoders as ce
import plotly.figure_factory as ff
import matplotlib.pyplot as plt
import seaborn as sns
import io

df = st.session_state['df']



st.title("Data Preparation")

#st.write(df.head(25))

tab,tab1, tab2, tab3= st.tabs(['Selecting data','Cleaning data','Feature Engineering', 'Customize your plot'])
if df is not None:

    with tab:
        st.subheader('Drop zero variance features:')
        col_list=df.columns
        st.write('Shape Before:',df.shape)
        zero_var_lst =[]
        for col in col_list:
            if len(df[col].unique())==1:
                zero_var_col = zero_var_col.append(col)
                zero_var_df =pd.DataFrame({'Column Names':zero_var_col})
                st.write(zero_var_df)
                df.drop(col,axis=1, inplace=True)
        st.write('Shape After:',df.shape)
        st.subheader('Drop irrelevant and/ or sensitive data:')
        all_columns_names = df.columns.tolist()
        st.write('Shape Before:',df.shape)
        options = st.multiselect(
        'Selecting attributes to drop',
        all_columns_names)
        to_drop =options
        st.write('You selected:', to_drop)
        df.drop(to_drop,axis=1,inplace=True)
        st.write('Shape After:',df.shape)

        st.subheader('selecting categories')
        st.write('Shape Before:',df.shape)
        obj_cols =df.select_dtypes(include ='object').columns.tolist()
        sel_colum = st.selectbox('Select Column:', obj_cols)
        if df[sel_colum].dtype == 'object':
            records_lst = df[sel_colum].unique().tolist()
            record_options = st.multiselect(
            'Selecting Records To Drop:',
            records_lst)
            st.write('You selected:', record_options)
        st.write('Shape After:',df.shape)

    with tab1:
        st.header('HANDLING MISSING VAUES')
        st.write('Columns with missing values:')
        NAs = pd.concat([(df.isnull().sum()*100/len(df))], axis=1, keys=['% of null values'])
        col_with_NAs = NAs[NAs.sum(axis=1) > 0]
        with_only_NAs = pd.DataFrame(col_with_NAs.to_records())
        with_only_NAs.columns =['Column name','% of null values']
        st.write(with_only_NAs)
        st.subheader('Drop rows and/or columns if they contain only missing values:')
        st.write('shape before:', df.shape)
        df =df.dropna(axis=0,how='all')
        df =df.dropna(axis=1,how='all')
        st.write('shape after:',df.shape)
        threshold = st.slider("% of null values:", 0, len(df.columns.tolist()))
        txt = 'Drop row that contain less than {threshold} non-null values:'.format(threshold = threshold)
        st.subheader(txt)
        st.write('shape before:', df.shape)
        df.dropna(thresh= threshold)
        st.write('shape after:', df.shape)
        #txt1 = 'Drop rows that contain less than {threshold} observations:'.format(threshold = threshold[0])
        #st.subheader(txt1)
        #st.write('shape before:', df.shape)
        #df.dropna(thresh=threshold[0])
        #st.write('shape after:',df.shape)



        st.subheader('Filling missing values:')
        #st.write(df.isnull().any(axis=1))

        # Select a column to treat missing values
        col_option = st.selectbox("Select Column to treat missing values", df.columns)

        # Specify options to treat missing values

        if  df[col_option].dtype == 'float64' or df[col_option].dtype == 'int64':
            missing_values_clear = st.selectbox("Select Missing values treatment method", ("Replace with Mean", "Replace with Median","Replace with Mode"),key = A)
            if missing_values_clear == "Replace with Mean":
                replaced_value = df[col_option].mean()
                st.write("Mean value of column is :", replaced_value)
                Replace = st.selectbox("Replace values of column?", ("Yes", "No"),key = 'B')
                if Replace == "Yes":
                    df[col_option] = df[col_option].fillna(replaced_value)
                    st.write("Null values replaced")
                elif Replace == "No":
                    st.write("No changes made")
            elif missing_values_clear == "Replace with Median":
                replaced_value = df[col_option].median()
                st.write("Median value of column is :", replaced_value)
                Replace = st.selectbox("Replace values of column?", ("Yes", "No"),key = 'B')
                if Replace == "Yes":
                    df[col_option] = df[col_option].fillna(replaced_value)
                    st.write("Null values replaced")
                elif Replace == "No":
                    st.write("No changes made")
        elif df[col_option].dtype == 'object':
            missing_values_clear = st.selectbox("Select Missing values treatment method", ("Replace with Mean", "Replace with Median","Replace with Mode"),key ='C')
            if missing_values_clear == "Replace with Mode":
                replaced_value = df[col_option].mode()
                st.write("Mode value of column is :", replaced_value)
                Replace = st.selectbox("Replace values of column?", ("Yes", "No"),key = 'B')
                if Replace == "Yes":
                    df[col_option] = df[col_option].fillna(replaced_value)
                    st.write("Null values replaced")
                elif Replace == "No":
                    st.write("No changes made")

        st.header('HANDLING DATA ERRORS/INCONSISTENCIES')
        all_columns_names2 = df.columns.tolist()
        sel_colum2 = st.selectbox('Choose column', all_columns_names2)
        st.subheader('Change characters case:')
        char_case = st.selectbox("Select  case to use", ("lower", "upper", "title","capitalize"))

        if df[sel_colum2].dtype == 'object':
            if char_case == "lower":
                df[sel_colum2] = df[sel_colum2].str.lower()
            elif char_case == "upper":
                df[sel_colum2] = df[sel_colum2].str.upper()
            elif char_case == "title":
                df[sel_colum2] = df[sel_colum2].str.title()
            elif char_case == "capitalize":
                df[sel_colum2] = df[sel_colum2].str.capitalize()

        st.subheader("Replace values given in to_replace with value:")
        if df[sel_colum2].dtype == 'object':
            to_replace = st.text_input(label='to_replace')
            value = st.text_input(label='value')
        elif df[sel_colum2].dtype == 'int64' or df[sel_colum2].dtype == 'float64':
            to_replace = st.number_input(label ='to_replace')
            value =st.number_input(label='value')
        df[sel_colum2].replace(to_replace=to_replace, value=value, inplace=True)
        st.write(df[sel_colum2].unique())

        st.header('DEALING WITH DUPLICATES')
        st.subheader('Discovering Duplicates:')
        duplicates_df =df[df.duplicated(keep=False)]
        st.write('Number of duplicated rows:',df.duplicated().sum())
        st.write(duplicates_df)
        st.subheader('Removing Duplicates:')
        st.write('Shape Before:',df.shape)
        df.drop_duplicates(inplace=True)
        st.write('Shape After:',df.shape)


        st.header('HANDLING OUTLIERS')
        sel_colum3 = st.selectbox('Choose column', all_columns_names2, key ='4')
        if df[sel_colum3].dtype =='int64' or df[sel_colum3].dtype == 'float64':
            st.subheader('Discover Outliers:')
            fig2 = plt.figure(figsize=(10, 4))
            sns.boxplot(x=df[sel_colum3])
            st.pyplot(fig2)
            # IQR
            Q1 = np.percentile(df[sel_colum3], 25,interpolation = 'midpoint')
            Q3 = np.percentile(df[sel_colum3], 75,interpolation = 'midpoint')
            IQR = Q3 - Q1
            # Upper bound
            upper = np.where(df[sel_colum3] >= (Q3+1.5*IQR))
            # Lower bound
            lower = np.where(df[sel_colum3] <= (Q1-1.5*IQR))
            st.subheader('Removing the Outliers')
            st.write("Shape Before: ", df.shape)
            df.drop(upper[0], inplace = True)
            df.drop(lower[0], inplace = True)
            st.write("Shape After: ", df.shape)

    with tab2:
        obj_df = df.select_dtypes(include=['object']).copy()
        all_columns_names2 = obj_df.columns.tolist()

        sel_colum2 = st.selectbox('Choose your columns to encode', all_columns_names2, key = 2)
        st.write(df[sel_colum2].value_counts())

        encode_methods = ['Categorical encoding','Ordinal encoding', 'date-time conversion']
        sel_column3 = st.selectbox ('Choose the encding method: ',encode_methods, key =3)
