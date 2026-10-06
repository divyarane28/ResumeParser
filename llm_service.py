from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
import json
import re

print("LLM file imported")

load_dotenv()

API_KEY = os.getenv("HF_API_KEY")

client = InferenceClient(
    api_key=API_KEY,
    timeout=120
)


def parse_resume(resume_text):

    print("Calling Hugging Face...")

    prompt = f"""
You are an expert Resume Parser.

Extract ONLY the following fields.

Return ONLY valid JSON.

Do NOT include markdown.
Do NOT explain anything.
Do NOT include projects.
Do NOT include certifications.
Do NOT include responsibilities.
Do NOT include descriptions.

Return exactly this format:

{{
  "name":"",
  "email":"",
  "phone":"",
  "skills":[],
  "education":[],
  "experience":[]
}}

Resume:

{resume_text}
"""

    response = client.chat.completions.create(
        model="meta-llama/Llama-3.1-8B-Instruct",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        max_tokens=3000
    )

    result = response.choices[0].message.content

    print(result)

    result = result.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(result)

    except Exception:

        match = re.search(r"\{[\s\S]*\}", result)

        if not match:
         return {
        "error": "No valid JSON found",
        "raw_response": result
        }

        if match:
            return json.loads(match.group())

        return {
            "error": "JSON Parsing Failed",
            "raw_response": result
        }

def parse_job_description(jd_text):

    print("Analyzing Job Description...")

    prompt = f"""

You are an expert Job Description Parser.

Extract the important requirements from the following Job Description.

Return ONLY valid JSON.

Do NOT include markdown.
Do NOT explain anything.

Return exactly this format:

{{
  "required_skills": [],
  "preferred_skills": [],
  "experience": "",
  "education": ""
}}

Job Description:

{jd_text}

"""

    response = client.chat.completions.create(
        model="meta-llama/Llama-3.1-8B-Instruct",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        max_tokens=1000
    )

    result = response.choices[0].message.content

    print("JD LLM Response:")
    print(result)

    result = result.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(result)

    except Exception:

        match = re.search(r"\{.*\}", result, re.DOTALL)

        if not match:

            return {
                "error": "No valid JSON found",
                "raw_response": result
            }

        return json.loads(match.group())



