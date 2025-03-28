from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import login  # Add this import for logging in the user after signup
from django.contrib.auth.forms import UserCreationForm  # Add this import for the signup form
from .models import Customer, ServiceRequest
from .forms import ServiceRequestForm
from django.utils import timezone

# Add this new view for the homepage
def home(request):
    if request.user.is_authenticated:
        return redirect('request_list')  # Redirect authenticated users to their requests
    return redirect('login')  # Redirect unauthenticated users to the login page

# Add the signup view
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a Customer instance for the new user
            Customer.objects.create(user=user)
            # Log the user in after signup
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('request_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

# Existing views...
@login_required
def submit_request(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            service_request = form.save(commit=False)
            customer, created = Customer.objects.get_or_create(user=request.user)
            service_request.customer = customer
            service_request.save()
            messages.success(request, 'Service request submitted successfully!')
            return redirect('request_list')
    else:
        form = ServiceRequestForm()
    return render(request, 'services/request_form.html', {'form': form})

@login_required
def request_list(request):
    customer, created = Customer.objects.get_or_create(user=request.user)
    requests = customer.service_requests.all()
    return render(request, 'services/request_list.html', {'requests': requests})

@login_required
def request_detail(request, request_id):
    customer = Customer.objects.get(user=request.user)
    service_request = get_object_or_404(ServiceRequest, id=request_id, customer=customer)
    return render(request, 'services/request_detail.html', {'request': service_request})

@login_required
def account_info(request):
    customer, created = Customer.objects.get_or_create(user=request.user)
    return render(request, 'services/account_info.html', {'customer': customer})

@login_required
def support_dashboard(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('request_list')
    requests = ServiceRequest.objects.all()
    return render(request, 'services/support_dashboard.html', {'requests': requests})

@login_required
def update_request_status(request, request_id):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect('request_list')
    service_request = get_object_or_404(ServiceRequest, id=request_id)
    if request.method == 'POST':
        status = request.POST.get('status')
        service_request.status = status
        if status == 'RESOLVED':
            service_request.resolved_at = timezone.now()
        service_request.assigned_to = request.user
        service_request.save()
        messages.success(request, 'Request status updated successfully!')
        return redirect('support_dashboard')
    return render(request, 'services/update_status.html', {'request': service_request})