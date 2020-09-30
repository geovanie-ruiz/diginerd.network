from django.urls import include, path

from . import views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('register/', views.RegisterView.as_view(), name='register'),
]
