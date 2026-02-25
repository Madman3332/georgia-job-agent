from database import get_setting

def filter_jobs(jobs):

    min_salary = int(get_setting("min_salary"))
    keywords_raw = get_setting("keywords")
    keywords = [k.strip().lower() for k in keywords_raw.split(",")]

    filtered = []

    for job in jobs:

        title_match = any(
            keyword in job["title"].lower()
            for keyword in keywords
        )

        salary_ok = True

        if job["salary"] is not None:
            salary_ok = job["salary"] >= min_salary

        if title_match and salary_ok:
            filtered.append(job)

    return filtered