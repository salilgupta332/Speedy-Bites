from django.shortcuts import render
from django.http import HttpResponse
from .models import MenuItem
from .forms import MenuItemForm
from django.shortcuts import render, redirect
import base64
from django.contrib import messages
from core.utils import admin_login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from .forms import AdminRegistrationForm
from .models import Admin_User
from .models import SiteUser
from .forms import UserRegisterForm, UserLoginForm
from core.models import SiteUser
from django.urls import reverse
from django.core.mail import send_mail 
from django.conf import settings
import uuid
from core.utils import generate_otp, send_otp_email
import random
from django.contrib.auth.hashers import make_password
import bcrypt

@admin_login_required
def menu_dashboard(request):
    items = MenuItem.objects()
    return render(request, 'admin/menu_dashboard.html', {'menu_items': items})

@admin_login_required
def menu_dashboard(request):
    items = MenuItem.objects()
    return render(request, 'admin/menu_dashboard.html', {'menu_items': items})

def add_menu_item(request):
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            image_file = request.FILES.get('image')
            image_data = None

            if image_file:
                image_data = base64.b64encode(image_file.read()).decode('utf-8')

            MenuItem(
                name=form.cleaned_data['name'],
                description=form.cleaned_data['description'],
                price=form.cleaned_data['price'],  # ✅ comma fixed here
                image_data=image_data
            ).save()
            return redirect('menu_dashboard')
    else:
        form = MenuItemForm()
    return render(request, 'admin/add_item.html', {'form': form})


def delete_menu_item(request, item_id):
    item = MenuItem.objects.get(id=item_id)
    item.delete()
    return redirect('menu_dashboard')


def edit_menu_item(request, item_id):
    item = MenuItem.objects.get(id=item_id)

    if request.method == 'POST':
        form = MenuItemForm(request.POST)
        if form.is_valid():
            item.name = form.cleaned_data['name']
            item.price = form.cleaned_data['price']
            item.description = form.cleaned_data['description']
            item.save()
            return redirect('menu_dashboard')
    else:
        # Pre-fill the form manually
        form = MenuItemForm(initial={
            'name': item.name,
            'price': item.price,
            'description': item.description,
        })

    return render(request, 'admin/edit_item.html', {'form': form})

def delete_menu_item(request, item_id):
    try:
        item = MenuItem.objects.get(id=item_id)
        item.delete()
        return redirect('menu_dashboard')
    except MenuItem.DoesNotExist:
        return HttpResponse("Item not found", status=404)

def landing_page(request):
   def landing_page(request):
    try:
        print("[DEBUG] session:", request.session.items())
        return render(request, 'landing.html')
    except Exception as e:
        print("[ERROR] Landing page crash:", e)
        return HttpResponse("Internal Server Error in landing page", status=500)

def admin_dashboard(request):
    return render(request, 'admin/admin_dashboard.html')

def admin_register(request):
    if request.method == 'POST':
        form = AdminRegistrationForm(request.POST)
        if form.is_valid():
            Admin_User(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=make_password(form.cleaned_data['password'])  # 🔐 hashed
            ).save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('admin_login')  # or redirect to 'login'
    else:
        form = AdminRegistrationForm()

    return render(request, 'admin/admin_register.html', {'form': form})



from django.contrib.auth.hashers import check_password

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = Admin_User.objects.get(username=username)
            if check_password(password, user.password):
                # ✅ Login success - store session
                request.session['admin_logged_in'] = True
                messages.success(request, "Login successful!")
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Invalid password")
        except Admin_User.DoesNotExist:
            messages.error(request, "User not found")
    
    return render(request, 'admin/admin_login.html')

def admin_logout(request):
    print("Before logout:", request.session.items()) 
    request.session.flush()  # Clears all session data
    print("After logout:", request.session.items())
    return redirect('admin_login')  

# --- Step 3: User Auth Views START ---

