import os
from llama_api_client import LlamaAPIClient
from tools import screen_for_pep, screen_for_adverse_media
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

class KYCScoring(BaseModel):
    kyc_risk_score: list[str]
    kyc_rationale: list[str]


load_dotenv()
""" client = LlamaAPIClient(
    api_key=os.getenv("LLAMA_API_KEY"),  # This is the default and can be omitted
) """

client = OpenAI(
    api_key=os.getenv("LLAMA_API_KEY"),
    base_url="https://api.llama.com/compat/v1/"
)

def kyc_agent(df):
    for index, row in df.iterrows():
        firstname = row["first_name"]
        lastname = row["last_name"]
        occupation = row["occupation"]

        pep_results = screen_for_pep(firstname, lastname, occupation)
        adverse_media_results = screen_for_adverse_media(firstname, lastname, occupation)

pep_response = client.responses.parse(
    messages=[
        {
            "content": f"Given the adverse media search results ",
            "role": "system",
        }
    ],
    model="Llama-4-Scout-17B-16E-Instruct-FP8",
)

if __name__ == "__main__":  
    print(pep_response.completion_message)