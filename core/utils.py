from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import EmailMessage
import random

def admin_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('admin_logged_in'):
            messages.warning(request, "Please log in to access this page.")
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(email, otp):
    subject = "Your OTP Code"
    message = f"Hello,\n\nYour OTP for password reset is: {otp}\n\nRegards,\nSpeedy Bites"
    email_obj = EmailMessage(subject, message, to=[email])
    email_obj.send()