# dashboard/views.py

from django.shortcuts import render, redirect

def home_view(request):
    """
    Redirects logged-in users to the dashboard.
    Otherwise, directs them to the Allauth login/signup page.
    """
    if request.user.is_authenticated:
        # If logged in, go straight to the dashboard (which we'll create next)
        return redirect('dashboard_home') 
    
    # If not logged in, show a simple landing page or redirect to login
    # For now, let's redirect to the Allauth login page
    return redirect('account_login') 

def dashboard_home(request):
    """Placeholder for the main dashboard content."""
    # We will expand this view soon to display PPC data
    return render(request, 'dashboard/home.html')