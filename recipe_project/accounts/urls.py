from django.urls import path
from .views import Registration, login_view, logout_view, profile_view

#Import of django's built-in login and logout views.

urlpatterns = [
    path('register/', view=Registration.as_view(), name='register'),
    path('login/', view=login_view, name='login'),
    path('logout/', view=logout_view, name='logout'),
    path('profile/', view=profile_view, name='profile')
]