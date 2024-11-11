import streamlit as st
from PyPDF2 import PdfReader
from llama_index import Document, ServiceContext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.extractors import (
    SummaryExtractor,
    QuestionsAnsweredExtractor,
    TitleExtractor,
    KeywordExtractor,
)
from llama_index.extractors.entity import EntityExtractor
from llama_index import VectorStoreIndex

# Function to extract text from PDF
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Function to apply transformations and extract summary
def extract_summary(text):
    # Create Document from text
    documents = [Document(text)]
    
    # Set up the LlamaIndex service context
    service_context = ServiceContext.from_defaults()
    
    # Create a list of transformations
    transformations = [
        SentenceSplitter(),
        TitleExtractor(nodes=5),
        QuestionsAnsweredExtractor(questions=3),
        SummaryExtractor(summaries=["prev", "self"]),
        KeywordExtractor(keywords=10),
        EntityExtractor(prediction_threshold=0.5),
    ]
    
    # Create an index with the transformations
    index = VectorStoreIndex.from_documents(documents, service_context=service_context)
    
    # Apply transformations to the index and extract summary
    summary_result = index.extract_with_transformations(transformations)
    
    return summary_result.get("summaries", [])

# Streamlit app UI
def main():
    st.title("PDF Summary Extractor using LlamaIndex")
    
    # Upload PDF file
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    
    if uploaded_file is not None:
        # Extract text from PDF
        text = extract_text_from_pdf(uploaded_file)
        
        if text:
            st.write("Extracting summary...")
            
            # Get the summary using the extractor transformations
            summaries = extract_summary(text)
            
            if summaries:
                st.subheader("Extracted Summary:")
                st.write("\n".join(summaries))
            else:
                st.warning("No summary could be generated.")
        else:
            st.warning("No text could be extracted from the PDF.")

if __name__ == "__main__":
    main()
