# Proposal Generator — Member 4

This is the independent Proposal Generator module for the hackathon.

## What it does

RFP requirements + historical proposal memories
-> Proposal Generator
-> personalized proposal

The starter version runs without an API key, so you can test it immediately.

## Run in VS Code

1. Open this folder in VS Code.
2. Open the integrated terminal.
3. Run:

```bash
python app.py
```

If `python` is not recognized on Windows, try:

```bash
py app.py
```

## Your module

- `sample_data.py` — temporary RFP and historical memories
- `prompts.py` — LLM instructions
- `proposal_generator.py` — main reusable generator
- `app.py` — local test/demo
- `requirements.txt` — future dependencies
- `.env.example` — API-key template

## Team integration later

Member 3 will eventually replace `sample_rfp` with the real RFP Analyzer output.

Member 2 will eventually replace `past_memories` with relevant Hindsight memories.

Member 1 can later provide the real `llm_function`.

Your main interface is:

```python
generate_proposal(rfp, memories, llm_function)
```

Keep this interface stable so the other team members can connect their work later.
