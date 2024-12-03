from django import template
from datetime import datetime, timedelta
from django.utils import timezone

register = template.Library()

@register.filter
def multiply(value, arg):
    return value * arg

def minutes(value):
    if value is None:
        return 0
    return int(value.total_seconds() / 60)

def is_expired(exp_date):
    current_date = timezone.now().date()
    return exp_date < current_date

import hashlib

def custom_hash_function(password):
    # Hash the password using a secure hashing algorithm such as SHA-256
    # You can use a different algorithm based on your requirements

    # Convert the password to bytes
    password_bytes = password.encode('utf-8')

    # Create a hash object
    hash_object = hashlib.sha256()

    # Update the hash object with the password bytes
    hash_object.update(password_bytes)

    # Get the hashed password as a hexadecimal string
    hashed_password = hash_object.hexdigest()

    # Return the hashed password
    return hashed_password