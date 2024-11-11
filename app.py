import streamlit as st
from pathlib import Path
from typing import List
from pydantic import BaseModel
from llama_index import LLM, ServiceContext
from llama_index.core.llms import ChatMessage
from llama_index import Node, GPTSimpleVectorIndex

# Define a simple PDF or text extraction function
def extract_text_from_pdf(pdf_path: Path) -> str:
    import PyPDF2
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

# Function to split the text into sections (this is a simple split by paragraphs, can be enhanced)
def split_into_sections(text: str) -> List[str]:
    return text.split("\n\n")  # Split sections by double line breaks or paragraph

# Initialize the Streamlit app
st.title("Document Summary Extractor")

# File upload
uploaded_file = st.file_uploader("Upload a PDF or Text File", type=["pdf", "txt"])

# Initialize LlamaIndex LLM and ServiceContext
llm_instance = LLM()  # Initialize the LLM
service_context = ServiceContext.from_defaults(llm=llm_instance)

# Function to generate summaries using llama_index LLM
def generate_summary(text: str) -> str:
    # Use the ChatMessage to interact with the LLM
    chat_message = ChatMessage(role="user", content=f"Summarize this text: {text}")
    response = llm_instance.chat([chat_message])  # Pass the message to the LLM
    return response.content

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

    # Generate summaries for each section
    if st.button("Generate Summaries"):
        summaries = []
        with st.spinner("Extracting summaries..."):
            for section in sections:
                summary = generate_summary(section)  # Generate summary using llama_index LLM
                summaries.append(summary)

        # Display the summaries
        for i, summary in enumerate(summaries):
            st.write(f"Summary of section {i+1}:")
            st.write(summary)

    st.write("End of app")
