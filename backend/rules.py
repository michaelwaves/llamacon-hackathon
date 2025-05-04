import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import re
import os

# Define high-income occupations (typically earning >100k/year)
HIGH_INCOME_OCCUPATIONS = [
    'Software Engineer',
    'Financial Advisor',
    'Banking - Financial Analyst',
    'Compliance Officer',
    'Investment Banker',
    'Physician',
    'Surgeon',
    'Lawyer',
    'Senior Executive',
    'CEO',
    'CTO',
    'CFO',
    'Director'
]

def extract_amount(amount_str):
    """Extract numeric amount from CAD string format"""
    if pd.isna(amount_str):
        return 0

    # If it's already a number, return it
    if isinstance(amount_str, (int, float)):
        return float(amount_str)

    # Try to extract numeric value using regex
    match = re.search(r'(\d+(?:\.\d+)?)', str(amount_str))
    if match:
        return float(match.group(1))
    return 0

def flag_high_value_24h(transactions_df):
    """
    Flag transactions where total amount exceeds 10k in 24 hours by the same account
    """
    # Convert request date to datetime
    transactions_df['Request_Date'] = pd.to_datetime(transactions_df['Request Date (UTC)'], format='mixed')

    # Group by Player ID and date
    flagged_transactions = []

    # Get unique player IDs
    player_ids = transactions_df['Player ID'].unique()

    for player_id in player_ids:
        player_txns = transactions_df[transactions_df['Player ID'] == player_id].copy()

        # Sort by date
        player_txns = player_txns.sort_values('Request_Date')

        # For each transaction, check if total in 24 hours exceeds 10k
        for idx, txn in player_txns.iterrows():
            txn_date = txn['Request_Date']

            # Get all transactions within 24 hours
            start_time = txn_date - timedelta(hours=24)
            end_time = txn_date

            # Filter transactions in the 24-hour window
            window_txns = player_txns[(player_txns['Request_Date'] >= start_time) &
                                      (player_txns['Request_Date'] <= end_time)]

            # Calculate total amount
            total_amount = sum(extract_amount(amt) for amt in window_txns['Amount (TRX)'])

            if total_amount > 10000:
                # Flag this transaction
                flagged_transactions.append({
                    'Transaction': txn,
                    'Flag_Reason': f'Total transactions of ${total_amount:.2f} in 24 hours exceeds $10,000 threshold'
                })
                break  # Only flag once per player

    return flagged_transactions

def flag_high_value_single_transaction(transactions_df):
    """
    Flag transactions above 100k in a single transaction
    """
    flagged_transactions = []

    # Flag transactions above 100k
    for idx, txn in transactions_df.iterrows():
        amount = extract_amount(txn['Amount (TRX)'])

        # Check if amount > 100k
        if amount > 100000:
            flagged_transactions.append({
                'Transaction': txn,
                'Flag_Reason': f'Transaction amount ${amount:.2f} exceeds $100,000 threshold'
            })

    return flagged_transactions

def flag_high_volume_2days(transactions_df):
    """
    Flag accounts with 20+ transactions in the past 2 days
    """
    # Convert request date to datetime
    transactions_df['Request_Date'] = pd.to_datetime(transactions_df['Request Date (UTC)'], format='mixed')

    flagged_transactions = []

    # Get unique player IDs
    player_ids = transactions_df['Player ID'].unique()

    # Get the latest date in the dataset
    latest_date = transactions_df['Request_Date'].max()

    # Check each player's transaction count in the last 2 days
    for player_id in player_ids:
        player_txns = transactions_df[transactions_df['Player ID'] == player_id]

        # Filter transactions in the last 2 days
        two_days_ago = latest_date - timedelta(days=2)
        recent_txns = player_txns[player_txns['Request_Date'] >= two_days_ago]

        # If more than 20 transactions, flag all of them
        if len(recent_txns) >= 20:
            for idx, txn in recent_txns.iterrows():
                flagged_transactions.append({
                    'Transaction': txn,
                    'Flag_Reason': f'High volume: {len(recent_txns)} transactions in the past 2 days'
                })

    return flagged_transactions

