from django.shortcuts import redirect
from django.contrib import messages

def admin_login_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('admin_logged_in'):
            messages.warning(request, "Please log in to access this page.")
            return redirect('admin_login')
        return view_func(request, *args, **kwargs)
    return wrapper