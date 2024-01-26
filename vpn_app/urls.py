# vpn_app/urls.py
from django.urls import path
from .views import home, create_site, view_user_details, visit_site, edit_profile, view_statistics

urlpatterns = [
    
    path('home/', home, name='home'),
    path('create_site/', create_site, name='create_site'),
    path('<str:user_site_name>/', visit_site, name='visit_site'),
    path('view_statistics/<int:user_id>/', view_statistics, name='view_statistics'),
    path('edit_profile/<int:user_id>/', edit_profile, name='edit_profile'),
    path('user/<int:user_id>/', view_user_details, name='view_user_details'),

    
]


