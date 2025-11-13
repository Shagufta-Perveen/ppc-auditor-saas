# dashboard/tasks.py

from celery import shared_task
from django.utils import timezone
from .models import CustomerAccount, AuditResult
from google.ads.googleads.client import GoogleAdsClient
from google.ads.googleads.errors import GoogleAdsException
import logging

logger = logging.getLogger(__name__)

# NOTE: Is function ko abhi hum frontend se call karenge jab user apna ID daalega
# Aage hum isko Celery Beat mein schedule karenge.

@shared_task(bind=True)
def run_full_account_audit(self, customer_account_id):
    """
    Celery task to fetch PPC data and run the waste detection logic.
    """
    try:
        account = CustomerAccount.objects.get(id=customer_account_id)
    except CustomerAccount.DoesNotExist:
        logger.error(f"CustomerAccount ID {customer_account_id} not found.")
        return

    # 1. Fetch the CRITICAL Refresh Token and Credentials
    token = account.get_social_token()
    if not token or not token.token_secret:
        logger.error(f"No refresh token found for user: {account.user.email}. User needs to re-authenticate.")
        return

    # 2. Configure the Google Ads Client
    try:
        client = GoogleAdsClient.load_from_dict({
            # You must REPLACE THIS with your actual Google Ads Developer Token
            'developer_token': 'YOUR_DEVELOPER_TOKEN_HERE', 
            'client_id': token.app.client_id,
            'client_secret': token.app.secret,
            'refresh_token': token.token_secret, # CRITICAL: The saved token
            'use_proto_plus': True
        })
    except Exception as e:
        logger.error(f"Failed to initialize GoogleAdsClient: {e}")
        return

    # 3. Call the Data Pull Function (Mocked for now)
    try:
        # Is function ko baad mein real API call se replace kiya jaega
        audit_data = fetch_mock_wasted_keyword_data(client, account.customer_id) 
        
        # 4. Process and Save Audit Results
        today = timezone.now().date()
        for row in audit_data:
            # Using update_or_create to avoid duplicates if the task runs multiple times a day
            AuditResult.objects.update_or_create(
                account=account,
                date=today,
                keyword_text=row['keyword_text'],
                defaults={
                    'cost_usd': row['cost'],
                    'reason': row['reason'],
                    'is_resolved': False
                }
            )
        logger.info(f"Successfully processed {len(audit_data)} audit results for {account.customer_id}")
    
    except GoogleAdsException as ex:
        logger.error(f"Google Ads API Error for {account.customer_id}: {ex.error.message}")
    except Exception as e:
        logger.error(f"General processing error: {e}")


def fetch_mock_wasted_keyword_data(client, customer_id):
    """
    MOCK function: Simulates querying Google Ads API for keywords 
    with high cost and zero conversions (wasted spend).
    """
    # --- MOCK DATA RETURN FOR TESTING ---
    # In a real app, you would use client.get_service('GoogleAdsService') here.
    return [
        {'keyword_text': 'zero conversion keyword A', 'cost': 15.20, 'reason': 'Zero conversions, high clicks.'},
        {'keyword_text': 'broad match failure B', 'cost': 22.80, 'reason': 'High cost, irrelevant searches.'},
    ]
    # ------------------------------------