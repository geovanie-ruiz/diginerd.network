from django.urls import path

from . import views

urlpatterns = [
    # POST paths
    path('filter/', views.card_filter, name='card_filter'),
    path('search/', views.card_search, name='card_search'),
    path('random/', views.get_random_card, name='random'),

    # Filtered Card Lists
    path('sets/', views.SetListView.as_view(), name='sets'),
    path('set/<str:code>/', views.FilteredSetView.as_view(), name='filtered_set'),
    path('list/<str:term>/', views.FilteredListView.as_view(), name='filtered_list'),
    #path('decks/', views.DecksListView.as_view(), name='decks'),

    # Card View
    path('card-details/<str:number>', views.CardDetailView.as_view(), name='card_view'),

    # General Landing Page
    path('', views.CardsIndexView.as_view(), name='cards'),
]
