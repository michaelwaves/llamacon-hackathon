import os
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel
import pandas as pd
import json # Added import for JSON parsing

class TransactionScoring(BaseModel):
    transactions_risk_scores: list[int] # Changed from list[str] to list[int]
    transactions_rationales: list[str]

load_dotenv()
""" client = LlamaAPIClient(
    api_key=os.getenv("LLAMA_API_KEY"),  # This is the default and can be omitted
) """

client = OpenAI(
    api_key=os.getenv("LLAMA_API_KEY"),
    base_url="https://api.llama.com/compat/v1/"
)


<<<<<<< HEAD
def transactions_agent(df:pd.DataFrame )->pd.DataFrame:
    
=======
def transactions_agent(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analyzes transaction data using an LLM to generate risk scores and rationales.

    Args:
        df: Input DataFrame containing transaction data.

    Returns:
        DataFrame with added 'risk_score' and 'transaction_rationale' columns.
    """
    # 1. Format data for LLM (convert DataFrame to CSV string)
    # Select relevant columns for analysis (adjust as needed)
    relevant_columns = [
        'customer_id', 'tx_id', 'type', 'request_date_utc', 'payment_method',
        'amount', 'bin_country', 'country', 'first_name', 'last_name', 'occupation',
        'yearly_income', 'account_creation_date', 'birthdate', 'ip_address'
    ]
    # Ensure only existing columns are selected
    relevant_columns = [col for col in relevant_columns if col in df.columns]
    data_string = df[relevant_columns].to_csv(index=False)

    # 2. Craft LLM Prompt
    prompt = f"""Analyze the following transaction data (in CSV format) and provide a risk assessment for each transaction.
For each transaction, determine a risk score (integer between 0 and 100, where 100 is highest risk) and a brief rationale explaining the score.
Consider factors like transaction amount, type (withdrawal/deposit), countries involved (bin_country vs country), user information (occupation, income, account age), IP address, and potential patterns across transactions.

Data:
{data_string}

Output the results as a JSON object containing two lists:
1.  `transactions_risk_scores`: A list of integer risk scores, one for each transaction in the input order.
2.  `transactions_rationales`: A list of string rationales, one for each transaction in the input order, corresponding to the scores.

Example Output Format:
{{
  "transactions_risk_scores": [75, 20, 90, ...],
  "transactions_rationales": ["High amount withdrawal to high-risk country.", "Standard low-value deposit.", "Multiple large withdrawals in short period.", ...]
}}

Provide only the JSON object in your response.
"""

    # 3. Invoke LLM
    try:
        completion = client.chat.completions.create(
            model="Llama-3.3-70B-Instruct", # Or another suitable large context model
            messages=[
                {"role": "system", "content": "You are a financial transaction risk analyst. Analyze the provided data and return risk scores and rationales in the specified JSON format. Provide ONLY the JSON object in your response, with no other text before or after it."},
                {"role": "user", "content": prompt}
            ],
            # response_format={"type": "json_object"}, # Removed unsupported parameter
            temperature=0.2, # Lower temperature for more deterministic output
        )
        response_content = completion.choices[0].message.content

        # 4. Parse Response
        # Use Pydantic model for parsing and validation
        # Attempt to extract JSON from potentially messy response
        try:
            # Find the start and end of the JSON object
            json_start = response_content.find('{')
            json_end = response_content.rfind('}') + 1
            if json_start != -1 and json_end != 0:
                json_string = response_content[json_start:json_end]
                parsed_response = TransactionScoring.model_validate_json(json_string)
            else:
                raise ValueError("Could not find JSON object in the LLM response.")
        except (json.JSONDecodeError, ValueError) as json_error:
             print(f"Error parsing JSON from LLM response: {json_error}")
             print(f"Raw response content:\n{response_content}")
             raise json_error # Re-raise after printing details

        scores = parsed_response.transactions_risk_scores
        rationales = parsed_response.transactions_rationales

        # Basic validation
        if len(scores) != len(df) or len(rationales) != len(df):
            raise ValueError(f"LLM response length mismatch: Expected {len(df)}, got {len(scores)} scores and {len(rationales)} rationales.")
        if not all(isinstance(s, int) or (isinstance(s, str) and s.isdigit()) for s in scores):
             raise ValueError("LLM response format error: Risk scores are not all integers.")
        if not all(isinstance(r, str) for r in rationales):
             raise ValueError("LLM response format error: Rationales are not all strings.")


        # 5. Update DataFrame
        df['risk_score'] = [int(s) for s in scores] # Ensure scores are integers
        df['transaction_rationale'] = rationales

    except Exception as e:
        print(f"Error during LLM processing or parsing: {e}")
        # Handle error case, e.g., return df with empty/default columns
        df['risk_score'] = pd.NA
        df['transaction_rationale'] = pd.NA

    # 6. Return DataFrame
    return df

# Example Usage (optional, for testing)
if __name__ == '__main__':
    # Load the data
    input_csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'input_data.csv')
    output_csv_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'output_data_with_scores.csv') # Define output path

    if os.path.exists(input_csv_path):
        input_df = pd.read_csv(input_csv_path)
        # Process the entire DataFrame, not just a subset
        # input_df_subset = input_df.head(5) # Removed subsetting
        print(f"Input DataFrame loaded with {len(input_df)} rows.")
        # print(input_df_subset)

        # Run the agent on the full DataFrame
        # Use copy to avoid modifying original if needed elsewhere, though not strictly necessary here
        output_df = transactions_agent(input_df.copy())

        print("\\nOutput DataFrame with Risk Scores and Rationales:")
        # Print head to avoid overwhelming console for large files
        print(output_df[['tx_id', 'risk_score', 'transaction_rationale']].head())

        # Save the entire output DataFrame to a new CSV
        try:
            output_df.to_csv(output_csv_path, index=False)
            print(f"\\nSuccessfully saved output to {output_csv_path}")
        except Exception as e:
            print(f"\\nError saving output file: {e}")

    else:
        print(f"Error: Input CSV not found at {input_csv_path}")
>>>>>>> a89dce959524bb1da4dd86a8e42c943ceb55fd5e
