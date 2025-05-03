from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
from io import BytesIO

app = FastAPI()

# Allow all CORS (not recommended for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Accept all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def welcome():
    return {"message": "Welcome to the Transaction Monitoring AI API"}

@app.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    if not file.filename.endswith((".xlsx", ".xls")):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload an Excel file.")
    
    try:
        contents = await file.read()
        df = pd.read_excel(BytesIO(contents))  # Read file into pandas DataFrame
        # For now, just return the column names
        return JSONResponse(content={"columns": df.columns.tolist()})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
