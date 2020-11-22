import streamlit as st
import pandas as pd
import numpy as np
import googletrans
from googletrans import Translator
import os
import base64
import xlsxwriter
from io import StringIO
import cgi



from enum import Enum
from io import BytesIO, StringIO
from typing import Union


STYLE = """
<style>
img {
    max-width: 100%;
}
</style>
"""

FILE_TYPES = ["csv","xlsx"]

translator = Translator()

st.title("")

class FileType(Enum):
    """Used to distinguish between file types"""

    IMAGE = "Image"
    CSV = "csv"
    PYTHON = "Python"
    EXCEL = "Excel"


def get_file_type(file: Union[BytesIO, StringIO]) -> FileType:
    """The file uploader widget does not provide information on the type of file uploaded so we have
    to guess using rules or ML. See
    [Issue 896](https://github.com/streamlit/streamlit/issues/896)

    I've implemented rules for now :-)

    Arguments:
        file {Union[BytesIO, StringIO]} -- The file uploaded

    Returns:
        FileType -- A best guess of the file type
    """
    content = file.getvalue()

    if ('xlsx' in file.name):
        return FileType.EXCEL

    return FileType.CSV

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

    


    


def main():
    """Run this function to display the Streamlit app"""
    #st.info(__doc__)
    st.markdown(STYLE, unsafe_allow_html=True)

    file = st.file_uploader("Upload file", type=FILE_TYPES)
    #show_file = st.empty()
    if not file:
        show_file.info("Lütfen şu uzantılı dosyaları yükleyin: " + ", ".join(FILE_TYPES))
        return

    file_type = get_file_type(file)
    if file_type == FileType.IMAGE:
        show_file.image(file)
    elif file_type == FileType.PYTHON:
        st.code(file.getvalue())
    else:
        if file_type ==  FileType.CSV:
            try:
                data = pd.read_csv(file)
            except:
                data = pd.read_csv(file,error_bad_lines = False)

            translate_download(data)

        else: 
            try:
                data = pd.read_excel(file)
            except:
                try:
                    data = pd.read_excel(file,index_col=None, header=None)
                except:
                    data = pd.read_html(file)

            translate_download(data)

    file.close()


main()


translator = Translator()

st.title("Excel ve csv dosyalarınızı burada herhangi bir dilden Türkçe'ye dönüştürebilirsiniz")
st.header("Google Translate ile bağlantılı çalışığından, hata verdiği zaman bir kaç kere tekrar denerseniz veya sayfayı yenilerseniz program çalışacaktır.")








    