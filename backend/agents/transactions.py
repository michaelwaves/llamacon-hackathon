import os
from llama_api_client import LlamaAPIClient
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
import pandas as pd

class TransactionScoring(BaseModel):
    transactions_risk_scores: list[str] #0 to 100
    transactions_rationales: list[str]

risk_scores = [50,100,60]
rationales = ["reason 1","reason 2"]

combined =[{"risk_score":50,"rationale":"reason 1"}]
load_dotenv()
""" client = LlamaAPIClient(
    api_key=os.getenv("LLAMA_API_KEY"),  # This is the default and can be omitted
) """

client = OpenAI(
    api_key=os.getenv("LLAMA_API_KEY"),
    base_url="https://api.llama.com/compat/v1/"
)


def transactions_agent(df:pd.DataFrame )->pd.DataFrame:
