import streamlit as st
from llama_index import LlamaIndex  # Import the LlamaIndex class
from io import StringIO

# Define function to summarize the document using LlamaIndex
def summarize_document(content: str) -> str:
    # Initialize LlamaIndex
    index = LlamaIndex()
    
    # Build the document index and get the summary
    index.build(content)
    summary = index.summarize()
    return summary

# Streamlit UI
st.title("Document Summarizer with LlamaIndex")

uploaded_file = st.file_uploader("Upload a document", type=["txt", "pdf"])

if uploaded_file is not None:
    # Read file content
    if uploaded_file.type == "application/pdf":
        # For PDFs, additional processing might be needed (e.g., PyMuPDF, pdfplumber)
        st.error("PDF processing is not yet implemented. Try a .txt file.")
    else:
        # Assume a text file for simplicity
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        content = stringio.read()

        st.write("### Uploaded Document")
        st.text(content)

        # Generate summary
        if st.button("Generate Summary"):
            with st.spinner("Generating summary..."):
                summary = summarize_document(content)
                st.write("### Summary")
                st.success(summary)
