from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='cards'),
    path('load-cards/', views.lazy_load_cards, name='lazy_load_cards'),
]