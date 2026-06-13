from bullet_extractor import extract_experience_bullets
from optimizer import optimize_bullet

jd = """
Java Backend Developer

Requirements:

Java 17+
Spring Boot
Microservices
REST APIs
Kafka
Redis
Hibernate
Docker
CI/CD
AWS
SQL
Performance Optimization
JUnit
Design Patterns
Distributed Systems
"""

with open(
    "resumes/master_resume.html",
    encoding="utf-8"
) as f:
    html = f.read()

bullets = extract_experience_bullets(html)

print(f"Found {len(bullets)} bullets")

print("\n========== ORIGINAL BULLET ==========\n")

first_bullet = "\n".join(
    bullets[0]
)

print(first_bullet)

print("\n========== OPTIMIZED BULLET ==========\n")

updated = optimize_bullet(
    first_bullet,
    jd
)

print(updated)

from validator import validate_fragment

valid, reason = validate_fragment(
    first_bullet,
    updated
)

print("\nVALIDATION")
print(valid)
print(reason)