def match_resume_with_jd_llm(
    resume_data,
    resume_text,
    jd_data
):

    print("LLM Resume-JD Matching Started...")

    resume_skills = resume_data.get("skills", [])

    required_skills = jd_data.get("required_skills", [])

    preferred_skills = jd_data.get("preferred_skills", [])

    prompt = f"""

You are an expert technical recruiter and resume matching system.

Your task is to evaluate whether a candidate has each skill required by a job description.

Use the candidate's ENTIRE resume content as evidence.

The resume may mention skills in:

- Skills section
- Work experience
- Responsibilities
- Projects
- Technical work
- Other relevant sections

Do NOT assume that a skill is missing simply because it is not present in the Skills section.

Use contextual and semantic understanding.

IMPORTANT MATCHING RULES:

1. Exact skill match

Example:

Resume:
SQL

JD:
SQL

Status:
MATCHED

2. Equivalent skill names

Examples:

Microsoft Excel = Excel = MS Excel

Power BI = PowerBI

Status:
MATCHED

3. Combined skills

Example:

JD:
VLOOKUP/XLOOKUP

Resume:
VLOOKUP
XLOOKUP

Status:
MATCHED

Do NOT mark VLOOKUP or XLOOKUP as missing in this situation.

4. Technology versions

Example:

Resume:
Python

JD:
Python 3.11

Status:
MATCHED

If the resume specifies a different version:

Resume:
Python 3.10

JD:
Python 3.11

Status:
VERSION_MISMATCH

The base technology is still considered matched.

5. Do not create false matches.

Examples:

C is NOT automatically the same as C#.

C is NOT automatically the same as CSS.

6. Evidence matters.

If SQL is not listed in the Skills section but the resume says:

"Developed SQL queries and stored procedures"

then SQL should be considered MATCHED.

7. Projects are valid evidence.

Example:

Project:
"Sales analysis using Python and Pandas"

JD:
Python

Status:
MATCHED

8. Do not infer skills without evidence.

If a skill is not explicitly mentioned or strongly supported by the resume context, mark it as MISSING.

9. For every required skill, return exactly ONE result.

Possible statuses:

MATCHED
MISSING
VERSION_MISMATCH

10. Do not return the same JD skill in both MATCHED and MISSING.

11. Do not split a combined JD skill into contradictory results.

For example:

JD:
VLOOKUP/XLOOKUP

Resume:
VLOOKUP, XLOOKUP

Return one result:

VLOOKUP/XLOOKUP → MATCHED

12. Do not calculate match percentage.

Python will calculate the percentage.

13. Return ONLY valid JSON.

14. Do NOT return markdown.

15. Do NOT return explanations.

16. Do NOT add comments.

17. Do NOT add text before or after the JSON.

Return exactly this structure:

{{
    "required_skill_analysis": [
        {{
            "jd_skill": "",
            "status": "MATCHED",
            "evidence": ""
        }}
    ],
    "preferred_skill_analysis": [
        {{
            "jd_skill": "",
            "status": "MATCHED",
            "evidence": ""
        }}
    ],
    "version_mismatches": [
        {{
            "skill": "",
            "resume_version": "",
            "required_version": ""
        }}
    ]
}}

Candidate's extracted skills:

{resume_skills}

Required job skills:

{required_skills}

Preferred job skills:

{preferred_skills}

Full candidate resume:

{resume_text}

"""

    response = client.chat.completions.create(
        model="meta-llama/Llama-3.1-8B-Instruct",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        max_tokens=2500
    )

    result = response.choices[0].message.content

    print("LLM Matching Response:")
    print(result)

    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()

    try:

        llm_result = json.loads(result)

    except json.JSONDecodeError:

        print("Direct JSON parsing failed.")

        match = re.search(
            r"\{.*\}",
            result,
            re.DOTALL
        )

        if not match:

            return {
                "error": "No valid JSON found",
                "raw_response": result
            }

        json_text = match.group()

        json_text = re.sub(
            r'//.*',
            '',
            json_text
        )

        try:

            llm_result = json.loads(json_text)

        except json.JSONDecodeError as e:

            print("JSON parsing failed again.")
            print("Error:", e)

            return {
                "error": "Invalid JSON returned by LLM",
                "raw_response": result
            }


    # ---------------------------------
    # Convert LLM result for frontend
    # ---------------------------------

    required_analysis = llm_result.get(
        "required_skill_analysis",
        []
    )

    preferred_analysis = llm_result.get(
        "preferred_skill_analysis",
        []
    )


    matched_required_skills = []

    missing_required_skills = []


    for item in required_analysis:

        skill = item.get("jd_skill", "").strip()

        status = item.get("status", "").upper()


        if not skill:
            continue


        if status in ["MATCHED", "VERSION_MISMATCH"]:

            matched_required_skills.append(skill)

        elif status == "MISSING":

            missing_required_skills.append(skill)


    matched_preferred_skills = []


    for item in preferred_analysis:

        skill = item.get("jd_skill", "").strip()

        status = item.get("status", "").upper()


        if not skill:
            continue


        if status in ["MATCHED", "VERSION_MISMATCH"]:

            matched_preferred_skills.append(skill)


    # ---------------------------------
    # Calculate percentage using Python
    # ---------------------------------

    total_required = len(required_analysis)

    matched_required = len(
        matched_required_skills
    )


    if total_required > 0:

        match_percentage = round(
            (matched_required / total_required) * 100,
            2
        )

    else:

        match_percentage = 0


    return {

        "match_percentage": match_percentage,

        "matched_required_skills":
            matched_required_skills,

        "missing_required_skills":
            missing_required_skills,

        "matched_preferred_skills":
            matched_preferred_skills,

        "version_mismatches":
            llm_result.get(
                "version_mismatches",
                []
            )

    }
    