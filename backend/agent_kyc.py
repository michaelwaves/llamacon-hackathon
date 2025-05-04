import os
from llama_api_client import LlamaAPIClient
from agent_tools import screen_for_pep, screen_for_adverse_media, print_banner
from courtlistener import search_courtlistener
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
import pandas as pd

class KYCScoring(BaseModel):
    kyc_risk_score: str
    kyc_rationale: str

load_dotenv()
""" client = LlamaAPIClient(
    api_key=os.getenv("LLAMA_API_KEY"),  # This is the default and can be omitted
) """

client = OpenAI(
    api_key=os.getenv("LLAMA_API_KEY"),
    base_url="https://api.llama.com/compat/v1/"
)

def kyc_agent(df):
    scores = []
    rationales = []
    for _, row in df.iterrows():
        firstname = row["first_name"]
        lastname = row["last_name"]
        occupation = row["occupation"]
        pep_results = screen_for_pep(firstname, lastname, occupation)
        adverse_media_results = screen_for_adverse_media(firstname, lastname, occupation)

        response = client.beta.chat.completions.parse(
            messages=[
                {
                    "content": f"""Given the profile {row.to_dict()}, and the search results for adverse_media {adverse_media_results} 
                    and pep {pep_results} return a kyc_risk_score from 0 to 100 and a kyc_rationale of a few sentences explaining why
                    
                    MUST RETURN JSON FORMAT WITH FIELDS
                    kyc_risk_score
                    kyc_rationale
                    """,
                    "role": "system",
                }
            ],
            model="Llama-4-Scout-17B-16E-Instruct-FP8",
            response_format=KYCScoring,
        )

        parsed = response.choices[0].message.parsed
        scores.append(parsed.kyc_risk_score)
        rationales.append(parsed.kyc_rationale)

    # Add new columns to the original DataFrame
    df = df.copy()
    df["kyc_risk_score"] = scores
    df["kyc_rationale"] = rationales

    return df

def kyc_agent_multimodal(firstname, lastname, occupation, image_url):
    print_banner("Fetching Politically Exposed Person Results")
    pep_results = screen_for_pep(firstname, lastname, occupation)
    print(f"✅ Found {len(pep_results)} PEP hits")

    print_banner("Fetching Adverse Media Results")
    adverse_media_results = screen_for_adverse_media(firstname, lastname, occupation)
    print(f"✅ Found {len(adverse_media_results)} Adverse Media hits")

    print_banner("Fetching Court Cases Results")
    court_cases_results = search_courtlistener(f"{firstname} {lastname}")
    print(f"✅ Found {len(court_cases_results)} Court Case hits")

    print_banner("Analyzing KYC case")
    response = client.beta.chat.completions.parse(
        messages=[
            {
                "role": "user",
                "content":[ 
                {"type":"text",
                     "text":f"""Given the profile {firstname} {lastname} with occupation {occupation} and image below, and the search results for adverse_media {adverse_media_results} 
               court cases {court_cases_results} and pep {pep_results} return a kyc_risk_score from 0 to 100 and a kyc_rationale of a few sentences explaining why
                
                MUST RETURN JSON FORMAT WITH FIELDS
                kyc_risk_score
                kyc_rationale
                """,
                },
                {
                    "type":"image_url",
                    "image_url":{
                        "url":image_url
                    }
                }],
               
            },
            

        ],
        model="Llama-4-Scout-17B-16E-Instruct-FP8",
        response_format=KYCScoring,
    )

    parsed = response.choices[0].message.parsed
    kyc_risk_score = parsed.kyc_risk_score
    kyc_rationale=parsed.kyc_rationale

    print(f"✅ Risk score of  {kyc_risk_score}/100 due to the following rationale:")
    print(kyc_rationale)

    return ({
        "risk_score":kyc_risk_score,
        "rationale":kyc_rationale
    }, pep_results, adverse_media_results, court_cases_results)


if __name__ == "__main__":  
    # Manually define Michael Yu's data
    michael_data = {
        "first_name": "Michael",
        "last_name": "Yu",
        "occupation": "Software Engineer"
    }

    # Convert to DataFrame
    df = pd.DataFrame([michael_data])
    print("Michael Yu DataFrame:")
    print(df)   

    df = kyc_agent(df)
    print(df)

