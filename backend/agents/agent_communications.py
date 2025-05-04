import logging
from dataclasses import dataclass
from typing import List, Optional
import requests
from openai import OpenAI
from toolhouse import Toolhouse
import pandas as pd
import os




@dataclass
class PatientBillingInfo:
    patient_first_name: str
    patient_last_name: str
    email: str
    phone_number: str
    reason_for_visit: str
    portal_link: str



email_template = """<html>
  <body style="font-family: Arial, sans-serif; color: #333; margin:0; padding:20px;">
    <h2 style="color: #2C3E50; margin-bottom: 10px;">Capital One Fraud Alert</h2>
    <p>Hi Olivia,</p>
    <p>
      We detected a <strong>$25,000</strong> purchase at <strong>Rosevill Electronics</strong> on <strong>May 3, 2025</strong> using your debit card.<br>
      If you recognize this transaction, please confirm below.&nbsp;
      Otherwise, let us know immediately so we can secure your account.
    </p>
    <p style="margin-top: 5px;">
      <a href=""
         style="background-color: #007bff; color: #ffffff; padding: 8px 16px; text-decoration: none;
                border-radius: 4px; display: inline-block; margin-bottom: 10px; width: auto; max-width: 150px;">
        Confirm Transaction
      </a>
      <a href=""
         style="background-color: #d9534f; color: #ffffff; padding: 8px 16px; text-decoration: none;
                border-radius: 4px; display: inline-block; width: auto; max-width: 150px;">
        Report Unauthorized
      </a>
    </p>
    <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
    <p style="font-size: 12px; color: #999;">
      This is an automated message—please do not reply directly to this email.&nbsp;
      If you need assistance, call us at 1‑800‑BANK‑HELP.
    </p>
  </body>
</html>"""


email_template_2 = """<html>
  <body style="font-family: Arial, sans-serif; color: #333; margin:0; padding:20px;">
    <h2 style="color: #2C3E50; margin-bottom: 10px;">Capital One Unusual Activity Alert</h2>
    <p>Hi Olivia,</p>
    <p>
      We’ve noticed <strong>five transactions</strong> totaling <strong>$2,100</strong> in quick succession at merchants in <strong>Country Z</strong> on <strong>May 1–2, 2025</strong>. To ensure your account’s security, please confirm whether these charges are valid:
    </p>
    <ul style="padding-left: 20px; margin-bottom: 20px;">
      <li style="margin-bottom: 8px;">
        Skyline Mart – $500 on May 1
      </li>
      <li style="margin-bottom: 8px;">
        Orbit Electronics – $300 on May 1
      </li>
      <li style="margin-bottom: 8px;">
        Global Eats Café – $400 on May 2
      </li>
      <li style="margin-bottom: 8px;">
        Metro Travel Agency – $450 on May 2
      </li>
      <li style="margin-bottom: 8px;">
        Pinnacle Apparel – $450 on May 2
      </li>
   
    <p style="margin-top: 5px;">
      <a href=""
         style="background-color: #007bff; color: #ffffff; padding: 8px 16px; text-decoration: none;
                border-radius: 4px; display: inline-block; margin-right: 10px; max-width: 150px;">
        Confirm Activity
      </a>
      <a href=""
         style="background-color: #d9534f; color: #ffffff; padding: 8px 16px; text-decoration: none;
                border-radius: 4px; display: inline-block; max-width: 150px;">
        Report Fraud
      </a>
    </p>

     </ul>
    <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
    <p style="font-size: 12px; color: #999;">
      Stay safe, and if you need assistance, call our Fraud Prevention Team at 1‑800‑BANK‑HELP.
    </p>
  </body>
</html>"""

#email_template
template = email_template_2

def send_prompt_to_bland_ai(phone="+19038516387") -> dict:
    """
    Send a prompt to the Bland AI API for voice calling.

    Args:
    prompt (str): The prompt to be used for the voice call.

    Returns:
    dict: The response from the Bland AI API.
    """
    headers = { #
        "Authorization": ""
    }
    prompt = """
        Hello, this is Olivia calling from Capital One’s Fraud Prevention Team. I’m reaching out because we’ve noticed five transactions on your account in quick succession, totaling $3,100:


        Did you authorize these charges?  

        * if the person asks you about the transactions mention them:

            • Skyline Mart – $500  
            • Orbit Electronics – $300   
            • Global Eats Café – $400  
         
        *

        *[Wait for response]*  

        **(AI Agent should respond with: “Awesome,” “Thanks for letting me know,” or “Got it!” before continuing.)**

        If these are valid, we’ll leave everything as is. If not, I can freeze your card right now and help you dispute the charges.  

        *[Wait for response]*  

        **(AI Agent should respond with: “Great,” “Sounds good,” or “Perfect,” before continuing.)**

        make sure you thank them when they say its fraud and freeze their account. 

        Once we confirm, I’ll also send you a text and an email with next steps and a secure link to review or dispute any transactions.  

        *[Wait for response]*  

        **(AI Agent should respond with: “Totally understand,” “That makes sense,” or “Absolutely,” before continuing.)**

        Do you have any questions for me?  

        Thank you for your time, and for helping us keep your account safe. Have a great day!
"""


    data = {
        "phone_number": "+19038516387",
        "from": None,
        "task": prompt,
        "model": "enhanced",
        "language": "en",
        "voice": "June",
        "voice_settings": {},
        "pathway_id": None,
        "local_dialing": False,
        "max_duration": 12,
        "answered_by_enabled": False,
        "wait_for_greeting": False,
        "record": False,
        "amd": False,
        "interruption_threshold": 80,
        "voicemail_message": None,
        "temperature": None,
        "transfer_phone_number": None,
        "transfer_list": {},
        "metadata": None,
        "pronunciation_guide": [],
        "start_time": None,
        "request_data": {},
        "tools": [],
        "dynamic_data": [],
        "analysis_preset": None,
        "analysis_schema": {},
        "webhook": None,
        "calendly": {},
    }

    try:
        response = requests.post(
            "https://us.api.bland.ai/v1/calls", json=data, headers=headers
        )
        response.raise_for_status()
        logging.info("Bland AI API call successful.")
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error while calling Bland AI API: {e}")
        return {}

