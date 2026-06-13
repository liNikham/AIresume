from bullet_extractor import extract_experience_bullets

with open(
        "resumes/master_resume.html",
        encoding="utf-8") as f:

    html = f.read()

bullets = extract_experience_bullets(html)

print(
    f"Found {len(bullets)} bullets"
)

for i, bullet in enumerate(bullets):

    print("\n")
    print("=" * 50)

    print(
        f"BULLET {i+1}"
    )

    print("=" * 50)

    print(
        "\n".join(bullet)
    )