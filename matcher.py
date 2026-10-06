from llm_service import match_resume_with_jd_llm


def match_resume_with_jd(resume_data, resume_text, jd_data):

    print("Starting semantic resume-JD matching...")

    result = match_resume_with_jd_llm(
        resume_data,
        resume_text,
        jd_data
    )

    return result