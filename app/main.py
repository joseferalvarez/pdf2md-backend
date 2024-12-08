from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.concurrency import run_in_threadpool
import tempfile
import pymupdf4llm
import requests
import os

app = FastAPI(root_path="/api")

api_env = os.getenv("API_ENV", "DEV")

origins = ["*"]

if api_env == "PROD":
  origins = ["https://pdf2md.joseferalvarez.dev"]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=False,
  allow_methods=["POST"],
  allow_headers=["*"]
)

class BaseURL(BaseModel):
  url: str

@app.post("/v1/file/")
async def upload_file(file: UploadFile):
  file_bytes = await file.read()

  if len(file.filename.split(".")) < 2 or file.filename.split(".")[1] != "pdf":
      return {"file": "You can only upload pdf files"}

  with tempfile.NamedTemporaryFile(delete=True, mode="w+b", suffix="pdf") as temp_file:

    if not temp_file or not temp_file.name:
      return {"file": "The file can not be converted"}
    
    temp_file.write(file_bytes)

    md_file = await run_in_threadpool(pymupdf4llm.to_markdown, temp_file.name)
    return {"file": md_file.encode()}
  
  return {"file": "The file can not be converted"}

@app.post("/v1/url/")
async def download_file(req: BaseURL):
  res = requests.get(req.url)
  pdf_content = res.content

  with tempfile.NamedTemporaryFile(delete=True, mode="w+b", suffix="pdf") as temp_file:

    if not temp_file or not temp_file.name:
      return {"file": "The file can not be converted"}
    
    temp_file.write(pdf_content)

    md_file = await run_in_threadpool(pymupdf4llm.to_markdown, temp_file.name)
    return {"file": md_file.encode()}
  
  return {"file": "The file can not be extracted"}



  
  
