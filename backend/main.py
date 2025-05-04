from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
from io import BytesIO
import uvicorn
from rules import flag_transactions
from agent_transactions import transactions_agent
from agent_kyc import kyc_agent

app = FastAPI()

# Allow all CORS (not recommended for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Accept all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def print_banner(title: str):
    print("\n" + "=" * 40)
    print(f"{title.center(40)}")
    print("=" * 40 + "\n")

@app.get("/")
async def welcome():
    return {"message": "Welcome to the Transaction Monitoring AI API"}

@app.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    if not file.filename.endswith((".xlsx", ".xls", ".csv")):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload an Excel or csv file.")
    
    try:
        is_csv = file.filename.endswith(".csv")
        contents = await file.read()
        if is_csv:
            df  = pd.read_csv(BytesIO(contents))
        else:
            df = pd.read_excel(BytesIO(contents))  # Read file into pandas DataFrame
        # For now, just return the column names

        print_banner("Flagging Transactions")
        df = flag_transactions(df)

        print_banner("Running KYC Agent")
        df = kyc_agent(df)

        print_banner("Running Transactions Agent")
        df = transactions_agent(df)

        print_banner("Final DataFrame Output")
        print(df)
        
        return JSONResponse(content={"columns": df.columns.tolist()})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

if __name__=="__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)