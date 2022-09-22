import streamlit as st
import pandas as pd
import io
# Viz Pkgs
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import seaborn as sns
from chart_studio import plotly
#import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as ff
import plotly.express as px
import numpy as np

from plotly.offline import init_notebook_mode, iplot
init_notebook_mode()

df = st.session_state['df']



st.title("Relationships between two or more variables")

# sideb = st.sidebar
# corr = sideb.button('Click for correlation plot')
# piplot = sideb.button ('Click for pie plot')
# custom_plot = sideb.button('Click for a custom plot')


tab1, tab2, tab3 = st.tabs(['Visualisation of Correlation','Bivariate plots', 'Multivariate plots'])
#Correlation
#Seaborn Plot
with tab1:
    st.write('Heatmaps of Correlation Matrices')
    df_corr = df.corr()
    fig_corr = go.Figure([go.Heatmap(z=df_corr.values,
                                 x=df_corr.index.values,
                                 y=df_corr.columns.values)])
    #data=[trace]
    st.plotly_chart(fig_corr)
    #st.write(sns.heatmap(df.corr(),annot=True))
    #st.pyplot()

    st.write('X-Y Plots With a Regression Line')
    num_cols = df.select_dtypes(include='number').columns.tolist()
    sel_colum = st.selectbox('Select X', num_cols,key='1')
    sel_colum1 = st.selectbox('Select Y', num_cols,key='2')
    if df[sel_colum].dtype == 'float64' and df[sel_colum1].dtype == 'float64':
        x =df[sel_colum]
        y =df[sel_colum1]
        fig, ax = plt.subplots()
        sns.scatterplot(x,y, ax=ax)
        st.write(fig)

with tab2:
    all_columns_names1 = df.columns.tolist()


    sel_colum2 = st.selectbox('Select X', all_columns_names1,key='3')
    sel_colum3 = st.selectbox('Select Y', all_columns_names1,key='4')
    x =df[sel_colum2]
    y=df[sel_colum3]
    #categorical vs categorical
    if x.dtype =='object' and y.dtype == 'object':
        type_of_plot = st.selectbox("Select Type of Plot",["crosstab","countplot"],key='7')
        if type_of_plot == 'crosstab':
            table =pd.crosstab(x,y)
            st.write(table)
        elif type_of_plot == 'countplot':
            fig, ax = plt.subplots()
            sns.countplot(data=df, x=x, hue=y)
            st.write(fig)
        #elif type_of_plot == 'stacked bar':
        #    fig = plt.figure(figsize = (10, 5))
        #    plt.bar(Courses, values)
        #    st.pyplot(fig)
    #categorical vs numerical
    elif x.dtype =='object' and y.dtype == 'float64' or y.dtype == 'int64':
            type_of_plot = st.selectbox("Select Type of Plot",["barplot","boxplot"],key='10')
            if type_of_plot == 'barplot':
                fig, ax = plt.subplots()
                sns.barplot(x=x,y=y,data=df, ax=ax)
                st.write(fig)
            elif type_of_plot == 'boxplot':
                fig, ax = plt.subplots()
                sns.boxplot(x=x,y=y,data=df, ax=ax)
                st.write(fig)
    elif x.dtype == 'int64' or x.dtype == 'float64' and y.dtype =='int64' or y.dtype== 'float64':
        type_of_plot = st.selectbox("Select Type of Plot",["scatterplot","lineplot"],key='11')
        if type_of_plot == 'scatterplot':
            fig, ax = plt.subplots()
            sns.scatterplot(x=x,y=y, ax=ax)
            st.write(fig)
        elif type_of_plot == 'lineplot':
            fig, ax = plt.subplots()
            sns.lineplot(data=df, x=x, y=y,ax=ax)
            st.write(fig)

with tab3:
    all_columns_names = df.columns.tolist()
    obj_cols =df.select_dtypes(include='object').columns.tolist()
    num_cols =df.select_dtypes(include='number').columns.tolist()

    sel_colum4 = st.selectbox('Select X', all_columns_names,key='12')
    sel_colum5 = st.selectbox('Select Y', num_cols,key='13')
    sel_colum6 = st.selectbox('Select Z', obj_cols,key='14')
    x =df[sel_colum4]
    y=df[sel_colum5]
    z =df[sel_colum6]
    #categorical vs categorical
    if x.dtype == 'int64' or x.dtype == 'float64' and y.dtype =='int64' or y.dtype== 'float64' and z.dtype == 'object':
        type_of_plot = st.selectbox("Select Type of Plot",["scatterplot","lineplot"],key='15')
        if type_of_plot == 'scatterplot':
            fig, ax = plt.subplots()
            sns.scatterplot(data=df, x=x, y=y, hue=z)
            st.write(fig)
        elif type_of_plot == 'lineplot':
            fig, ax = plt.subplots()
            sns.lineplot(data=df, x=x, y=y, hue=z)
            st.write(fig)
    elif x.dtype =='object' and y.dtype == 'float64' or y.dtype == 'int64' and z.dtype =='object':
            type_of_plot = st.selectbox("Select Type of Plot",["boxplot","barplot"],key='10')
            if type_of_plot == 'boxplot':
                fig, ax = plt.subplots()
                sns.boxplot(x=x,y=y,data=df, hue =z)
                st.write(fig)
            #elif type_of_plot == 'boxplot':
            #    fig, ax = plt.subplots()
            #    sns.boxplot(x=x,y=y,data=df, ax=ax)
            #    st.write(fig)
