from memory import ProposalMemory


memory = ProposalMemory()

results = memory.recall(
    "What do we know about ABC Corporation's previous proposal?"
)

print("\n=== RELEVANT MEMORIES ===\n")

for result in results.results:
    print(result.text)
    print()