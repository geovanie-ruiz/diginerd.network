from django.urls import path

from . import views

urlpatterns = [
    # General Landing Page
    path('', views.CardsIndexView.as_view(), name='cards'),

    # Filtered Card Lists
    path('sets/', views.SetListView.as_view(), name='sets'),
    path('list/<str:term>/', views.FilteredListView.as_view(), name='filtered_list'),
    #path('decks/', views.DecksListView.as_view(), name='decks'),

    # Card View
    path('card-details/<str:number>', views.CardDetailView.as_view(), name='card_view'),
]
