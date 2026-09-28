from hindsight_client import Hindsight


class ProposalMemory:

    def __init__(self):
        self.client = Hindsight(
            base_url="http://localhost:8888"
        )

        self.bank_id = "proposal-memory"

    def remember(self, content, context=None):
        """Store proposal/RFP information in Hindsight."""

        return self.client.retain(
            bank_id=self.bank_id,
            content=content,
            context=context
        )

    def recall(self, query):
        """Retrieve relevant information from previous proposals/RFPs."""

        return self.client.recall(
            bank_id=self.bank_id,
            query=query
        )

    def close(self):
        """Close the Hindsight client."""

        self.client.close()