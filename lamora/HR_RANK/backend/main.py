from fastapi import FastAPI, UploadFile, File, Body
from fastapi.middleware.cors import CORSMiddleware
from utils.extractor import extract_resume_text, query_groq
from utils.calendar_utils import schedule_interview_event
from starlette.concurrency import run_in_threadpool
from fastapi.responses import JSONResponse
import uvicorn
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/parse_resume/")
async def parse_resume(file: UploadFile = File(...), job_description: str = ""):
    try:
        content = await file.read()
        text = extract_resume_text(content)
        
        # Debug log
        print(f"Extracted text length: {len(text)}")
        print("First 200 characters:", text[:200])

        prompt = f"""
Analyze this resume against the job description and return a JSON response.

Resume text:
{text[:5000]}  # Limit text length to avoid API limits

Job Description:
{job_description}

Return a JSON object in this exact format:
{{
    "candidates": [
        {{
            "name": "Extracted Name",
            "email": "Extracted Email",
            "why_top": "Brief explanation of match",
            "ranking": 1
        }}
    ]
}}
"""

        raw_response = await run_in_threadpool(query_groq, prompt)

        try:
            result = json.loads(raw_response.strip())
            return {"result": result}
        except json.JSONDecodeError as e:
            print(f"JSON Parse Error: {str(e)}")
            print("Raw response:", raw_response)
            return JSONResponse(
                content={
                    "error": "Failed to parse JSON from model",
                    "details": str(e),
                    "raw": raw_response
                },
                status_code=400
            )
    except Exception as e:
        print(f"General Error: {str(e)}")
        return JSONResponse(
            content={"error": f"Error processing request: {str(e)}"},
            status_code=500
        )

import traceback

@app.post("/schedule_meeting/")
async def schedule_meeting(data: dict = Body(...)):
    name = data.get("name")
    email = data.get("email")
    if not name or not email:
        return JSONResponse(content={"error": "Missing name or email"}, status_code=400)

    try:
        result = schedule_interview_event(name, email)
        return {"success": True, "event": result}
    except Exception as e:
        traceback.print_exc()  # This prints the full error to terminal
        return JSONResponse(content={"success": False, "error": str(e)}, status_code=500)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
