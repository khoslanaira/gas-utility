from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Add this for the root URL
    path('signup/', views.signup, name='signup'),  # Ensure this line exists
    path('submit/', views.submit_request, name='submit_request'),
    path('requests/', views.request_list, name='request_list'),
    path('requests/<int:request_id>/', views.request_detail, name='request_detail'),
    path('accounts/', views.account_info, name='account_info'),
    path('support/', views.support_dashboard, name='support_dashboard'),
    path('support/update/<int:request_id>/', views.update_request_status, name='update_request_status'),
]