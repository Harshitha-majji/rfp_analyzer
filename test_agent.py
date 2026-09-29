from agent import generate_memory_queries


rfp_analysis = """
Client:
ABC Institute of Technology

Project:
Smart Campus Management System

Requirements:
Secure authentication, student management, faculty management,
attendance management, event management, announcements,
facility information, search functionality, administrative dashboard.

Technical Requirements:
Responsive web interface, REST APIs, Python or Node.js,
PostgreSQL or MongoDB, role-based access control,
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

Eligibility:
At least 3 years of web application development experience
and at least two similar software projects.

Evaluation:
Technical approach, relevant experience, development team,
timeline, security, support plan, commercial proposal.

Constraints:
Data protection requirements, minimum 5,000 registered users,
future scalability, source code handover.
"""


queries = generate_memory_queries(rfp_analysis)

print("\nMEMORY QUERIES:\n")

for i, query in enumerate(queries, start=1):
    print(f"{i}. {query}")