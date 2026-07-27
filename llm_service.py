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