# vpn_app/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# from django.contrib.auth import authenticate, login, logout

from .models import UserSite, UserSiteVisit
from django.contrib import messages
from users.forms import UserProfileForm
from django.contrib.auth.models import auth

from .models import *
from django.contrib.auth.models import User


@login_required
def home(request):
    user_sites = UserSite.objects.filter(user=request.user)
    user_id = request.user.id
    return render(request, 'home.html', {'user_sites': user_sites, 'user_id': user_id})

@login_required
def create_site(request):
    if request.method == 'POST':
        name = request.POST['name']
        url = request.POST['url']
        user_site = UserSite.objects.create(user=request.user, name=name, url=url)
        return redirect('home')
    return render(request, 'create_site.html')

@login_required
def visit_site(request, user_site_name):
    try:
        user_site = UserSite.objects.get(user=request.user, name=user_site_name)
        UserSiteVisit.objects.create(user_site=user_site)
        return redirect(user_site.url)
    except:
        return redirect('home')



from django.shortcuts import get_object_or_404
@login_required
def edit_profile(request, user_id):

    print(request.user)
    try:
        user_profile = get_object_or_404(User, id=user_id)
        if request.method == 'POST':
            form = UserProfileForm(request.POST, instance=user_profile)
            if form.is_valid():
                form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('home')
        else:
            form = UserProfileForm(instance=user_profile)

        return render(request, 'edit_profile.html', {'form': form})
    except:  # Обробка винятку, якщо UserProfile не існує
        messages.error(request, 'Profile does not exist. Please create a profile first.')
        return redirect('home')

@login_required
def view_statistics(request, user_id):
    try:
        user = get_object_or_404(User, id=user_id)
        user_sites = UserSite.objects.filter(user=user)
        site_statistics = {}
        total_data_sent = 0
        total_data_received = 0

        for user_site in user_sites:
            print(user_site)
            visits = UserSiteVisit.objects.filter(user_site=user_site)
            print(visits)
            data_sent = visits.aggregate(models.Sum('data_sent'))['data_sent__sum'] or 0
            print(data_sent)
            data_received = visits.aggregate(models.Sum('data_received'))['data_received__sum'] or 0

            site_statistics[user_site.name] = {
                'visits': visits.count(),
                'data_sent': data_sent,
                'data_received': data_received,
            }

            total_data_sent += data_sent
            total_data_received += data_received

        return render(request, 'view_statistics.html', {
            'site_statistics': site_statistics,
            'total_data_sent': total_data_sent,
            'total_data_received': total_data_received,
        })
    except:
        return redirect('home')

@login_required
def view_user_details(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
        user_attributes = [(field.name, getattr(user, field.name)) for field in user._meta.fields]

        return render(request, 'view_user_details.html', {'user_attributes': user_attributes, 'user_id': user_id})
    except User.DoesNotExist:
        # Обробка випадку, коли користувача не існує
        return render(request, 'register')
    
    