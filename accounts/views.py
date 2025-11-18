from django.shortcuts import render
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from .forms import CustomUserCreationForm, CustomErrorList, ProfilePictureForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from cart.models import Order
from .models import UserProfile

@login_required
def logout(request):
    auth_logout(request)
    return redirect('home.index')
def login(request):
    template_data = {}
    template_data['title'] = 'Login'
    if request.method == 'GET':
        return render(request, 'accounts/login.html', {'template_data': template_data})
    elif request.method == 'POST':
        user = authenticate(
            request,
            username = request.POST['username'],
            password = request.POST['password']
        )
        if user is None:
            template_data['error'] = 'The username or password is incorrect.'
            return render(request, 'accounts/login.html', {'template_data': template_data})
        else:
            auth_login(request, user)
            return redirect('home.index')
def signup(request):
    template_data = {}
    template_data['title'] = 'Sign Up'
    if request.method == 'GET':
        template_data['form'] = CustomUserCreationForm()
        return render(request, 'accounts/signup.html',
            {'template_data': template_data})
    elif request.method == 'POST':
        form = CustomUserCreationForm(request.POST, error_class=CustomErrorList)
        if form.is_valid():
            form.save()
            return redirect('accounts.login')
        else:
            template_data['form'] = form
            return render(request, 'accounts/signup.html', {'template_data': template_data})
        
@login_required
def orders(request):
    template_data = {}
    template_data['title'] = 'Orders'
    template_data['orders'] = request.user.order_set.all()
    return render(request, 'accounts/orders.html', {'template_data': template_data})

@login_required
def subscription(request):
    template_data = {}
    template_data['title'] = 'Subscription'
    # Sum all orders' totals for the current user
    total_spend = sum(order.total for order in Order.objects.filter(user=request.user))
    # Determine subscription level
    if total_spend <= 15:
        level = 'Basic'
    elif total_spend <= 30:
        level = 'Medium'
    else:
        level = 'Premium'
    template_data['total_spend'] = total_spend
    template_data['level'] = level
    return render(request, 'accounts/subscription.html', {'template_data': template_data})

@login_required
def profile(request):
    template_data = {}
    template_data['title'] = 'User Profile'
    
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            template_data['success_message'] = 'Profile picture updated successfully!'
            template_data['form'] = ProfilePictureForm(instance=profile)
        else:
            template_data['form'] = form
    else:
        template_data['form'] = ProfilePictureForm(instance=profile)
    
    template_data['profile'] = profile
    return render(request, 'accounts/profile.html', {'template_data': template_data})