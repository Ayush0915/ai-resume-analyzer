def classify_skill_gaps(missing_skills, jd_skills):
    """
    Classify missing skills into Critical, Important, Optional
    """

    core_skills = [
        "python",
        "machine learning",
        "sql",
        "deep learning",
        "data structures",
        "algorithms"
    ]

    classification = {
        "critical": [],
        "important": [],
        "optional": []
    }

    for skill in missing_skills:

        if skill in core_skills:
            classification["critical"].append(skill)

        elif len(jd_skills) <= 5:
            classification["important"].append(skill)

        else:
            classification["optional"].append(skill)

    return classification