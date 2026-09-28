from app.proposal_agent import ProposalAgent


rfp_text = """
RFP TITLE: Cloud Migration Solution

CLIENT: ABC Corporation

ABC Corporation is requesting a cloud migration solution.

The proposal should provide competitive and clearly justified pricing.

The implementation timeline should be short.

The proposal should explain:
1. The migration approach
2. The implementation plan
3. Expected outcomes
"""

rfp_analysis = """
Client: ABC Corporation
Project: Cloud Migration Solution
Requirements:
- Competitive and clearly justified pricing
- Short implementation timeline
- Explain migration approach
- Explain implementation plan
- Explain expected outcomes
"""

memory_queries = [
    "ABC Corporation previous cloud migration proposals",
    "cloud migration previous proposals pricing timeline",
    "unsuccessful cloud migration proposals lessons learned"
]


agent = ProposalAgent()

result = agent.generate_integrated_recommendations(
    rfp_text=rfp_text,
    rfp_analysis=rfp_analysis,
    memory_queries=memory_queries
)

print("\n=== MEMORY COUNT ===")
print(result["memory_count"])

print("\n=== RETRIEVED MEMORIES ===")
for memory in result["memories"]:
    print("-", memory)

print("\n=== RECOMMENDATIONS ===")
print(result["recommendations"])