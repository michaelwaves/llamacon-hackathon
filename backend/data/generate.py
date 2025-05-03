import pandas as pd
import random
from faker import Faker
from uuid import uuid4
from datetime import timedelta

fake = Faker()

transaction_headers = [
    "customer_id", "tx_id", "psp_tx_id", "pan", "type", "request_date_utc", "update_date_utc",
    "payment_method", "amount", "amount_trx", "customer_fee", "email_address", "nickname",
    "ip_address", "agent_fee", "tax", "sit", "bin_country", "country", "agent",
    "marketing_type", "status", "detail", "transaction_status", "auditor", "onboard_date"
]

customer_headers = [
    "customer_id", "first_name", "last_name", "username_nickname", "account_creation_date", "birthdate",
    "email", "login_date_and_time", "address_unit", "address_building_number", "address_street",
    "address_city", "address_postal_code", "occupation", "credit_file", "driver_license",
    "id_number", "device_number", "ip_address", "yearly_income"
]

def generate_random_customer(customer_id=None):
    customer_id = customer_id or str(uuid4())
    ip_address = fake.ipv4()
    email = fake.email()

    return {
        "customer_id": customer_id,
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "username_nickname": fake.user_name(),
        "account_creation_date": fake.date_time_between(start_date='-5y', end_date='now').isoformat(),
        "birthdate": fake.date_of_birth(minimum_age=18, maximum_age=80).isoformat(),
        "email": email,
        "login_date_and_time": fake.date_time_between(start_date='-30d', end_date='now').isoformat(),
        "address_unit": fake.secondary_address(),
        "address_building_number": fake.building_number(),
        "address_street": fake.street_name(),
        "address_city": fake.city(),
        "address_postal_code": fake.postcode(),
        "occupation": fake.job(),
        "credit_file": random.choice(["yes", "no"]),
        "driver_license": fake.license_plate(),
        "id_number": fake.ssn(),
        "device_number": fake.uuid4(),
        "ip_address": ip_address,
        "yearly_income": round(random.uniform(20000, 200000), 2)
    }

def generate_random_transaction(customer, sanctioned_countries):
    customer_id = customer["customer_id"]
    tx_id = str(uuid4())
    psp_tx_id = str(uuid4())
    pan = fake.credit_card_number()
    tx_type = random.choice(["deposit", "withdrawal"])
    request_date = fake.date_time_between(start_date='-30d', end_date='now')
    onboard_date = fake.date_time_between(start_date='-5y', end_date='now')
    update_date = request_date + timedelta(minutes=random.randint(1, 60))

    method = random.choice(["Visa", "MasterCard", "PayPal", "Crypto"])
    amount = round(random.uniform(10, 100000), 2)
    amount_trx = amount
    customer_fee = round(amount * 0.01, 2)
    email = customer["email"]
    nickname = customer["username_nickname"]
    ip_address = customer["ip_address"]
    agent_fee = round(amount * 0.02, 2)
    tax = round(amount * 0.05, 2)
    sit = fake.word()
    bin_country = fake.country_code()
    country = fake.country_code()
    agent = fake.name()
    marketing_type = random.choice(["email", "affiliate", "organic"])
    status = random.choice(["pending", "completed", "failed"])
    detail = fake.sentence()
    transaction_status = random.choice(["pending"])
    auditor = fake.name()

    # Inject sanctioned country
    if random.random() < 0.05 and sanctioned_countries:
        bin_country = country = random.choice(sanctioned_countries)

    return {
        "customer_id": customer_id,
        "tx_id": tx_id,
        "psp_tx_id": psp_tx_id,
        "pan": pan,
        "type": tx_type,
        "request_date_utc": request_date.isoformat(),
        "update_date_utc": update_date.isoformat(),
        "payment_method": method,
        "amount": amount,
        "amount_trx": amount_trx,
        "customer_fee": customer_fee,
        "email_address": email,
        "nickname": nickname,
        "ip_address": ip_address,
        "agent_fee": agent_fee,
        "tax": tax,
        "sit": sit,
        "bin_country": bin_country,
        "country": country,
        "agent": agent,
        "marketing_type": marketing_type,
        "status": status,
        "detail": detail,
        "transaction_status": transaction_status,
        "auditor": auditor,
        "onboard_date": onboard_date.isoformat()
    }

def generate_customers(n_customers, sanctioned_entities):
    customers = []
    for _ in range(n_customers):
        cust = generate_random_customer()
        
        # Inject sanctioned entity by replacing name, not ID
        if random.random() < 0.05 and sanctioned_entities:
            full_name = random.choice(sanctioned_entities)
            parts = full_name.split()
            if len(parts) >= 2:
                cust["first_name"], cust["last_name"] = parts[0], " ".join(parts[1:])
            else:
                cust["first_name"], cust["last_name"] = full_name, ""
        
        customers.append(cust)
    return pd.DataFrame(customers)

def generate_transactions(n_transactions, customers_df, sanctioned_countries):
    transactions = []
    customers_list = customers_df.to_dict("records")
    for _ in range(n_transactions):
        cust = random.choice(customers_list)
        tx = generate_random_transaction(cust, sanctioned_countries)
        transactions.append(tx)
    return pd.DataFrame(transactions)

def generate_dataset_2step(
    n_customers=500,
    n_transactions=1000,
    sanctioned_entities=None,
    sanctioned_countries=None,
    output_file="full_dataset.csv"
):
    sanctioned_entities = sanctioned_entities or []
    sanctioned_countries = sanctioned_countries or []

    customers_df = generate_customers(n_customers, sanctioned_entities)
    transactions_df = generate_transactions(n_transactions, customers_df, sanctioned_countries)

    full_df = pd.merge(transactions_df, customers_df, on="customer_id", suffixes=("", "_cust"))
    full_df = full_df.loc[:, ~full_df.columns.duplicated()]
    full_df.to_csv(output_file, index=False)
    print(f"✅ Generated {n_customers} customers and {n_transactions} transactions to {output_file}")

if __name__ == "__main__":
    generate_dataset_2step(
        n_customers=300,
        n_transactions=1500,
        sanctioned_entities=["Vladimir Putin", "Oleg Viktorovitj MOROZOV"],
        sanctioned_countries=["IR", "KP", "RU"],
        output_file="full_data.csv"
    )
