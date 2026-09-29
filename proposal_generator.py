from prompts import build_proposal_prompt


def generate_proposal(rfp, memories, llm_function):
    """
    Generate a proposal using the current RFP and
    historical memories retrieved from Hindsight.
    """

    prompt = build_proposal_prompt(
        rfp=rfp,
        memories=memories
    )

    response = llm_function(prompt)

    return {
        "proposal": response,
        "memories_used": memories,
        "memory_count": len(memories),
    }