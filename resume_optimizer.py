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
    optimize_resume_batch
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

    emit("objective", 15, "Extracting resume structure...")

    objective = extract_objective(html)
    objective_html = "\n".join(objective)

    skills = extract_skills(html)
    skills_html = "\n".join(skills)

    exp_bullets = extract_experience_bullets(html)
    exp_bullet_strings = ["\n".join(b) for b in exp_bullets]

    proj_bullets = extract_project_bullets(html)
    proj_bullet_strings = ["\n".join(b) for b in proj_bullets]

    emit("skills", 30, "Optimizing all resume sections in batch mode...")

    batch_result = optimize_resume_batch(
        objective_html,
        skills_html,
        exp_bullet_strings,
        proj_bullet_strings,
        jd
    )

    emit("experience", 65, "Validating & applying Career Objective and Skills...")

    # Objective
    updated_obj = batch_result.get("objective", "")
    if updated_obj:
        valid, reason = validate_fragment(objective_html, updated_obj)
        print(f"Objective validation: {reason}")
        if valid:
            html = replace_bullet_by_classes(html, objective_html, updated_obj)

    # Skills
    updated_skills = batch_result.get("skills", "")
    if updated_skills:
        valid, reason = validate_fragment(skills_html, updated_skills)
        print(f"Skills validation: {reason}")
        if valid:
            html = replace_bullet_by_classes(html, skills_html, updated_skills)

    # Experience Bullets
    updated_exp = batch_result.get("experience_bullets", [])
    emit("experience", 78, f"Validating {len(exp_bullet_strings)} Experience Bullets...")
    for idx, original in enumerate(exp_bullet_strings):
        if idx < len(updated_exp):
            updated = updated_exp[idx]
            valid, reason = validate_fragment(original, updated)
            print(f"Exp Bullet {idx+1} validation: {reason}")
            if valid:
                html = replace_bullet_by_classes(html, original, updated)

    # Project Bullets
    updated_proj = batch_result.get("project_bullets", [])
    emit("projects", 85, f"Validating {len(proj_bullet_strings)} Project Bullets...")
    for idx, original in enumerate(proj_bullet_strings):
        if idx < len(updated_proj):
            updated = updated_proj[idx]
            valid, reason = validate_fragment(original, updated)
            print(f"Proj Bullet {idx+1} validation: {reason}")
            if valid:
                html = replace_bullet_by_classes(html, original, updated)

    emit("assembly", 90, "Reconstructing HTML structure...")
    return html