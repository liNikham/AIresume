from extractor import extract_sections
from optimizer import optimize_section
from validator import validate_fragment


with open(
        "resumes/master_resume.html",
        encoding="utf-8") as f:

    html = f.read()


sections = extract_sections(html)

print("\nFOUND SECTIONS\n")

for key in sections.keys():
    print(key)

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


optimized_sections = {}

for section_name in [
    "Objective",
    "Experience",
    "Projects",
    "Skills"
]:

    print(
        f"\nOptimizing {section_name}..."
    )

    original_fragment = "\n".join(
        sections[section_name]
    )

    updated_fragment = optimize_section(
        section_name,
        original_fragment,
        jd
    )

    valid, reason = validate_fragment(
        original_fragment,
        updated_fragment
    )

    print(
        f"{section_name}: {reason}"
    )

    if valid:

        optimized_sections[
            section_name
        ] = updated_fragment

    else:

        print(
            f"Validation failed for {section_name}"
        )

        optimized_sections[
            section_name
        ] = original_fragment


new_html = html

for section_name in optimized_sections:

    original_fragment = "\n".join(
        sections[section_name]
    )
    print("\n====================")
    print(section_name)
    print("====================")

    print(original_fragment[:1000])

    updated_fragment = optimized_sections[
        section_name
    ]
    print(f"\n===== GENERATED {section_name} =====\n")
    print(updated_fragment[:2000])

    new_html = new_html.replace(
        original_fragment,
        updated_fragment
    )


with open(
        "generated/tailored_resume.html",
        "w",
        encoding="utf-8") as f:

    f.write(new_html)

print(
    "\nGenerated: generated/tailored_resume.html"
)