def flag_sudden_activity(transactions_df):
    """
    Flag accounts with sudden transaction activity (multiple transactions in a short period)
    """
    # Convert request date to datetime
    transactions_df['Request_Date'] = pd.to_datetime(transactions_df['Request Date (UTC)'], format='mixed')

    flagged_transactions = []

    # Group by player ID
    player_groups = transactions_df.groupby('Player ID')

    for player_id, group in player_groups:
        # Sort transactions by date
        sorted_txns = group.sort_values('Request_Date')

        # If there are at least 3 transactions
        if len(sorted_txns) >= 3:
            oldest_txn_date = sorted_txns['Request_Date'].min()
            newest_txn_date = sorted_txns['Request_Date'].max()

            # If all transactions are within a 1-day window
            if (newest_txn_date - oldest_txn_date).days <= 1:
                for idx, txn in sorted_txns.iterrows():
                    flagged_transactions.append({
                        'Transaction': txn,
                        'Flag_Reason': f'Sudden activity: {len(sorted_txns)} transactions in {(newest_txn_date - oldest_txn_date).total_seconds() / 3600:.1f} hours'
                    })

    return flagged_transactions

def flag_velocity_2weeks(transactions_df):
    """
    Flag accounts where inflows-outflows <1000 in the past 2 weeks
    """
    # Convert request date to datetime
    transactions_df['Request_Date'] = pd.to_datetime(transactions_df['Request Date (UTC)'], format='mixed')

    flagged_transactions = []

    # Get the latest date in the dataset
    latest_date = transactions_df['Request_Date'].max()

    # Define the 2-week window
    two_weeks_ago = latest_date - timedelta(days=14)

    # Filter transactions in the last 2 weeks
    recent_txns = transactions_df[transactions_df['Request_Date'] >= two_weeks_ago].copy()

    # Group by player ID
    player_groups = recent_txns.groupby('Player ID')

    for player_id, group in player_groups:
        # Calculate inflows and outflows
        # Assuming withdrawals are negative (outflows) and deposits are positive (inflows)
        group['Amount_Value'] = group.apply(
            lambda row: -extract_amount(row['Amount (TRX)']) if row['Type'] == 'Withdrawal' else extract_amount(row['Amount (TRX)']),
            axis=1
        )

        # Calculate net flow
        net_flow = group['Amount_Value'].sum()

        # If net flow is less than 1000, flag all transactions
        if abs(net_flow) < 1000 and len(group) > 1:  # Only flag if there are multiple transactions
            for idx, txn in group.iterrows():
                flagged_transactions.append({
                    'Transaction': txn,
                    'Flag_Reason': f'Low net flow: ${abs(net_flow):.2f} in the past 2 weeks'
                })

    return flagged_transactions

def flag_sanctioned_individuals(transactions_df):
    """
    Flag transactions from sanctioned individuals
    """
    flagged_transactions = []

    try:
        # Load sanctions data from combined_sanctions.csv
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sanctions_csv = os.path.join(current_dir, 'data', 'sanctions', 'combined_sanctions.csv')
        print(f"Loading sanctions from: {sanctions_csv}")
        sanctions_df = pd.read_csv(sanctions_csv)

        # Check each transaction for sanctioned individuals
        for idx, txn in transactions_df.iterrows():
            # Extract the name from the email address
            email = txn['Email Address']
            name_parts = email.split('@')[0].split('_')
            name = ' '.join([part.capitalize() for part in name_parts if not part.isdigit()])

            # Check if the name is in the sanctions list
            for _, sanction in sanctions_df.iterrows():
                first_name = str(sanction['first_name']) if not pd.isna(sanction['first_name']) else ''
                last_name = str(sanction['last_name']) if not pd.isna(sanction['last_name']) else ''
                sanctioned_name = f"{first_name} {last_name}".strip()

                # Check aliases as well
                aliases = []
                if not pd.isna(sanction['aliases']):
                    try:
                        # Try to parse the aliases field as a list
                        import ast
                        alias_list = ast.literal_eval(sanction['aliases'])
                        for alias in alias_list:
                            if isinstance(alias, dict) and 'whole_name' in alias:
                                aliases.append(alias['whole_name'])
                    except:
                        pass

                # Check if name matches sanctioned name or any alias
                if (sanctioned_name and (sanctioned_name.lower() in name.lower() or name.lower() in sanctioned_name.lower())):
                    source = sanction['source'] if not pd.isna(sanction['source']) else 'Unknown'
                    programs = sanction['sanctions_programs'] if not pd.isna(sanction['sanctions_programs']) else ''

                    flagged_transactions.append({
                        'Transaction': txn,
                        'Flag_Reason': f'Sanctioned individual: {sanctioned_name} - Source: {source} - Programs: {programs}'
                    })
                    break

                # Check aliases
                for alias in aliases:
                    if alias and alias.lower() in name.lower() or name.lower() in alias.lower():
                        source = sanction['source'] if not pd.isna(sanction['source']) else 'Unknown'
                        programs = sanction['sanctions_programs'] if not pd.isna(sanction['sanctions_programs']) else ''

                        flagged_transactions.append({
                            'Transaction': txn,
                            'Flag_Reason': f'Sanctioned individual (alias match): {alias} - Source: {source} - Programs: {programs}'
                        })
                        break
    except Exception as e:
        print(f"Error checking sanctions: {e}")

    return flagged_transactions

