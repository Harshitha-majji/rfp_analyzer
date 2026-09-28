import streamlit as st

from pdf_processor import extract_text
from rfp_analyzer import analyze_rfp
from agent import generate_memory_queries, generate_recommendations
from proposal_generator import generate_proposal
from app.memory import ProposalMemory


st.title("RFP Analyzer")

st.write("Upload an RFP PDF to analyze it.")

pdf_file = st.file_uploader(
    "Upload your RFP",
    type=["pdf"]
)

if pdf_file:

    text = extract_text(pdf_file)

    st.subheader("Extracted RFP Text")
    st.write(text)

    if st.button("Analyze RFP"):

        with st.spinner("Analyzing RFP..."):

            # ---------------------------------------
            # STEP 1: Analyze RFP
            # ---------------------------------------

            result = analyze_rfp(text)

        st.subheader("RFP Analysis")
        st.write(result)

        # ---------------------------------------
        # STEP 2: Generate memory queries
        # ---------------------------------------

        with st.spinner("Searching previous proposals..."):

            queries = generate_memory_queries(result)

        st.subheader("Memory Queries")

        for i, query in enumerate(queries, start=1):
            st.write(f"{i}. {query}")

        # ---------------------------------------
        # STEP 3: Retrieve Hindsight memories
        # ---------------------------------------

        memory = ProposalMemory()

        all_memories = []

        try:

            for query in queries:

                results = memory.recall(query)

                for item in results:

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

        # ---------------------------------------
        # STEP 4: Generate recommendations
        # ---------------------------------------

        with st.spinner("Generating recommendations..."):

            recommendations = generate_recommendations(
                result,
                all_memories
            )

        st.subheader("Recommendations")

        st.json(recommendations)
        # ---------------------------------------
        # STEP 5: Generate final proposal
        # ---------------------------------------

        with st.spinner("Generating final proposal..."):

            proposal_result = generate_proposal(
                result,
                all_memories,
                lambda prompt: __import__("agent").call_openrouter(prompt)
            )

        st.subheader("Generated Proposal")

        st.write(proposal_result["proposal"])

        st.caption(
            f"Historical memories used: "
            f"{proposal_result['memory_count']}"
        )
