from prompts import build_proposal_prompt


def generate_proposal(rfp, memories, llm_function):
<<<<<<< HEAD
    """Generate a proposal from an RFP and historical memories."""
    prompt = build_proposal_prompt(rfp, memories)
=======
    """
    Generate a proposal using the current RFP and
    historical memories retrieved from Hindsight.
    """

    prompt = build_proposal_prompt(
        rfp=rfp,
        memories=memories
    )

>>>>>>> member2-hindsight-local
    response = llm_function(prompt)

    return {
        "proposal": response,
        "memories_used": memories,
        "memory_count": len(memories),
<<<<<<< HEAD
    }
=======
    }
>>>>>>> member2-hindsight-local
