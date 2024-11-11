import streamlit as st
from pathlib import Path
from typing import List
from pydantic import BaseModel
from llama_index.core.llms import ChatMessage  # Import ChatMessage
from your_module import SummaryExtractor, TextNode, BaseNode  # Adjust to your imports
from your_module.llm import LLM  # Your LLM module (if necessary)

# Define a simple PDF or text extraction function
def extract_text_from_pdf(pdf_path: Path) -> str:
    import PyPDF2
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

# Function to split the text into sections (this is a simple split by paragraphs)
def split_into_sections(text: str) -> List[str]:
    return text.split("\n\n")  # Split sections by double line breaks or paragraphs

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

    # Define the LLM to use (based on ChatMessage for generating summaries)
    class CustomLLM:
        def chat(self, messages):
            # Here, replace this mock implementation with the actual call to your LLM
            response = llm.chat([ChatMessage(role="user", content=messages[0]['content'])])
            return response

    # Initialize the SummaryExtractor with the custom LLM
    llm_instance = CustomLLM()  # Use your actual LLM instance here
    summary_extractor = SummaryExtractor(
        llm=llm_instance,
        summaries=["self", "prev", "next"],  # Extract self, previous, and next summaries
        prompt_template="Summarize this section: {section}"  # Example template
    )

    # Extract summaries asynchronously for each section
    async def extract_summaries():
        nodes = [TextNode(content=section) for section in sections]  # Create nodes for each section
        summaries = await summary_extractor.aextract(nodes)  # Extract summaries
        return summaries

    # Button to trigger summary generation
    if st.button("Generate Summaries"):
        summaries_placeholder = st.empty()  # Display placeholder for summaries
        with st.spinner("Extracting summaries..."):
            summaries = await extract_summaries()
            for i, summary in enumerate(summaries):
                st.write(f"Section {i+1} Summary:")
                st.write(summary)
        
    st.write("End of app")
