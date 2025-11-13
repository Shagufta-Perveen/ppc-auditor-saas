from django.db import models
from django.conf import settings
# allauth ka SocialAccount model import karein taaki hum token fetch kar saken
from allauth.socialaccount.models import SocialAccount

class CustomerAccount(models.Model):
    """
    Represents a single Google Ads Customer ID linked to a user.
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # The Google Ads Customer ID (e.g., 1234567890)
    customer_id = models.CharField(max_length=15, unique=True)
    
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.customer_id}"

    def get_social_token(self):
        """Fetches the associated SocialToken needed for API calls."""
        try:
            # Google Adwords scope sirf 'google' provider se milta hai
            social_account = SocialAccount.objects.get(user=self.user, provider='google')
            # socialtoken_set.first() mein hamara access aur refresh token stored hai
            return social_account.socialtoken_set.first()
        except SocialAccount.DoesNotExist:
            return None


class AuditResult(models.Model):
    """
    Stores the results of an audit (e.g., wasted keywords, high CPC).
    """
    account = models.ForeignKey(CustomerAccount, on_delete=models.CASCADE)
    date = models.DateField() # Jis din ka data audit hua
    keyword_text = models.CharField(max_length=255)
    cost_usd = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    reason = models.CharField(max_length=255) # e.g., 'Zero Conversions' or 'High Cost'
    is_resolved = models.BooleanField(default=False) # User ne is issue ko theek kiya ya nahi

    class Meta:
        # User ko ek hi din mein ek hi keyword ka duplicate result na dikhe
        unique_together = ('account', 'date', 'keyword_text')

    def __str__(self):
        return f"Audit for {self.account.customer_id} on {self.date}: {self.keyword_text}"


