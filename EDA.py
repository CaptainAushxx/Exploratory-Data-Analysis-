import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import os

st.title('Exploratory Data Analysis')

st.markdown("""
This app performs EDA
* **Contact Us: ** [marathonfox.com] (https://marathonfox.com/contact-us/).""")

file_bytes = st.file_uploader('Upload a file', type="csv")
print(file_bytes)

if file_bytes is not None:
    data = pd.read_csv(file_bytes)
    obj = []
    int_float = []
    for i in data.columns:
        clas = data[i].dtypes
        if clas == 'object':
            obj.append(i)
        else:
            int_float.append(i)

    with st.form(key='my_form'):
        with st.sidebar:
            st.sidebar.header("To remove Null Values press button below")
            submit_button = st.form_submit_button(label='Remove Null')

    if submit_button:
        for i in data.columns:
            clas =data[i].dtypes
            if clas == 'object':
                data[i].fillna(data[i].mode()[0], inplace = True)
            else:
                data[i].fillna(data[i].mean(), inplace=True)

    lis = []
    for i in data.columns:
        dd = sum(pd.isnull(data[i]))
        lis.append(dd)

    if max(lis) == 0:
        st.write("Total no.of Null Values "+ str(max(lis)))
    else:
        st.write("Bar plot to know no.of Null values in each column")
        st.write("Total no.of Null Values "+str(sum(lis)))
        fig2 = px.bar(x=data.columns, y = lis, labels={'x':"Column Names", 'y':"No. of Null Values"})
        st.plotly_chart(fig2)

    st.sidebar.header("Select Variable")
    selected_pos = st.sidebar.selectbox('Object Variables', obj)
    st.write("Bar Plot to know frequency of each category")
    frequency_data = data[selected_pos].value_counts()
    fig = px.bar(frequency_data,x=frequency_data.index, y=selected_pos, labels={'x':selected_pos, 'y': "count"})
    st.plotly_chart(fig)

    st.sidebar.header("Select Variable")
    selected_pos1 = st.sidebar.selectbox('Int or Float Variables', int_float)
    st.write("Bar Plot to know count of calues based on range")
    counts, bins = np.histogram(data[selected_pos1], bins=range(int(min(data[selected_pos1])), int(max(data[selected_pos1])),int(max(data[selected_pos1])/10)))
    bins = 0.5 * (bins[: -1] + bins[1:])
    fig1 = px.bar(x=bins, y=counts, labels={'x':selected_pos1,'y':'count'})
    st.plotly_chart(fig1)

    st.sidebar.header("Select Variable")
    selected_pos2 = st.sidebar.multiselect('Int or Float Variables-Correlation',int_float)
    st.write("Scatter Plot for correlation")
    if len(selected_pos2)==2:
        fig3 = px.scatter(data,x=selected_pos2[0],y=selected_pos2[1])
        st.plotly_chart(fig3)
    else: 
        st.write("Selected Two Variables")


