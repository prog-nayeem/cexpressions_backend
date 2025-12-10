import random
from datetime import datetime, timedelta
from django.utils import timezone
from .models import User 

def generate_and_store_otp(user: User):
    otp = str(random.randint(100000, 999999))
    expiry_time = timezone.now() + timedelta(minutes=5)

    user.otp_code = otp
    user.otp_created_at = expiry_time
    user.save()
    return otp