import streamlit as st
from pathlib import Path
from typing import List
from pydantic import BaseModel
from openai import AzureOpenAI
import PyPDF2

# Initialize Azure OpenAI client
client = AzureOpenAI(  
    azure_endpoint="https://uswest3daniel.openai.azure.com",  
    api_key="fcb2ce5dc289487fad0f6674a0b35312",  
    api_version="2024-10-01-preview",
)  

# Define a simple PDF extraction function
def extract_text_from_pdf(pdf_path: Path) -> str:
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

# Function to split text into sections (can be enhanced)
def split_into_sections(text: str) -> List[str]:
    return text.split("\n\n")  # Split by double line breaks (or paragraphs)

# Initialize the Streamlit app
st.title("Document Summary Extractor")

# File upload
uploaded_file = st.file_uploader("Upload a PDF or Text File", type=["pdf", "txt"])

if uploaded_file:
    # Process the uploaded file
    if uploaded_file.type == "application/pdf":
        st.write("Processing PDF...")
        document_text = extract_text_from_pdf(uploaded_file)
    else:
        st.write("Processing Text File...")
        document_text = uploaded_file.getvalue().decode("utf-8")

    # Split the document into sections
    sections = split_into_sections(document_text)

    # Show the first section to the user
    st.write("First section of the document:")
    st.write(sections[0])

    # Function to call Azure OpenAI API for summaries
    def get_summary_from_azure(section: str) -> str:
        messages = [{"role": "user", "content": f"Summarize this section: {section}"}]
        response = client.chat.completions.create(  
            model="GPT-4Omni",  
            messages=messages,  
            temperature=0,  
            max_tokens=4095,  
            top_p=1
        )
        return response.choices[0].message.content.strip()

    # Extract summaries for each section using Azure OpenAI
    def extract_summaries(sections: List[str]) -> List[str]:
        summaries = []
        for section in sections:
            summary = get_summary_from_azure(section)
            summaries.append(summary)
        return summaries

    # Button to trigger the extraction of summaries
    if st.button("Generate Summaries"):
        with st.spinner("Extracting summaries..."):
            summaries = extract_summaries(sections)
            for i, summary in enumerate(summaries):
                st.write(f"Section {i+1} Summary:")
                st.write(summary)
        
    st.write("End of app")
