# ProposalMind Frontend

Frontend for the Proposal & RFP Agent hackathon project.

## Run in VS Code

1. Install Node.js (18+ recommended).
2. Open this folder in VS Code.
3. Open the terminal.
4. Run:

```bash
npm install
npm run dev
```

5. Open the localhost URL shown by Vite.

## Current version

This is the **Member 5 frontend MVP**. It currently uses mock data so the UI can be developed before the backend is connected.

### User flow

Dashboard
→ Upload RFP
→ RFP Analysis
→ Hindsight Memory
→ Generate Proposal
→ Proposal Preview

## Backend integration

Replace the mock actions in `src/main.jsx` with API calls when the other team members expose their endpoints.

Suggested API contracts:

POST /api/analyze-rfp
Response:
{
  "client": "...",
  "requirements": ["..."]
}

POST /api/retrieve-memory
Response:
{
  "memories": [
    {
      "title": "...",
      "status": "WON | LOST",
      "reason": "...",
      "detail": "..."
    }
  ]
}

POST /api/generate-proposal
Response:
{
  "proposal": "..."
}