def flag_transactions():
    """
    Main function to flag suspicious transactions based on defined rules
    """
    # Load data
    current_dir = os.path.dirname(os.path.abspath(__file__))
    transactions_csv = os.path.join(current_dir, 'data', 'transactions.csv')
    print(f"Loading transactions from: {transactions_csv}")
    transactions_df = pd.read_csv(transactions_csv)

    # Apply all flagging rules
    flagged_high_value_24h = flag_high_value_24h(transactions_df)
    flagged_high_value_single = flag_high_value_single_transaction(transactions_df)
    flagged_high_volume = flag_high_volume_2days(transactions_df)
    flagged_sudden = flag_sudden_activity(transactions_df)
    flagged_velocity = flag_velocity_2weeks(transactions_df)
    flagged_sanctions = flag_sanctioned_individuals(transactions_df)

    # Combine all flagged transactions
    all_flagged = (
        flagged_high_value_24h +
        flagged_high_value_single +
        flagged_high_volume +
        flagged_sudden +
        flagged_velocity +
        flagged_sanctions
    )

    # Create a set of flagged transaction IDs for quick lookup
    flagged_tx_ids = set()
    flagged_reasons = {}

    # Extract transaction IDs and reasons
    for item in all_flagged:
        tx_id = item['Transaction']['TX ID']
        flagged_tx_ids.add(tx_id)

        # Store the reason for flagging
        if tx_id in flagged_reasons:
            # If we already have a reason for this transaction, append the new reason
            flagged_reasons[tx_id] = flagged_reasons[tx_id] + "; " + item['Flag_Reason']
        else:
            flagged_reasons[tx_id] = item['Flag_Reason']

    # Create a copy of the original transactions DataFrame
    result_df = transactions_df.copy()

    # Remove the Request_Date column if it exists (it was added for internal processing)
    if 'Request_Date' in result_df.columns:
        result_df = result_df.drop(columns=['Request_Date'])

    # Add the two new columns
    result_df['flagged'] = 'false'  # Default all to false
    result_df['reason'] = ''        # Default all reasons to empty string

    # Update flagged transactions
    for tx_id in flagged_tx_ids:
        # Find rows with this transaction ID
        mask = result_df['TX ID'] == tx_id
        # Set flagged to true
        result_df.loc[mask, 'flagged'] = 'true'
        # Set the reason
        result_df.loc[mask, 'reason'] = flagged_reasons[tx_id]

    # Save to CSV in the data directory (same level as the source file)
    data_dir = os.path.join(current_dir, 'data')
    output_csv = os.path.join(data_dir, 'flagger_transactions.csv')
    result_df.to_csv(output_csv, index=False)
    print(f"Saved flagged transactions to: {output_csv}")

    # Print summary
    flagged_count = result_df['flagged'].value_counts().get('true', 0)
    print(f"Processed {len(result_df)} transactions, flagged {flagged_count} suspicious transactions.")

    # Print each flagged transaction with its reason
    if flagged_count > 0:
        print("-" * 100)
        for idx, row in transactions_df.iterrows():
            tx_id = row['TX ID']
            if tx_id in flagged_tx_ids:
                print(f"Transaction ID: {tx_id}")
                print(f"Player ID: {row['Player ID']}")
                print(f"Email: {row['Email Address']}")
                print(f"Amount: {row['Amount (TRX)']}")
                print(f"Date: {row['Request Date (UTC)']}")
                print(f"Flag Reason: {flagged_reasons[tx_id]}")
                print("-" * 100)

    return result_df

if __name__ == "__main__":
    flag_transactions()
