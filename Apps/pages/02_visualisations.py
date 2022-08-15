import streamlit as st
import pandas as pd
import io
# Viz Pkgs
import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use('Agg')
import seaborn as sns 

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
    st.write(sns.heatmap(df.corr(),annot=True))
    st.pyplot()


# Pie Chart
# if piplot:
#     all_columns_names = df.columns.tolist()
#     if st.button("Generate Pie Plot"):
#         st.success("Generating A Pie Plot")
#         st.write(df.iloc[:,-1].value_counts().plot.pie(autopct="%1.1f%%"))
#         st.pyplot()

# Customizable Plot


#if custom_plot:
    #custom_plot = True
with tab3:
    st.subheader("Customizable Plot")
    all_columns_names = df.columns.tolist()
    type_of_plot = st.selectbox("Select Type of Plot",["area","bar","line","hist","box","kde"])
    #custom_plot = True
    selected_columns_names = st.multiselect("Select Columns To Plot", all_columns_names, key='2')
    st.write(all_columns_names)
    st.write(selected_columns_names)
    st.write(type_of_plot)
    #st.write(custom_plot)

    if st.button("Generate Plot"):
        st.success("Generating Customizable Plot of {} for {}".format(type_of_plot,selected_columns_names))

        # Plot By Streamlit
        if type_of_plot == 'area':
            cust_data = df[selected_columns_names]
            
            st.area_chart(cust_data)

        elif type_of_plot == 'bar':
            cust_data = df[selected_columns_names]
            st.bar_chart(cust_data)

        elif type_of_plot == 'line':
            cust_data = df[selected_columns_names]
            st.line_chart(cust_data)

        # Custom Plot 
        elif type_of_plot:
            cust_plot= df[selected_columns_names].plot(kind=type_of_plot)
            st.write(cust_plot)
            st.pyplot()