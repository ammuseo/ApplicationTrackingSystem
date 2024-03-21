import streamlit as st
import google.generativeai as genai
import os
import docx2txt
import PyPDF2 as pdf
from dotenv import load_dotenv

## load environment variable from a .env file
load_dotenv()

#configure the generative AI model with the Google API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

#set up the model configuration for text generation
generation_config={
    "temperature":0,
    "top_p":1,
    "top_k":32,
    "max_output_tokens":4096,
}
#define safety settings for the content generation
safety_ssettings=[
    {"category":f"HARM_CATEGORY_{category}","threshold":"BLOCK_MEDIUM_AND_ABOVE"}
    for category in ["HARASSMENT", "HATE_SPEECH", "SEXUALLY_EXPLICIT", "DANGEROUS_CONTENT"]
]
#CREATE THE MODEL
def generate_response_from_gemini(input_text):
    #create a GenerativeModel instance with 'gemini_pro' as the model type
    model=genai.GenerativeModel(
        model_name="gemini-pro",
        generation_config=generation_config,
        safety_settings=safety_ssettings,
    )
    #generate content based on the input text
    response=model.generate_content(input_text)
    #Return the generated text
    return response.text
def extract_text_from_pdf_file(uploaded_file):
    #Use PdfReader to read the content from a PDF file
    pdf_reader=pdf.PdfReader(uploaded_file)
    text_content=""
    for page in pdf_reader.pages:
        text_content+=str(page.extract_text())
        return text_content
    
def extract_text_from_docx_file(uploaded_file):
    #Use Docx2txt to extract text from a Docx file
    return docx2txt.process(uploaded_file)

#Prompt Template
input_prompt_template="""
Hey Act like a skilled or very experience ATS(Application Tracking System) with a deep unterstanding of tech field, software engineering, 
data science, data analyst, and big data engineer. Your task is to evaluate the resume based on the given job description. you must consider the job 
moarket is very competitive and you should provide best assistance for imporving the resumes. Assign the percentage Matching based 
on JD and 
the missing keywords with high accuracy
resume:{text}
description:{jd}

Evaluation Output:
1.Calculate the percentage of match between the resume and the job description. Give a number and explanation.
2.Identify any key keywords that are missing from the resume in comparison to the job description.
3. Offer specific and actionable tips to enhance the resume and improve its alignment with the job requirements. 
"""

#Streamlit app
#initialize streamlit app
st.set_page_config(page_title="ATS Resume Expert")
st.header(":blue[Smart ATS Resume Expert]" , divider='rainbow')
st.text("Improve your ATS resume score match")
##st.markdown('<style>h1{color:red; text_align:center;}</style>', unsafe_allow_html=True)
jd=st.text_area("Paste the Job Description:", height=300)
uploaded_file=st.file_uploader("Upload Your Resume....", type=["pdf", "docx"], help="Please upload a PDF or Docx file")

if uploaded_file is not None:
    st.success('The File Uploaded Successfully', icon="✅")
    ###st.write("The File Uploaded Successfully")

submit1=st.button("Check Your Score")


if submit1:
    if uploaded_file is not None:
        if uploaded_file.type=="application/pdf":
             resume_text=extract_text_from_pdf_file(uploaded_file)
        elif uploaded_file.type=="application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                resume_text=extract_text_from_docx_file(uploaded_file)
        response_text=generate_response_from_gemini(input_prompt_template.format(text=resume_text, jd=jd))

        st.subheader("ATS Evaluation Result:")
        st.write(response_text)
    else:
        st.write("Please upload the resume")
            

