import csv
import requests
import time
import os
import pandas as pd
from urllib.parse import quote

# Your CourtListener API key
API_KEY = 'e6a8dbdbc283626f78e03bc530ca69f0a63189d5'
API_URL = 'https://www.courtlistener.com/api/rest/v4/search/'

# Keywords to search for in case names
KEYWORDS = ['fraud', 'narcotics', 'drug trafficking', 'money laundering']

def search_courtlistener(name):
    """
    Search CourtListener for cases involving the given name and keywords.
    Returns True if any relevant cases are found.
    """

    query = name
    params = {
        'q': query,
        'order_by': 'dateFiled desc',
        'type': 'o',
        'page_size': 1
    }
    headers = {
        'Authorization': f'Token {API_KEY}'
    }
    response = requests.get(API_URL, headers=headers, params=params)
    if response.status_code == 200:
        print("success")
        data = response.json()
    
        return data
    else:
        print(f"Error querying CourtListener for {name}: {response.status_code}")
        return []

def process_transactions(max_transactions=5):
    """
    Process the input CSV file, flagging transactions associated with suspicious individuals.

    Args:
        max_transactions: Maximum number of transactions to process (for testing)
    """
    # Load data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(os.path.dirname(current_dir), 'data')
    input_csv = os.path.join(data_dir, 'input_data_flagged.csv')
    output_csv = os.path.join(data_dir, 'flagger_transactions_court.csv')

    print(f"Loading transactions from: {input_csv}")
    transactions_df = pd.read_csv(input_csv)

    # Limit the number of transactions for testing
    if max_transactions > 0:
        print(f"Processing only the first {max_transactions} transactions for testing")
        transactions_df = transactions_df.head(max_transactions)

    # Create a copy of the original transactions DataFrame
    result_df = transactions_df.copy()

    # Add the two new columns
    result_df['court_flagged'] = 'false'  # Default all to false
    result_df['court_reason'] = ''        # Default all reasons to empty string

    # Process each transaction
    flagged_count = 0

    # Create a dictionary to cache API results
    name_cache = {}

    for idx, row in result_df.iterrows():
        # Extract name from email address
        email = row['Email Address']
        name = ""

        if '@' in email:
            name_parts = email.split('@')[0].split('_')
            if len(name_parts) == 1:  # No underscores, try splitting by dot
                name_parts = email.split('@')[0].split('.')
            name = ' '.join([part.capitalize() for part in name_parts if not part.isdigit()])

        print(f"Checking {name}...")

        # Check cache first
        if name in name_cache:
            is_flagged = name_cache[name]
        else:
            # Only call API if not in cache
            is_flagged = search_courtlistener(name)
            name_cache[name] = is_flagged

        if is_flagged:
            result_df.at[idx, 'court_flagged'] = 'true'
            result_df.at[idx, 'court_reason'] = 'Match found in CourtListener for fraud-related case'
            print(f"Flagged: {name}")
            flagged_count += 1

    # Save to CSV in the data directory
    result_df.to_csv(output_csv, index=False)
    print(f"Saved flagged transactions to: {output_csv}")

    # Print summary
    print(f"Processed {len(result_df)} transactions, flagged {flagged_count} suspicious transactions.")

    # Print each flagged transaction with its reason
    if flagged_count > 0:
        print("-" * 100)
        for idx, row in result_df.iterrows():
            if row['court_flagged'] == 'true':
                # Display the full row of suspicious transactions
                print(f"Flagged Transaction:")
                for col, val in row.items():
                    print(f"{col}: {val}")
                print("-" * 100)

    return result_df

if __name__ == "__main__":
    # Process only 5 transactions for testing
    #process_transactions(max_transactions=5)
    res = search_courtlistener("salvador madrigal")
    print(res)
    print("Processing complete.")

