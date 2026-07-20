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
    optimize_resume_batch,
    evaluate_ats_score
)

from validator import (
    validate_fragment
)


def apply_updates_to_html(current_html, batch_result, objective_html, skills_html, exp_bullet_strings, proj_bullet_strings):
    # Objective
    updated_obj = batch_result.get("objective", "")
    if updated_obj:
        valid, reason = validate_fragment(objective_html, updated_obj)
        print(f"Objective validation: {reason}")
        if valid:
            current_html = replace_bullet_by_classes(current_html, objective_html, updated_obj)

    # Skills
    updated_skills = batch_result.get("skills", "")
    if updated_skills:
        valid, reason = validate_fragment(skills_html, updated_skills)
        print(f"Skills validation: {reason}")
        if valid:
            current_html = replace_bullet_by_classes(current_html, skills_html, updated_skills)

    # Experience Bullets
    updated_exp = batch_result.get("experience_bullets", [])
    for idx, original in enumerate(exp_bullet_strings):
        if idx < len(updated_exp):
            updated = updated_exp[idx]
            valid, reason = validate_fragment(original, updated)
            print(f"Exp Bullet {idx+1} validation: {reason}")
            if valid:
                current_html = replace_bullet_by_classes(current_html, original, updated)

    # Project Bullets
    updated_proj = batch_result.get("project_bullets", [])
    for idx, original in enumerate(proj_bullet_strings):
        if idx < len(updated_proj):
            updated = updated_proj[idx]
            valid, reason = validate_fragment(original, updated)
            print(f"Proj Bullet {idx+1} validation: {reason}")
            if valid:
                current_html = replace_bullet_by_classes(current_html, original, updated)

    return current_html


def optimize_resume(
        html,
        jd,
        progress_callback=None):

    def emit(step_id, progress, message, extra=None):
        if progress_callback:
            try:
                progress_callback(step_id, progress, message, extra)
            except TypeError:
                try:
                    progress_callback(step_id, progress, message)
                except Exception as err:
                    print(f"Progress callback error: {err}")
            except Exception as err:
                print(f"Progress callback error: {err}")

    emit("init", 10, "Extracting resume structure & initial ATS audit...")

    initial_eval = evaluate_ats_score(html, jd)
    initial_score = initial_eval.get("ats_score", 0)
    print(f"Initial Resume ATS Score: {initial_score}/100")

    objective = extract_objective(html)
    objective_html = "\n".join(objective)

    skills = extract_skills(html)
    skills_html = "\n".join(skills)

    exp_bullets = extract_experience_bullets(html)
    exp_bullet_strings = ["\n".join(b) for b in exp_bullets]

    proj_bullets = extract_project_bullets(html)
    proj_bullet_strings = ["\n".join(b) for b in proj_bullets]

    TARGET_SCORE = 80
    MAX_ITERATIONS = 3
    iteration = 0

    current_html = html
    feedback = None
    missing_keywords = None
    eval_result = initial_eval
    current_score = initial_score
    score_history = [initial_score]

    while iteration < MAX_ITERATIONS:
        iteration += 1
        progress_base = 20 + (iteration - 1) * 20

        emit(
            "optimization",
            progress_base,
            f"Pass {iteration}/{MAX_ITERATIONS}: Optimizing resume content...",
            {"ats_score": current_score, "iteration": iteration}
        )

        batch_result = optimize_resume_batch(
            objective_html,
            skills_html,
            exp_bullet_strings,
            proj_bullet_strings,
            jd,
            feedback=feedback,
            missing_keywords=missing_keywords
        )

        current_html = apply_updates_to_html(
            html,
            batch_result,
            objective_html,
            skills_html,
            exp_bullet_strings,
            proj_bullet_strings
        )

        emit(
            "ats_eval",
            progress_base + 12,
            f"Pass {iteration}/{MAX_ITERATIONS}: Evaluating ATS match score...",
            {"ats_score": current_score, "iteration": iteration}
        )

        eval_result = evaluate_ats_score(current_html, jd)
        current_score = eval_result.get("ats_score", 0)
        score_history.append(current_score)
        print(f"Pass {iteration} ATS Score: {current_score}/100")

        if current_score > TARGET_SCORE:
            emit(
                "ats_eval",
                85,
                f"Target achieved! ATS Score: {current_score}/100 (> {TARGET_SCORE})",
                {"ats_score": current_score, "iteration": iteration}
            )
            break
        else:
            feedback = eval_result.get("feedback", "")
            missing_keywords = eval_result.get("missing_keywords", [])
            emit(
                "refinement",
                progress_base + 18,
                f"ATS Score: {current_score}/100. Refining resume (Pass {iteration+1})...",
                {"ats_score": current_score, "missing_keywords": missing_keywords}
            )

    emit("assembly", 90, f"Finalizing PDF with ATS Score: {current_score}/100...")

    return {
        "html": current_html,
        "ats_score": current_score,
        "initial_score": initial_score,
        "iterations": iteration,
        "score_history": score_history,
        "breakdown": eval_result.get("breakdown", {}),
        "feedback": eval_result.get("feedback", ""),
        "missing_keywords": eval_result.get("missing_keywords", [])
    }
