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
import altair as alt
import plotly.express as px
import numpy as np
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from plotly.offline import init_notebook_mode, iplot
init_notebook_mode()
st.set_option('deprecation.showPyplotGlobalUse', False)

df = st.session_state['df'] 



st.title("Data Visualization")

# sideb = st.sidebar
# corr = sideb.button('Click for correlation plot')
# piplot = sideb.button ('Click for pie plot')
# custom_plot = sideb.button('Click for a custom plot')


tab1, tab2, tab3 = st.tabs(['Correlation plot','Pie Plot', 'Customize your plot'])
#Correlation
#Seaborn Plot
with tab1:
    df_corr = df.corr()
    fig_corr = go.Figure([go.Heatmap(z=df_corr.values,
                                 x=df_corr.index.values,
                                 y=df_corr.columns.values)])
    #data=[trace]
    st.plotly_chart(fig_corr)
    #st.write(sns.heatmap(df.corr(),annot=True))
    #st.pyplot()

with tab2:
    all_columns_names = df.columns.tolist()
    value = st.selectbox("Value", df.select_dtypes(include=['float', 'int']).columns.tolist())
    name = st.selectbox("Name", df.select_dtypes(include=['object', 'datetime']).columns.tolist())
    
    if st.button("Generate Pie Plot"):
        st.success("Generating A Pie Plot")
        fig = plt.subplots(figsize=(35,25))
        fig = px.pie(df, values=value, names=name)
        fig.update_layout(width=600,height=600)
        #fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig, use_container_width=True)


