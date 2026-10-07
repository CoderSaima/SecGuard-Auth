from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import SecAuth_Model 

# -------
# Home
# -------
def home_view(request):
    return render(request, 'home.html')

# ----------
# regiter
# ----------
def SecAuth_views(request):
    """Handles secure new account creation updates within register.html."""
    context = {'error_message': None, 'success_message': None}

    if request.method == "POST":
        user_name = request.POST.get('user_Name')
        user_email = request.POST.get('user_Email')
        user_password = request.POST.get('user_Password')

        if not user_name or not user_email or not user_password:
            context['error_message'] = "All registration fields are required."
            return render(request, 'register.html', context)

        if len(user_password) < 8 :
            context['error_message'] = "Password must be at least 8 characters long for system security."
            return render(request, 'register.html', context)

        if SecAuth_Model.objects.filter(name=user_name).exists():
            context['error_message'] = 'The username already exists.'
            return render(request, 'register.html', context)

        try:
            encrypted_pwd = make_password(user_password)

            SecAuth_Model.objects.create(
                name=user_name,
                email=user_email,
                password=encrypted_pwd
            )
            context['success_message'] = "Account created successfully!"
        
        except Exception:
            context['error_message'] = "An account with this email address already exists!"
            
    return render(request, 'register.html', context)
    # return redirect('login_url')
# -----------
# LOGIN
# -----------
def SecAuth_login_view(request):
    """Handles verification parameters inside login.html using accurate field keys."""
    context = {'error_message': None}

    if request.method == 'POST':
        # FIXED: Swapped keys to match HTML names: 'login_Email' and 'login_Password'
        email_input = request.POST.get('login_Email', '').strip()
        password_input = request.POST.get('login_Password', '')

        try:
            user_record = SecAuth_Model.objects.get(email=email_input)

            if check_password(password_input, user_record.password):
                request.session['auth_user_id'] = user_record.id
                request.session['auth_user_name'] = user_record.name

                return HttpResponse(f"Welcome back, {user_record.name}!")
            else:
                context['error_message'] = "Invalid Authentication Details."
        except SecAuth_Model.DoesNotExist:
            context['error_message'] = 'The account does not exist. Invalid Inputs.'
        
    return render(request, 'login.html', context)

#----------------------
# dashboard
# --------------------

def SecAuth_dashboard_view(request):
    """
    CRITICAL RESTRICTIVE PERMISSION SHIELD:
    Checks if the user carries an active authentication session badge.
    If missing, it intercepts execution and triggers a security drop bounce.
    """

    if 'auth_user_id' not in request.session:
        return redirect('login_url')

    context = {
        'username' : request.session.get('auth_user_name')
    }
    return render(request, 'dashboard.html', context)


# -------
# LOGOUT
# -------
def SecAuth_logout_view(request):
    """Destroys active session metadata tracking arrays cleanly."""

    request.session.flush()
    return redirect('login_url')