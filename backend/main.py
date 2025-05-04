from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd
from io import BytesIO
import uvicorn
from rules import flag_transactions
from agent_transactions import transactions_agent
from agent_kyc import kyc_agent, kyc_agent_multimodal
from agent_tools import print_banner
import base64

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

@app.post("/kyc")
async def analyze_kyc(
    first_name: str = Form(...),
    last_name: str = Form(...),
    occupation: str = Form(...),
    image: UploadFile = File(...)
):
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Uploaded file must be an image.")

    image_bytes = await image.read()
    encoded_image = base64.b64encode(image_bytes).decode("utf-8")
    data_url = f"data:{image.content_type};base64,{encoded_image}"
    print(data_url)

    res,pep_results,adverse_media_results,court_cases_results = kyc_agent_multimodal(first_name, last_name, occupation, data_url)
    print(res)
    # Placeholder logic – replace with your actual KYC processing
    result = {
        "first_name": first_name,
        "last_name": last_name,
        "occupation": occupation,
        "image_filename": image.filename,
        "image_content_type": image.content_type,
        "image_size_bytes": len(image_bytes),
        "pep_results":pep_results,
        "adverse_media_results":adverse_media_results,
        "court_cases_results":court_cases_results,
        "kyc_result":res
    }

    return JSONResponse(content=result)



@app.post("/transactions")
async def analyze_transactions(file: UploadFile = File(...)):
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
        #df = kyc_agent(df)

        print_banner("Running Transactions Agent")
        df = transactions_agent(df)

        print_banner("Final DataFrame Output")
        print(df)
        
        return JSONResponse(content={"columns": df.columns.tolist()})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

if __name__=="__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)