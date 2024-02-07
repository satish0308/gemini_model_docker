import streamlit as st
import os
#from PathLib import Path
import pathlib
import textwrap
import PyPDF2
import base64
import PIL.Image
from dotenv import load_dotenv
load_dotenv()


import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

api_key = os.environ.get("GOOGLE_API_KEY")

genai.configure(api_key=api_key)
st.title('Your own gemeni model')

value=st.radio(label='please select MODEL',options=['Gemini_Pro','Gemini_Pro_Vision'])

if value == 'Gemini_Pro_Vision':
    st.write('You have selected Gemini Pro Vision Model')
    value=st.radio(label='please select file type',options=['PDF','Image','word'])
    if value == 'PDF':
        uploaded_file = st.file_uploader("Choose a file")
        model_name='gemini-pro'
    
        if uploaded_file is not None:
            # creating a pdf reader object
            pdfReader = PyPDF2.PdfReader(uploaded_file)

            # printing number of pages in pdf file
            print(len(pdfReader.pages))

            # creating a page object
            pageObj = pdfReader.pages[0]

            # extracting text from page
            input_value=pageObj.extract_text()
            #st.markdown(uploaded_file)
            # closing the pdf file object
            bytes_data = uploaded_file.getvalue()

            base64_pdf = base64.b64encode(bytes_data).decode('utf-8')
            pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
            #st.markdown(pdf_display, unsafe_allow_html=True)
    
    elif value == 'Image':
        uploaded_file = st.file_uploader("Choose a file")
        if uploaded_file is not None:
            img = PIL.Image.open(uploaded_file)
            input_value=img  
            model_name='gemini-pro-vision'
    elif value == 'Word':
        pass
    
    prompt_value=st.text_input('Please Enter the Prompt Details',key='prompt_vision')
    
        

elif value == 'Gemini_Pro':
    st.write('You have selected Gemini Pro Model')
    model_name='gemini-pro'
    prompt_value=st.text_input('Please Enter the Prompt Details',key='prompt')
    input_value=st.text_input('Please Enter the Question',key='input')


submit=st.button("Submit", type="primary")

def Gemini_Model(input,model,prompt):
    model = genai.GenerativeModel(model)
    response = model.generate_content([prompt,input])
    st.write(response.text)
    #print(response.text)


if submit:
    st.write(input_value)
    st.write(model_name)
    st.write(prompt_value)
    Gemini_Model(input_value,model_name,prompt_value)