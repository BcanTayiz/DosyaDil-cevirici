import streamlit as st
import pandas as pd
import numpy as np
import googletrans
from googletrans import Translator
import streamlit as st
import os
import base64
import xlsxwriter



translator = Translator()

sentence = """I think ordinary people may also be extraordinary."""

example = translator.translate(sentence,dest="tr").text

st.write(example)


def file_selector(folder_path='.'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    path = os.path.dirname(os.path.abspath(selected_filename))
    path = path + "\\" + selected_filename
    return path 

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download csv file</a>'

    st.markdown(href, unsafe_allow_html=True)

def translate_download(dataFrame):
    df_tr = dataFrame.copy()
    df_tr.rename(columns=lambda x: translator.translate(x,dest="tr").text, inplace=True)

    translations = {}
    for column in df_tr.columns:
        # unique elements of the column
        unique_elements = df_tr[column].unique()
        for element in unique_elements:
            # add translation to the dictionary
            try:
                translations[element] = translator.translate(element,dest="tr").text 
            except:
                continue


    df_tr.replace(translations, inplace = True)
    get_table_download_link(df_tr)


filename = file_selector()
st.write('You selected `%s`' % filename)



if "csv" in filename:
    try:
        data = pd.read_csv(filename)
    except:
        data = pd.read_csv(filename,error_bad_lines = False)

    translate_download(data)

else: 
    try:
        data = pd.read_excel(filename)
    except:
        try:
            data = pd.read_excel(filename,index_col=None, header=None)
        except:
            data = pd.read_html(filename)

    translate_download(data)






    