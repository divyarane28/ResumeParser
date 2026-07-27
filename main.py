from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from parser import extract_text_from_pdf
from llm_service import parse_resume
print("1 Main Started")

import shutil
import os

app = FastAPI()

print("2 FastAPI Created")

app.mount("/static", StaticFiles(directory="static"), name="static")
print("3 Static Mounted")

templates = Jinja2Templates(directory="templates")
print("4 Templates Ready")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    print("5 Home Route Called")
    return templates.TemplateResponse(
        request=request,
        name="index.html"
    )


@app.post("/upload")
async def upload_resume(file: UploadFile = File(...)):

    print("STEP 1 : Upload started")

    os.makedirs("uploads", exist_ok=True)

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    print("STEP 2 : File saved")

    resume_text = extract_text_from_pdf(file_path)

    print("STEP 3 : PDF text extracted")

    parsed_data = parse_resume(resume_text)

    print("STEP 4 : LLM finished")

    return {
        "message": "Resume parsed successfully!",
        "filename": file.filename,
        "parsed_data": parsed_data
    }

@app.post("/submit")
async def submit_candidate(request: Request):

    data = await request.json()

    print(data)

    return {
        "message":"Candidate saved successfully!"
    }

@app.get("/candidate", response_class=HTMLResponse)
async def candidate_page(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="candidate.html"
    )