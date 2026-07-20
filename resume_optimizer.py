from bullet_extractor import (
    extract_experience_bullets,
    extract_project_bullets
)

from objective_extractor import (
    extract_objective
)

from skills_extractor import (
    extract_skills
)

from dom_replacer import (
    replace_bullet_by_classes
)

from optimizer import (
    optimize_bullet,
    optimize_section
)

from validator import (
    validate_fragment
)


def optimize_resume(
        html,
        jd,
        progress_callback=None):

    def emit(step_id, progress, message):
        if progress_callback:
            try:
                progress_callback(step_id, progress, message)
            except Exception as err:
                print(f"Progress callback error: {err}")

    emit("objective", 15, "Optimizing Career Objective...")


    print("\n====================")
    print("OBJECTIVE")
    print("====================")

    objective = extract_objective(
        html
    )

    objective_html = "\n".join(
        objective
    )

    updated_objective = optimize_section(
        "Objective",
        objective_html,
        jd
    )

    valid, reason = validate_fragment(
        objective_html,
        updated_objective
    )

    print(
        f"Objective: {reason}"
    )

    if valid:

        print(
            "Replacing Objective"
        )

        html = replace_bullet_by_classes(
            html,
            objective_html,
            updated_objective
        )

    else:

        print(
            "Skipping Objective"
        )

    emit("skills", 35, "Aligning Skills & ATS Keywords...")

    print("\n====================")
    print("SKILLS")
    print("====================")

    skills = extract_skills(
        html
    )

    skills_html = "\n".join(
        skills
    )

    updated_skills = optimize_section(
        "Skills",
        skills_html,
        jd
    )

    valid, reason = validate_fragment(
        skills_html,
        updated_skills
    )

    print(
        f"Skills: {reason}"
    )

    if valid:

        print(
            "Replacing Skills"
        )

        html = replace_bullet_by_classes(
            html,
            skills_html,
            updated_skills
        )

    else:

        print(
            "Skipping Skills"
        )

    experience = extract_experience_bullets(
        html
    )

    print("\n====================")
    print("EXPERIENCE")
    print("====================")

    total_exp = len(experience) if len(experience) > 0 else 1

    for idx, bullet in enumerate(
            experience):

        prog = 35 + int(((idx + 1) / total_exp) * 30)
        emit("experience", prog, f"Tuning Experience Bullet {idx+1}/{total_exp}...")

        print(
            f"Optimizing Experience Bullet {idx+1}"
        )

        original = "\n".join(
            bullet
        )

        updated = optimize_bullet(
            original,
            jd
        )

        valid, reason = validate_fragment(
            original,
            updated
        )

        print(
            f"Validation: {reason}"
        )

        if valid:

            print(
                f"Replacing Experience Bullet {idx+1}"
            )

            html = replace_bullet_by_classes(
                html,
                original,
                updated
            )

        else:

            print(
                f"Skipping Experience Bullet {idx+1}"
            )

    projects = extract_project_bullets(
        html
    )

    print("\n====================")
    print("PROJECTS")
    print("====================")

    total_proj = len(projects) if len(projects) > 0 else 1

    for idx, bullet in enumerate(
            projects):

        prog = 65 + int(((idx + 1) / total_proj) * 25)
        emit("projects", prog, f"Refining Project Bullet {idx+1}/{total_proj}...")

        print(
            f"Optimizing Project Bullet {idx+1}"
        )

        original = "\n".join(
            bullet
        )

        updated = optimize_bullet(
            original,
            jd
        )

        valid, reason = validate_fragment(
            original,
            updated
        )

        print(
            f"Validation: {reason}"
        )

        if valid:

            print(
                f"Replacing Project Bullet {idx+1}"
            )

            html = replace_bullet_by_classes(
                html,
                original,
                updated
            )

        else:

            print(
                f"Skipping Project Bullet {idx+1}"
            )

            print("\nORIGINAL\n")
            print(original)

            print("\nGENERATED\n")
            print(updated)

    emit("assembly", 90, "Reconstructing HTML structure...")
    return html