# Customizable Plot
with tab3:
    st.subheader("Customizable Plot")
    all_columns_names = df.columns.tolist()
    type_of_plot = st.selectbox("Select Type of Plot",["area","bar","line","count", "histogram", "box", "kde", "scatterplot"])

    # Plot By Streamlit
    if type_of_plot == 'area':
        x_column_name = st.multiselect("Select (X) Column To Plot", all_columns_names)
        y_column_name = st.multiselect("Select (Y) Column To Plot", all_columns_names)
        hue_column_name = st.multiselect("Select (Color) Column To Plot", all_columns_names)
        
        if st.button("Generate Plot"):
            fig, ax = plt.subplots(figsize=(25,10))
            if hue_column_name == []:
                fig = px.area(df, x=x_column_name[0], y=y_column_name[0])
            else:
                fig = px.area(df, x=x_column_name[0], y=y_column_name[0], color=hue_column_name[0])

            fig.update_layout(xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=False), paper_bgcolor="rgba(255,255,255,0)", plot_bgcolor="rgba(255,255,255,0)",
                height=600)

            st.plotly_chart(fig, use_container_width=True)

    elif type_of_plot == 'bar':
        x_column_name = st.multiselect("Select (X) Column To Plot", all_columns_names, key='x')
        y_column_name = st.multiselect("Select (Y) Column To Plot", all_columns_names, key='y')
        hue_column_name = st.multiselect("Select (Color) Column To Plot", all_columns_names, key='hue')

        if st.button("Generate Plot"):
            fig, ax = plt.subplots(figsize=(25,10))

            if hue_column_name == []:
                st.write(sns.barplot(data=df, x=x_column_name[0], y=y_column_name[0], ci=None, lw=3, ax=ax))
            else:
                st.write(sns.barplot(data=df, x=x_column_name[0], y=y_column_name[0], hue=hue_column_name[0], ci=None, lw=3, ax=ax))

            if df[x_column_name[0]].dtype != np.object0:
                for p in ax.patches:
                    ax.annotate('{:.0f}'.format(p.get_width()), 
                            (p.get_width(), p.get_y() + p.get_height() / 2.), 
                            ha = 'left', va = 'center', 
                            xytext = (3, 1), 
                            textcoords = 'offset points')

            else:
                for p in ax.patches:
                    ax.annotate('{:.0f}'.format(p.get_height()), 
                            (p.get_x() + p.get_width() / 2., p.get_height()), 
                            ha = 'center', va = 'center', 
                            xytext = (0, 10), 
                            textcoords = 'offset points')
            
            plt.rcParams["font.weight"] = "bold"
            plt.rcParams["axes.labelweight"] = "bold"
            
            plt.xticks(rotation=45, horizontalalignment="center")
            
            st.pyplot(fig)

    
    elif type_of_plot == 'line':
        x_column_name = st.multiselect("Select (X) Column To Plot", all_columns_names, key='x')
        y_column_name = st.multiselect("Select (Y) Column To Plot", all_columns_names, key='y')
        hue_column_name = st.multiselect("Select (Color) Column To Plot", all_columns_names, key='hue')
        
        if st.button("Generate Plot"):
            if len(df[x_column_name[0]].unique()) > 80:
            
                fig = plt.figure(figsize=(30,10))
                #st.write(df[x_column_name[0]].unique())

                if hue_column_name == []:
                    if st.button("Generate Plot"):
                        st.write(sns.lineplot(data=df[:80], x=x_column_name[0], y=y_column_name[0], ci=None, lw=3))
                        plt.xticks(rotation=90, horizontalalignment="center")
                        st.pyplot(fig)    
                else:
                    hue_column = st.selectbox(hue_column_name[0], df[hue_column_name[0]].unique())                
                    if st.button("Generate Plot"):
                        opt = df[hue_column_name[0]] == hue_column
                        st.write(sns.lineplot(data=df[opt][:80], x=x_column_name[0], y=y_column_name[0], ci=None, lw=3))
                        plt.xticks(rotation=90, horizontalalignment="center")
                        st.pyplot(fig)
            else:
                #if st.button("Generate Plot"):
                fig = plt.figure(figsize=(25,10))
                
                if hue_column_name == []:
                    st.write(sns.lineplot(data=df, x=x_column_name[0], y=y_column_name[0], ci=None, lw=3))
                else:
                    st.write(sns.lineplot(data=df, x=x_column_name[0], y=y_column_name[0], hue=hue_column_name[0], ci=None, lw=3))
                        
                plt.xticks(rotation=45, horizontalalignment="center")
                st.pyplot(fig)


    elif type_of_plot == "count": #if it is only categorical data
        x_column_name = st.multiselect("Select (X) Column To Plot", all_columns_names, key='x')
        hue_column_name = st.multiselect("Select (Color) Column To Plot", all_columns_names, key='hue')

        if st.button("Generate Plot"):
            st.success("Generating Customizable Plot of {} for {} {} ".format(type_of_plot,x_column_name, hue_column_name))

            fig, ax = plt.subplots(figsize=(25,10))
            st.write(sns.countplot(x=x_column_name[0], hue=hue_column_name[0],  data=df, ax=ax))
            for p in ax.patches:
                ax.annotate(format(p.get_height(), '.0f'), 
                            (p.get_x() + p.get_width() / 2., p.get_height()), 
                            ha = 'center', va = 'center', 
                            xytext = (0, 9), 
                            textcoords = 'offset points')
            #fig = plt.yscale("log")
            st.pyplot(fig)

    elif type_of_plot == 'histogram':
        x_column_name = st.multiselect("Select (X) Column To Plot", df.select_dtypes(include=['float', 'int']).columns.tolist())
    # y_column_name = st.multiselect("Select (Y) Column To Plot", df.select_dtypes(include=['float', 'int']).columns.tolist())
        hue_column_name = st.multiselect("Select (Color) Column To Plot", df.select_dtypes(include=['object', 'datetime']).columns.tolist())
        
        if st.button("Generate Plot"):
            
            fig, ax = plt.subplots(figsize=(25,10))
            if hue_column_name == []:
                fig = px.histogram(df, x=x_column_name[0])
            else:
                fig = px.histogram(df, x=x_column_name[0], color=hue_column_name[0])

            fig.update_layout(xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=False), paper_bgcolor="rgba(255,255,255,0)", plot_bgcolor="rgba(255,255,255,0)",
                height=600)

            st.plotly_chart(fig, use_container_width=True)

    # Custom Plot 
    elif type_of_plot == 'box':
        x_column_name = st.multiselect("Select (X) Column To Plot", df.select_dtypes(include=['float', 'int']).columns.tolist())
    # y_column_name = st.multiselect("Select (Y) Column To Plot", df.select_dtypes(include=['float', 'int']).columns.tolist())
        hue_column_name = st.multiselect("Select (Color) Column To Plot", df.select_dtypes(include=['object', 'datetime']).columns.tolist())
        
        if st.button("Generate Plot"):
           
            fig, ax = plt.subplots(figsize=(25,10))
            if hue_column_name == []:
                fig = px.box(df, x=x_column_name[0])
            else:
                fig = px.box(df, x=x_column_name[0], color=hue_column_name[0])

            fig.update_layout(xaxis=dict(showgrid=False),
                yaxis=dict(showgrid=False), paper_bgcolor="rgba(255,255,255,0)", plot_bgcolor="rgba(255,255,255,0)",
                height=600)

            st.plotly_chart(fig, use_container_width=True)

    elif type_of_plot == 'kde':
        x_column_name = st.multiselect("Select (X) Column To Plot", df.select_dtypes(include=['float', 'int']).columns.tolist())
    # y_column_name = st.multiselect("Select (Y) Column To Plot", df.select_dtypes(include=['float', 'int']).columns.tolist())
        hue_column_name = st.multiselect("Select (Color) Column To Plot", df.select_dtypes(include=['object', 'datetime']).columns.tolist())

        if st.button("Generate Plot"):
            fig = plt.figure(figsize=(25,10))
            
            if hue_column_name == []:
                st.write(sns.kdeplot(data=df, x=x_column_name[0]))
            else:
                st.write(sns.kdeplot(data=df, x=x_column_name[0], hue=hue_column_name[0]))
                    
            st.pyplot(fig)

    elif type_of_plot == 'scatterplot':
        x_column_name = st.multiselect("Select (X) Column To Plot", df.select_dtypes(include=['float', 'int']).columns.tolist())
        y_column_name = st.multiselect("Select (Y) Column To Plot", df.select_dtypes(include=['float', 'int']).columns.tolist())

        x = df[x_column_name]
        y = df[y_column_name]

        if st.button("Generate Plot"):
            fig = plt.figure(figsize=(25,10))
            
            st.write(sns.regplot(x, y, ci=None))
                      
            st.pyplot(fig)
    

        
           
    #cust_data = cust_data.rename(columns={selected_columns_names[0]:'lat', selected_columns_names[1]:'lon'}, inplace=True)
    #st.map(cust_data, zoom= 11)
