import os
from hindsight_client import Hindsight

class ProposalMemory:
    def __init__(self):
        base_url=os.getenv(
            "HINDSIGHT_URL",
            "http://localhost:8888"
        )

        api_key=os.getenv("hsk_a91211f1ee7bbf3e72a4bde4e43acfa8_a16064863253b394")

        self.client=Hindsight(
            base_url=base_url,
            api_key=api_key
        )

        self.bank_id="proposal-memory"

    def remember(self, content, context=None):
        return self.client.retain(
            bank_id=self.bank_id,
            content=content,
            context=context
        )

    def recall(self, query):
        return self.client.recall(
            bank_id=self.bank_id,
            query=query
        )

    def close(self):
        self.client.close()