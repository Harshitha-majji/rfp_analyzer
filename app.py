import streamlit as st

from pdf_processor import extract_text
from rfp_analyzer import analyze_rfp
from agent import (
    generate_memory_queries,
    generate_recommendations,
    call_openrouter,
)
from proposal_generator import generate_proposal
from app.memory import ProposalMemory


st.title("RFP Analyzer")

st.write("Upload an RFP PDF to analyze it and generate a proposal.")

pdf_file = st.file_uploader(
    "Upload your RFP",
    type=["pdf"]
)


if pdf_file:

    text = extract_text(pdf_file)

    st.subheader("Extracted RFP Text")
    st.write(text)

    if st.button("Analyze RFP"):

        # -------------------------------------------------
        # STEP 1 — Analyze RFP
        # -------------------------------------------------

        with st.spinner("Analyzing RFP..."):
            rfp_analysis = analyze_rfp(text)

        st.subheader("RFP Analysis")
        st.write(rfp_analysis)

        # -------------------------------------------------
        # STEP 2 — Generate memory queries
        # -------------------------------------------------

        with st.spinner("Generating memory queries..."):
            memory_queries = generate_memory_queries(rfp_analysis)

        st.subheader("Memory Queries")

        for i, query in enumerate(memory_queries, start=1):
            st.write(f"{i}. {query}")

        # -------------------------------------------------
        # STEP 3 — Retrieve Hindsight memories
        # -------------------------------------------------

        with st.spinner("Retrieving historical memories..."):

            memory = ProposalMemory()

            all_memories = []

            try:
                for query in memory_queries:

                    recall_result = memory.recall(query)

                    for item in recall_result.results:
                        all_memories.append({
                            "query": query,
                            "memory": item.text
                        })

            finally:
                memory.close()

        st.subheader("Retrieved Memories")

        if all_memories:

            for item in all_memories:
                st.write(f"**Query:** {item['query']}")
                st.write(item["memory"])
                st.divider()

        else:

            st.info("No relevant previous memories were found.")

        # -------------------------------------------------
        # STEP 4 — Generate recommendations
        # -------------------------------------------------

        with st.spinner("Generating recommendations..."):

            recommendations = generate_recommendations(
                rfp_analysis,
                all_memories
            )

        st.subheader("Recommendations")
        st.json(recommendations)

        # -------------------------------------------------
        # STEP 5 — Generate final proposal
        # -------------------------------------------------

        with st.spinner("Generating final proposal..."):

            proposal_result = generate_proposal(
                rfp=text,
                memories=all_memories,
                llm_function=call_openrouter
            )

        st.subheader("Final Proposal")

        st.write(proposal_result["proposal"])

        st.caption(
            f"Historical memories used: "
            f"{proposal_result['memory_count']}"
        )