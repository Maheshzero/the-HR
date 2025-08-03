from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from utils.extractor import extract_resume_text, query_groq
import uvicorn
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.extractor import extract_resume_text, query_groq

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/parse_resume/")
async def parse_resume(file: UploadFile = File(...), job_description: str = ""):
    content = await file.read()
    text = extract_resume_text(content)

    prompt = f"You're an HR expert. Match the resume below to the job description and give a score out of 10. Highlight relevant skills and experience.\n\nJob Description:\n{job_description}\n\nResume:\n{text}"
    
    result = query_groq(prompt)
    return {"result": result}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
