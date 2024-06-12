from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from authentication.views import login_page

# Create your views here.
@login_required(login_url='/auth/login/')
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required(login_url='/auth/login/')
def home(request):
    return redirect('dashboard')