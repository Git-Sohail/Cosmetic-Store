import hashlib
import requests
from django.conf import settings
from django.urls import reverse

def generate_esewa_payment_url(payment):
    """Generate eSewa payment URL"""
    success_url = settings.SITE_URL + reverse('payment:esewa_callback')
    failure_url = settings.SITE_URL + reverse('payment:esewa_callback')
    
    # eSewa payment parameters
    params = {
        'amt': str(payment.amount),
        'pdc': '0',  # Delivery charge
        'psc': '0',  # Service charge
        'txAmt': '0',  # Tax amount
        'tAmt': str(payment.amount),  # Total amount
        'pid': payment.payment_id,
        'scd': settings.ESEWA_MERCHANT_CODE,
        'su': success_url,
        'fu': failure_url,
    }
    
    # Generate signature
    signature_string = f"pid={params['pid']}&amt={params['amt']}&tAmt={params['tAmt']}&txAmt={params['txAmt']}&psc={params['psc']}&pdc={params['pdc']}&scd={params['scd']}&su={params['su']}&fu={params['fu']}"
    signature = hashlib.md5(signature_string.encode()).hexdigest()
    params['signature'] = signature
    
    # Generate payment URL
    payment_url = f"{settings.ESEWA_PAYMENT_URL}?{'&'.join(f'{k}={v}' for k, v in params.items())}"
    return payment_url

def verify_esewa_payment(data):
    """Verify eSewa payment response"""
    try:
        # Extract required fields
        pid = data.get('pid')
        ref = data.get('ref')
        tAmt = data.get('tAmt')
        amt = data.get('amt')
        signature = data.get('signature')
        
        # Generate signature for verification
        signature_string = f"pid={pid}&ref={ref}&tAmt={tAmt}&amt={amt}&scd={settings.ESEWA_MERCHANT_CODE}"
        calculated_signature = hashlib.md5(signature_string.encode()).hexdigest()
        
        # Verify signature and amount
        return (signature == calculated_signature and 
                float(tAmt) == float(amt))
    except Exception:
        return False

def verify_khalti_payment(data):
    """Verify Khalti payment response"""
    try:
        # Extract required fields
        token = data.get('token')
        amount = data.get('amount')
        idx = data.get('idx')
        
        # Verify payment with Khalti API
        headers = {
            'Authorization': f'Key {settings.KHALTI_SECRET_KEY}',
            'Content-Type': 'application/json'
        }
        
        response = requests.post(
            settings.KHALTI_VERIFY_URL,
            headers=headers,
            json={'token': token}
        )
        
        if response.status_code == 200:
            response_data = response.json()
            return (response_data.get('idx') == idx and 
                   response_data.get('amount') == amount)
        return False
    except Exception:
        return False 