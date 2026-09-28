from prompts import build_proposal_prompt


def generate_proposal(rfp, memories, llm_function):
    """Generate a proposal from an RFP and historical memories."""
    prompt = build_proposal_prompt(rfp, memories)
    response = llm_function(prompt)

    return {
        "proposal": response,
        "memories_used": memories,
        "memory_count": len(memories),
    }
