from fastapi import FastAPI, File, UploadFile, HTTPException, Form # Added Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
from io import BytesIO
import uvicorn
import random # Added for placeholder risk score
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
    # first name last name, occupations and 3 text field, image
    # return description and risk score
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

# New endpoint for profile analysis
@app.post("/api/analyze_profile")
async def analyze_profile(
    firstName: str = Form(...),
    lastName: str = Form(...),
    occupation: str = Form(...),
    textField1: str = Form(...),
    textField2: str = Form(...),
    textField3: str = Form(...),
    image: UploadFile = File(...) # Keep receiving the image, but don't process it
):
    print_banner("Received Profile Analysis Request")
    print(f"First Name: {firstName}")
    print(f"Last Name: {lastName}")
    print(f"Occupation: {occupation}")
    print(f"Text Field 1: {textField1}")
    print(f"Text Field 2: {textField2}")
    print(f"Text Field 3: {textField3}")
    print(f"Image Filename: {image.filename}")
    print(f"Image Content Type: {image.content_type}")

    # Placeholder for actual analysis logic
    # TODO: Implement actual profile analysis using the provided data (excluding image for now)
    # This might involve processing text fields, calling KYC agents, etc.
    # await image.read() # Temporarily disabled image processing
    print("Image received but processing is currently disabled.")

    # Simulate analysis result (without image analysis)
    # Replace with actual logic
    placeholder_description = f"Analysis for {firstName} {lastName} ({occupation}). Additional info processed. Image analysis is currently disabled."
    placeholder_risk_score = random.randint(5, 95) # Generate a random score for now

    print(f"Generated Description: {placeholder_description}")
    print(f"Generated Risk Score: {placeholder_risk_score}")

    return JSONResponse(content={
        "description": placeholder_description,
        "riskScore": placeholder_risk_score
    })


if __name__=="__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)