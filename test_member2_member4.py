from app.proposal_agent import ProposalAgent
from proposal_generator import generate_proposal
from llm import generate_with_llm


rfp_text = """
REQUEST FOR PROPOSAL

Client: ABC Institute of Technology

Project: Smart Campus Management System

The institute requires a web-based Smart Campus Management System.

The system should provide:
- Student management
- Faculty management
- Attendance management
- Event management
- Announcements
- Facility information
- Search functionality
- Administrative dashboard

Technical requirements:
- Responsive web interface
- REST APIs
- Python or Node.js backend
- PostgreSQL or MongoDB
- Role-based access control
- Secure password storage
- HTTPS
- Input validation
- Regular database backups

The system must support at least 5,000 registered users.

The project should be completed within 16 weeks.

The estimated budget is INR 12,00,000 to INR 15,00,000.
"""


# These would normally come from Member 1
memory_queries = [
    "Previous proposals for ABC Institute of Technology",
    "Previous proposals for Smart Campus Management System",
    "Previous university proposals with PostgreSQL REST APIs RBAC",
    "Previous proposals supporting 5000 users",
    "Previous proposal security lessons",
]


# --------------------------------------------------
# STEP 1: Get real memories from Hindsight
# --------------------------------------------------

agent = ProposalAgent()

memories = agent.retrieve_memories(memory_queries)

print("\n=== HINDSIGHT MEMORIES ===")
print("Memory count:", len(memories))

for memory in memories:
    print("-", memory)


# --------------------------------------------------
# STEP 2: Give those real memories to Member 4
# --------------------------------------------------

result = generate_proposal(
    rfp=rfp_text,
    memories=memories,
    llm_function=generate_with_llm
)


# --------------------------------------------------
# STEP 3: Display generated proposal
# --------------------------------------------------

print("\n=== FINAL PROPOSAL ===\n")
print(result["proposal"])

print("\n=== MEMORIES USED ===")
print(result["memory_count"])