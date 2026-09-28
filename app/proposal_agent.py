import os

from groq import Groq
from memory import ProposalMemory


class ProposalAgent:

    def __init__(self):
        self.memory = ProposalMemory()

        self.llm = Groq(
            api_key=os.environ["GROQ_API_KEY"]
        )

        self.model = "openai/gpt-oss-20b"

    def analyze_rfp(self, rfp_text):
        """Retrieve relevant previous proposal experience."""

        results = self.memory.recall(
            query=rfp_text
        )

        memories = []

        for result in results.results:
            memories.append(result.text)

        return memories

    def generate_recommendations(self, rfp_text):
        """Generate proposal recommendations using RFP + previous experience."""

        memories = self.analyze_rfp(rfp_text)

        memory_context = "\n".join(
            f"- {memory}" for memory in memories
        )

        prompt = f"""
You are a Proposal and RFP Assistant.

Analyze the following RFP and provide practical proposal recommendations.

NEW RFP:
{rfp_text}

RELEVANT PREVIOUS EXPERIENCE:
{memory_context}

Based on the RFP and previous experience:

1. Identify important proposal requirements.
2. Identify lessons from previous experience that should be applied.
3. Identify risks or mistakes to avoid.
4. Suggest specific actions for the proposal team.

Do not invent facts that are not present in the RFP or previous experience.
"""

        response = self.llm.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content


if __name__ == "__main__":

    agent = ProposalAgent()

    rfp_file = "data/rfps/abc_cloud_migration.txt"

    with open(rfp_file, "r", encoding="utf-8") as file:
        rfp = file.read()

    print("\n=== RFP LOADED ===\n")
    print(rfp)

    print("\n=== PROPOSAL RECOMMENDATIONS ===\n")

    recommendations = agent.generate_recommendations(rfp)

    print(recommendations)