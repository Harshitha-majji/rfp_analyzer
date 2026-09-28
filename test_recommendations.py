import json

from agent import generate_memory_queries, generate_recommendations


rfp_analysis = """
Client: ABC Institute of Technology

Project: Smart Campus Management System

Requirements:
Student management, faculty management, attendance, events,
announcements, facility information, search functionality,
administrative dashboard.

Technical Requirements:
Python or Node.js, PostgreSQL or MongoDB, REST APIs,
responsive web interface, role-based access control,
secure password storage, HTTPS, input validation,
regular database backups.

Deliverables:
Complete web application, source code, database schema,
REST API documentation, deployment documentation,
administrator documentation, user documentation,
testing report, administrator training.

Timeline:
16 weeks.

Budget:
INR 12,00,000 to INR 15,00,000.

Users:
At least 5,000 registered users.

Constraints:
Data protection requirements, future scalability,
source code handover.
"""


# ---------------------------------------------------------
# Load mock organizational memories
# ---------------------------------------------------------

with open("mock_memories.json", "r", encoding="utf-8") as file:
    memories = json.load(file)


# ---------------------------------------------------------
# STEP 1 — Generate memory queries
# ---------------------------------------------------------

print("\nSTEP 1 — MEMORY QUERIES\n")

queries = generate_memory_queries(rfp_analysis)

for i, query in enumerate(queries, start=1):
    print(f"{i}. {query}")


# ---------------------------------------------------------
# STEP 2 — Analyze retrieved memories
# ---------------------------------------------------------

print("\nSTEP 2 — MEMORY ANALYSIS\n")

recommendations = generate_recommendations(
    rfp_analysis,
    memories
)

print(json.dumps(recommendations, indent=2, ensure_ascii=False))