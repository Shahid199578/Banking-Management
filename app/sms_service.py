#sms_service.py

# # for gupshup
# import requests

# def send_sms(mobile_number, message):
#     # Gupshup API configuration
#     api_url = "https://enterprise.smsgupshup.com/GatewayAPI/rest"
#     user_id = "your_gupshup_userid"  # Replace with your Gupshup user ID
#     password = "your_gupshup_password"  # Replace with your Gupshup password
    
#     # Prepare the payload
#     payload = {
#         'userid': user_id,
#         'password': password,
#         'send_to': mobile_number,
#         'method': 'SendMessage',
#         'msg': message,
#         'msg_type': 'TEXT',
#         'auth_scheme': 'plain',
#         'v': '1.1',
#         'format': 'text',
#         'linkTrakingEnabled': 'TRUE' # Optional parameter to enable link tracking
#     }
    
#     # Send the GET request to Gupshup API
#     response = requests.get(api_url, params=payload)
    
#     # Handle the response
#     if response.status_code == 200:
#         print(f"SMS sent successfully to {mobile_number}")
#     else:
#         print(f"Failed to send SMS. Status code: {response.status_code}, Response: {response.text}")

#     return response



import boto3
import logging
from botocore.exceptions import ClientError

# Set up logging
logging.basicConfig(level=logging.INFO)

# Create an SNS client with the region configured in the environment or default to 'us-east-1'
region = 'us-east-1'  # Default region, you can override this with an environment variable
sns_client = boto3.client('sns', region_name=region)

def send_sms(mobile_number, message):
    # Add country code by default (e.g., +91 for India)
    if not mobile_number.startswith('+'):
        mobile_number = '+91' + mobile_number  # Example country code
    
    try:
        response = sns_client.publish(
            PhoneNumber=mobile_number,
            Message=message
        )
        logging.info(f"SMS sent to {mobile_number}: {response}")
        return response
    except ClientError as e:
        logging.error(f"Failed to send SMS to {mobile_number}: {e}")
        return None


# import requests

# def send_sms(mobile_number, message):
#     # Exotel API configuration
#     exotel_sid = "cloud32"  # Your Exotel SID
#     exotel_api_key = "5b0d89dc51ff7fa3f2dc718afb800dae6473502ad146db50"  # Your Exotel API key (username)
#     exotel_api_token = "643532a6996ba0b8783681cecdf2791c5118c956c99a52ef"  # Your Exotel API token (password); fetch from dashboard
#     subdomain = "api.exotel.com"

#     api_url = f"https://{exotel_api_key}:{exotel_api_token}@{subdomain}/v1/Accounts/{exotel_sid}/Sms/send"
    
#     payload = {
#         'From': 'your_sender_id',  # Optional: Exotel approved sender ID
#         'To': mobile_number,
#         'Body': message
#     }
    
#     # Use basic authentication with API key and token
#     response = requests.post(api_url, data=payload,)

#     # Handle the response
#     if response.status_code == 200:
#         print(f"SMS sent successfully to {mobile_number}")
#     else:
#         print(f"Failed to send SMS. Status code: {response.status_code}, Response: {response.text}")

#     return response
