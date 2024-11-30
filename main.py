from fastapi import FastAPI, UploadFile
from fastapi.concurrency import run_in_threadpool
import tempfile
import pymupdf4llm

app = FastAPI()

@app.post("/upload/")
async def post_file(file: UploadFile):
  file_bytes = await file.read()

  with tempfile.NamedTemporaryFile(delete=True, mode="w+b") as temp_file:
    temp_file.write(file_bytes)
    temp_filename = temp_file.name

    md_file = await run_in_threadpool(pymupdf4llm.to_markdown, temp_filename)
    return {"file": md_file.encode()}
  
  return {"file": "The file can not be converted"}



  
  
