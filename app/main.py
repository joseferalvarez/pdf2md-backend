from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fastapi.concurrency import run_in_threadpool
import tempfile
import pymupdf4llm
from pymupdf import Document
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
  pdf_content = await file.read()

  if len(file.filename.split(".")) < 2 or file.filename.split(".")[1] != "pdf":
      return {"file": "You can only upload pdf files"}

  md_content = get_md_content(pdf_content=pdf_content)

  return {"file": md_content}

@app.post("/v1/url/")
async def download_file(req: BaseURL):
  res = requests.get(req.url)
  pdf_content = res.content

  md_content = get_md_content(pdf_content=pdf_content)

  return {"file": md_content}
  

def get_md_content(pdf_content):
  try:
    pdf_document = Document(filename='doc.pdf', stream=pdf_content)

    md_file = pymupdf4llm.to_markdown(pdf_document)

    return md_file.encode()
  except:
    return "Ha habido un error al convertir el pdf"



  
  
