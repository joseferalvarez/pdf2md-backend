from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from fastapi.concurrency import run_in_threadpool
import os
import tempfile
import pymupdf4llm
import requests

app = FastAPI()

class BaseURL(BaseModel):
  url: str

@app.post("/api/v1/file/")
async def upload_file(file: UploadFile):
  file_bytes = await file.read()

  with tempfile.NamedTemporaryFile(delete=True, mode="w+b") as temp_file:
    temp_file.write(file_bytes)

    md_file = await run_in_threadpool(pymupdf4llm.to_markdown, temp_file.name)
    return {"file": md_file.encode()}
  
  return {"file": "The file can not be converted"}

@app.post("/api/v1/url/")
async def download_file(req: BaseURL):
  res = requests.get(req.url)
  pdf_content = res.content

  with tempfile.NamedTemporaryFile(delete=True, mode="w+b", suffix=".pdf") as temp_file:
    temp_file.write(pdf_content)

    md_file = await run_in_threadpool(pymupdf4llm.to_markdown, temp_file.name)
    return {"file": md_file.encode()}
  
  return {"file": "The file can not be extracted"}



  
  
