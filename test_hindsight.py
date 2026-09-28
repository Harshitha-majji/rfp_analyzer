from hindsight_client import Hindsight

client = Hindsight(
    base_url="http://localhost:8888"
)

result = client.recall(
    bank_id="proposal-memory",
    query="What happened with ABC Corporation's previous proposal?"
)

print(result)