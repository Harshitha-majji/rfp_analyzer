from app.memory import ProposalMemory


def retrieve_memories(queries):
    """
    Send the generated memory queries to Hindsight
    and return JSON-serializable memory results.
    """

    memory = ProposalMemory()
    memories = []

    try:
        for query in queries:

            results = memory.recall(query)

            for result in results:
                memories.append(
                    {
                        "query": query,
                        "id": getattr(result, "id", None),
                        "type": getattr(result, "type", None),
                        "text": getattr(result, "text", str(result))
                    }
                )

        return memories

    finally:
        memory.close()