import pandas as pd
import random
from faker import Faker
from uuid import uuid4
from datetime import timedelta

fake = Faker()

snake_case_headers = [
    "player_id", "tx_id", "psp_tx_id", "pan", "type", "request_date_utc", "update_date_utc",
    "payment_method", "amount", "amount_trx", "player_fee", "email_address", "nickname",
    "ip_address", "agent_fee", "tax", "sit", "bin_country", "country", "agent",
    "marketing_type", "status", "detail", "transaction_status", "auditor", "onboard_date"
]

def generate_random_transaction(sanctioned_entities, sanctioned_countries):
    player_id = str(uuid4())
    tx_id = str(uuid4())
    psp_tx_id = str(uuid4())
    pan = fake.credit_card_number()
    tx_type = random.choice(["deposit", "withdrawal"])
    
    request_date = fake.date_time_between(start_date='-30d', end_date='now')
    onboard_date = fake.date_time_between(start_date='-5y', end_date='now')

    update_date = request_date + timedelta(minutes=random.randint(1, 60))

    method = random.choice(["Visa", "MasterCard", "PayPal", "Crypto"])
    amount = round(random.uniform(10, 10000), 2)
    amount_trx = amount
    player_fee = round(amount * 0.01, 2)
    email = fake.email()
    nickname = fake.user_name()
    ip_address = fake.ipv4()
    agent_fee = round(amount * 0.02, 2)
    tax = round(amount * 0.05, 2)
    sit = fake.word()
    bin_country = fake.country_code()
    country = fake.country_code()
    agent = fake.name()
    marketing_type = random.choice(["email", "affiliate", "organic"])
    status = random.choice(["pending", "completed", "failed"])
    detail = fake.sentence()
    transaction_status = random.choice(["cleared", "held", "flagged"])
    auditor = fake.name()

    # Randomly inject a sanctioned entity
    if random.random() < 0.05 and sanctioned_entities:
        player_id = random.choice(sanctioned_entities)

    # Randomly inject a sanctioned country
    if random.random() < 0.05 and sanctioned_countries:
        bin_country = country = random.choice(sanctioned_countries)

    return [
        player_id, tx_id, psp_tx_id, pan, tx_type, request_date.isoformat(), update_date.isoformat(),
        method, amount, amount_trx, player_fee, email, nickname, ip_address, agent_fee, tax,
        sit, bin_country, country, agent, marketing_type, status, detail, transaction_status, auditor, onboard_date
    ]

def generate_dataset(n=1000, sanctioned_entities=None, sanctioned_countries=None, output_file="transactions.csv"):
    sanctioned_entities = sanctioned_entities or []
    sanctioned_countries = sanctioned_countries or []
    
    data = [generate_random_transaction(sanctioned_entities, sanctioned_countries) for _ in range(n)]
    df = pd.DataFrame(data, columns=snake_case_headers)
    df.to_csv(output_file, index=False)
    print(f"Generated {n} rows to {output_file}")

if __name__ == "__main__":
    generate_dataset(
        n=1000,
        sanctioned_entities=["sanctioned-player-123", "bad-actor-456"],
        sanctioned_countries=["IR", "KP", "RU"],
        output_file="sample_transactions.csv"
    )
