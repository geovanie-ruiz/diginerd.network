from django.urls import path

from . import views

urlpatterns = [
    # General Landing Page
    path('', views.CardsIndexView.as_view(), name='cards'),

    # Filtered Card Lists
    path('sets/', views.SetListView.as_view(), name='sets'),
    path('trial-sets/', views.TrialSetListView.as_view(), name='trials'),
    path('booster-sets/', views.BoosterSetListView.as_view(), name='boosters'),
    #path('decks/', views.DecksListView.as_view(), name='decks'),

    # Card View
    path('card-details/<str:number>', views.CardDetailView.as_view(), name='card_view'),

    # POST paths
    path('load-cards/', views.lazy_load_cards, name='lazy_load_cards'),
]
