#notification_service.py

from .sms_service import send_sms
from .models import Users, Account, Transactions
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def notify_user_of_transaction(user, amount, transaction_type, updated_balance=None, reference_number=None):
    full_name = f"{user.first_name} {user.last_name}"
    # Construct the SMS message based on the transaction type
    if transaction_type == 'deposit':
        sms_message = (
            f"Dear {full_name}, your account {user.account_number} has been credited with {amount}. "
            f"New balance is {updated_balance}. Reference number: {reference_number}"
        )
    elif transaction_type == 'withdrawal':
        sms_message = (
            f"Dear {full_name}, your account {user.account_number} has been debited with {amount}. "
            f"New balance is {updated_balance}. Reference number: {reference_number}"
        )
    elif transaction_type == 'emi_payment':
        sms_message = (
            f"Dear {full_name}, EMI Payment of {amount} completed for account {user.account_number}. "
            f"New balance is {updated_balance}. Reference number: {reference_number}"
        )
    else:
        sms_message = (
            f"Dear {full_name}, Notification: {transaction_type} of {amount} for account {user.account_number}. "
            f"Reference number: {reference_number}"
        )
    
    # Add default country code if not present
    mobile_number = user.mobile_number
    if not mobile_number.startswith('+'):
        mobile_number = f"+91{user.mobile_number}"  # Add default country code; replace +91 with your preferred code

    # Send the SMS message
    send_sms(mobile_number, sms_message)

def notify_user_of_account_opening(user, account_number):
    logger.debug("notify_user_of_account_opening function called.")
    sns_message = f"Congratulations! Your account with number {account_number} has been successfully opened. Welcome aboard!"
    response = publish_to_sns_topic(SNS_TOPIC_ARN, sns_message)
    if response:
        logger.info(f"Notification sent to SNS Topic: {response}")
    else:
        logger.error("Failed to send notification to SNS Topic.")

    # Add default country code if not present
    mobile_number = user.mobile_number
    if not mobile_number.startswith('+'):
        mobile_number = f"+91{user.mobile_number}"  # Add default country code; replace +91 with your preferred code


    send_sms(mobile_number, sms_message)