import streamlit as st
from pdf_processor import extract_text
from rfp_analyzer import analyze_rfp

st.title("RFP Analyzer")

st.write("Upload an RFP PDF to analyze it.")

pdf_file=st.file_uploader("Upload your RFP",type=["pdf"])

if pdf_file:

    text=extract_text(pdf_file)

    st.subheader("Extracted RFP Text")
    st.write(text)

    if st.button("Analyze RFP"):

        with st.spinner("Analyzing RFP..."):

            result=analyze_rfp(text)

        st.subheader("RFP Analysis")

        st.write(result)