# send_prompt_to_bland_ai(prompt)


def fetch_csv() -> Optional["pd.DataFrame"]:
    """
    Read the OFACSanctionsHandler.csv file and return its contents as a pandas DataFrame.

    Returns:
    Optional[pd.DataFrame]: A DataFrame containing the OFAC sanctions data or None if an error occurs.
    """
    try:
        # Use the absolute path for reliability
        csv_path = "/Users/sorhan/Compliance Wizzards/llamacon-hackathon/backend/data/sanctions/OFACSanctionsHandler.csv"
        df = pd.read_csv(csv_path)
        return df
    except Exception as e:
        logging.error(f"Error while reading OFACSanctionsHandler.csv: {e}")
        return None

# Call the function to fetch and print patient billing inf
def generate_email_template() -> str:
    email_prompt = """
    You’re the automated Fraud Prevention Email Agent for [Your Bank Name].  
    Given one of the following scenarios, create a concise, professional email template to notify the customer and request confirmation:

    Scenario 1: A single transaction of $15,000 at an unfamiliar merchant (e.g., XYZ Electronics on May 2, 2025).  
    Scenario 2: Multiple rapid transactions totaling $2,100 in a high‑risk country (e.g., five charges from May 1–2, 2025).

    Return a JSON with a single key, "email_body", whose value is the full email (including subject line and body).
    """

    headers = {
        "Content-Type": "application/json",
        "Authorization": ""
    }

    data = {
        "model": "Llama-4-Maverick-17B-128E-Instruct-FP8",
        "messages": [
            {"role": "user", "content": email_prompt}
        ]
    }

    response = requests.post("https://api.llama.com/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        email_response = response.json()
        return email_response.get("email_body", "No email body found.")
    else:
        logging.error(f"Error while generating email template: {response.status_code} - {response.text}")
        return "Error generating email template."
    
def send_fraud_email(
     #email_template_2
   # email_body =  generate_email_template
    email_body: str = template,
    to_email: str = "amir.s.karimloo1@gmail.com",
    cc_email: str = "sorhanft@gmail.com",
    bcc_email: str = "newbeg89@gmail.com",
):
    """
    Send a billing notification email using OpenAI.

    Args:
    email_body (str): """"""The body of the email.
    to_email (str): The recipient's email address.
    cc_email (str): The CC email address. Default is "cc@example.com".
    bcc_email (str): The BCC email address. Default is "bcc@example.com".
    """
    email_request = f"""
    Send an email with the following details:
    - Subject: Billing Notification
    - To: {to_email}
    - Cc: {cc_email}
    - Bcc: {bcc_email}
    - Email body: {email_body}
    """

    # Initialize OpenAI and Toolhouse clients
    client = OpenAI(api_key="")
    th = Toolhouse(
        api_key="", provider="openai"
    )

    # Define the OpenAI model we want to use
    MODEL = "gpt-4o"
    messages = [{"role": "user", "content": email_request}]

    # **Step 2: Pass tools to OpenAI**
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=th.get_tools(),  # Passes the list of available tools
        )
        logging.info("OpenAI response received successfully.")
    except Exception as e:
        logging.error(f"Error while getting OpenAI response: {e}")
        return

    # **Step 3: Execute the tool selected by OpenAI**
    try:
        messages += th.run_tools(response)
        logging.info("Tools executed successfully.")
    except Exception as e:
        logging.error(f"Error while executing tools: {e}")
        return

    # **Print final model response**
    try:
        print(response.choices[0].message.content)
    except Exception as e:
        logging.error(f"Error while printing response: {e}")


############### CALL ###################





#email is done
#send_billing_email()
#phone is done 
#send_prompt_to_bland_ai()
#csv = fetch_csv()
