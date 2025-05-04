import pandas as pd
from datetime import timedelta

# Example list of sanctioned individuals
SANCTIONED_NAMES = {'john doe', 'jane smith', 'ivan petrov'}

def extract_amount(value):
    try:
        return float(str(value).replace('$', '').replace(',', ''))
    except:
        return 0.0

def flag_high_value_24h(df):
    df['request_date'] = pd.to_datetime(df['request_date_utc'], format='mixed')
    flagged = []

    for customer_id in df['customer_id'].unique():
        txns = df[df['customer_id'] == customer_id].sort_values('request_date')

        for i, txn in txns.iterrows():
            window_start = txn['request_date'] - timedelta(hours=24)
            window = txns[(txns['request_date'] >= window_start) & (txns['request_date'] <= txn['request_date'])]
            total = sum(extract_amount(amt) for amt in window['amount_trx'])
            if total > 10000:
                flagged.append({
                    'Transaction': txn,
                    'Flag_Reason': f'Total transactions of ${total:.2f} in 24h exceeds $10,000'
                })
                break
    return flagged

def flag_high_value_single_transaction(df):
    flagged = []
    for _, txn in df.iterrows():
        amount = extract_amount(txn['amount_trx'])
        if amount > 5000:
            flagged.append({
                'Transaction': txn,
                'Flag_Reason': f'Single transaction amount ${amount:.2f} exceeds $5,000'
            })
    return flagged

def flag_high_volume_2days(df):
    df['request_date'] = pd.to_datetime(df['request_date_utc'], format='mixed')
    flagged = []

    for customer_id in df['customer_id'].unique():
        txns = df[df['customer_id'] == customer_id].sort_values('request_date')

        for i, txn in txns.iterrows():
            window_start = txn['request_date'] - timedelta(days=2)
            count = txns[(txns['request_date'] >= window_start) & (txns['request_date'] <= txn['request_date'])].shape[0]
            if count > 5:
                flagged.append({
                    'Transaction': txn,
                    'Flag_Reason': f'More than 5 transactions in 48h window'
                })
                break
    return flagged

def flag_sudden_activity(df):
    df['request_date'] = pd.to_datetime(df['request_date_utc'], format='mixed')
    flagged = []

    for customer_id in df['customer_id'].unique():
        txns = df[df['customer_id'] == customer_id].sort_values('request_date')
        if len(txns) < 3:
            continue

        latest_txns = txns[txns['request_date'] > txns['request_date'].max() - timedelta(days=1)]
        earlier_txns = txns[txns['request_date'] <= txns['request_date'].max() - timedelta(days=1)]

        if len(latest_txns) >= 3 and len(earlier_txns) == 0:
            flagged.append({
                'Transaction': latest_txns.iloc[0],
                'Flag_Reason': 'Sudden activity: 3+ txns in 1 day, none before'
            })
    return flagged

def flag_velocity_2weeks(df):
    df['request_date'] = pd.to_datetime(df['request_date_utc'], format='mixed')
    flagged = []

    two_weeks_ago = df['request_date'].max() - timedelta(days=14)
    df_recent = df[df['request_date'] >= two_weeks_ago]

    for customer_id in df_recent['customer_id'].unique():
        txns = df_recent[df_recent['customer_id'] == customer_id]
        active_days = txns['request_date'].dt.date.nunique()
        if active_days >= 10:
            flagged.append({
                'Transaction': txns.iloc[0],
                'Flag_Reason': f'Customer active on {active_days} days in past 14'
            })
    return flagged

def flag_sanctioned_individuals(df):
    flagged = []
    for _, txn in df.iterrows():
        full_name = f"{str(txn['first_name']).strip().lower()} {str(txn['last_name']).strip().lower()}"
        if full_name in SANCTIONED_NAMES:
            flagged.append({
                'Transaction': txn,
                'Flag_Reason': 'Customer matched sanctioned individual'
            })
    return flagged

def flag_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Flag suspicious transactions in a given dataframe.

    Returns:
        The same dataframe with added 'flagged' and 'reason' columns.
    """
    df['request_date'] = pd.to_datetime(df['request_date_utc'], format='mixed')

    flagged_all = (
        flag_high_value_24h(df) +
        flag_high_value_single_transaction(df) +
        flag_high_volume_2days(df) +
        flag_sudden_activity(df) +
        flag_velocity_2weeks(df) +
        flag_sanctioned_individuals(df)
    )

    flagged_ids = set()
    reasons = {}
    for item in flagged_all:
        tx_id = item['Transaction']['tx_id']
        flagged_ids.add(tx_id)
        reasons[tx_id] = reasons.get(tx_id, '') + '; ' + item['Flag_Reason'] if tx_id in reasons else item['Flag_Reason']

    df['flagged'] = df['tx_id'].apply(lambda x: 'true' if x in flagged_ids else 'false')
    df['reason'] = df['tx_id'].apply(lambda x: reasons.get(x, ''))

    return df

if __name__== "__main__":
    df = pd.read_csv("./data/input_data.csv")
    print(df.columns)
    df = flag_transactions(df)
    print(df)