def user_register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            SiteUser(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                # mobile=form.cleaned_data['mobile']
            ).save()
            messages.success(request, 'Registration successful! Please login.')
            return redirect('user_login')
    else:
        form = UserRegisterForm()
    return render(request, 'user/user_register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            user = SiteUser.objects(username=form.cleaned_data['username'], password=form.cleaned_data['password']).first()
            if user:
                request.session['user_logged_in'] = True
                request.session['username'] = user.username
                return redirect('landing')  # or wherever
            else:
                messages.error(request, 'Invalid credentials')
    else:
        form = UserLoginForm()
    return render(request, 'user/user_login.html', {'form': form})
# --- Step 3: User Auth Views END ---

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            entered_password = form.cleaned_data['password']

            user = SiteUser.objects(username=username).first()
            if user:
                try:
                    if bcrypt.checkpw(entered_password.encode('utf-8'), user.password.encode('utf-8')):
                        request.session['user_logged_in'] = True
                        request.session['username'] = user.username
                        request.session['user_id'] = str(user.id) 
                        request.session['user_name'] = user.username
                        return redirect('landing')
                except ValueError:
                    # Fallback: assume password was stored as plain text (not secure!)
                    if user.password == entered_password:
                        # Auto-upgrade to hashed version
                        hashed = bcrypt.hashpw(entered_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                        user.password = hashed
                        user.save()
                        request.session['user_logged_in'] = True
                        request.session['username'] = user.username
                        request.session['user_id'] = str(user.id) 
                        request.session['user_name'] = user.username
                        return redirect('landing')

            messages.error(request, 'Invalid credentials')
    else:
        form = UserLoginForm()
    return render(request, 'user/user_login.html', {'form': form})


# --- Step 3: User Auth Views END ---

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = SiteUser.objects.get(email=email)

            # ✅ Generate token
            token = str(uuid.uuid4())
            user.token = token
            user.save()

            # ✅ Create reset link
            reset_link = request.build_absolute_uri(
                reverse('reset_password', args=[token])
            )

            # ✅ Send reset link (you can replace this with your own email system)
            send_mail(
                subject='Reset Your Password',
                message=f'Click here to reset your password: {reset_link}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )

            return render(request, 'user/forgot_password.html', {'message': 'Password reset link sent to your email.'})
        
        except SiteUser.DoesNotExist:
            return render(request, 'user/forgot_password.html', {'message': 'Email not found'})
    
    return render(request, 'user/send_otp.html')



def send_otp_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = SiteUser.objects.get(email=email)
            otp = str(random.randint(100000, 999999))  # Generate 6-digit OTP
            user.otp = otp
            user.save()

            # Simulate email sending
            send_mail(
                subject='Your OTP for Password Reset',
                message=f'Your OTP is: {otp}',
                from_email='noreply@speedybites.com',
                recipient_list=[email],
                fail_silently=False,
            )

            # Store OTP and email in session
            request.session['otp'] = otp
            request.session['reset_email'] = email
            request.session.set_expiry(300)  # OTP valid for 5 minutes

            print(f"Generated OTP for {email}: {otp}")
            return redirect('verify_otp_email')  # this must match your URL name
        except SiteUser.DoesNotExist:
            messages.error(request, "Email address not registered.")
    
    return render(request, 'user/send_otp.html')


def verify_otp_view(request):
    if not request.session.get('otp') or not request.session.get('reset_email'):
        messages.error(request, "Session expired. Please request a new OTP.")
        return redirect('send_otp')

    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        stored_otp = request.session.get('otp')

        if entered_otp == stored_otp:
            request.session['otp_verified'] = True
            return redirect('reset_password')
        else:
            messages.error(request, "Invalid OTP")
            return redirect('verify_otp_email')

    return render(request, 'user/verify_otp_email.html')

def reset_password_view(request):
    email = request.session.get('reset_email')

    if not request.session.get('otp_verified'):  # ✅ Prevent access without verification
        messages.error(request, "Access denied. Please verify OTP first.")
        return redirect('send_otp_email')

    if request.method == 'POST':
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if new_password == confirm_password:
            try:
                user = SiteUser.objects.get(email=email)

                # ✅ Hash with bcrypt, compatible with your login logic
                hashed = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                user.password = hashed
                user.save()

                messages.success(request, "Password reset successfully.")
                request.session.pop('otp_verified', None)
                return redirect('user_login')
            except SiteUser.DoesNotExist:
                messages.error(request, "User not found.")
                return redirect('forgot_password')
        else:
            messages.error(request, "Passwords do not match.")

    return render(request, 'user/reset_password.html')


def send_otp_email_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        print(f"[DEBUG] Submitted email: {email}")

        # Debug: Show all registered SiteUser emails
        print("[DEBUG] SiteUser emails in DB:")
        for user in SiteUser.objects.all():
            print(user.email)

        try:
            user = SiteUser.objects.get(email__iexact=email)
        except SiteUser.DoesNotExist:
            messages.error(request, "Email not registered.")
            return redirect('send_otp')

        otp = generate_otp()
        request.session['email_otp'] = otp
        request.session['reset_email'] = email

        send_otp_email(email, otp)
        messages.success(request, "OTP sent to your email.")
        return redirect('verify_otp_email')

    return render(request, 'user/send_otp.html')
