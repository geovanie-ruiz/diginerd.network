from django.urls import path

from . import views

urlpatterns = [
    # General Landing Page
    path('', views.IndexView.as_view(), name='cards'),

    # Specific Series
    #path('decks/', views.DecksListView.as_view(), name='decks'),
    path('trial-sets/', views.TrialSetListView.as_view(), name='trials'),
    path('boosters/', views.BoosterSetListView.as_view(), name='boosters'),
    #path('rulings/', views.RulingsListView.as_view(), name='rulings'),
    #path('errata/', views.ErrataListView.as_view(), name='errata'),

    # Specific Article
    #path('decks/<slug:slug>/', views.DeckView.as_view(), name='deck_view'),
    path('trial-sets/<slug:slug>/',
         views.TrialSetDetailView.as_view(), name='trial_set_view'),
    path('boosters/<slug:slug>/', views.BoosterSetDetailView.as_view(),
         name='booster_set_view'),
    #path('rulings/<slug:slug>/', views.RulingsDetailView.as_view(), name='rulings_view'),
    #path('errata/<slug:slug>/', views.ErrataDetailView.as_view(), name='errata_view'),

    # POST paths
    path('load-cards/', views.lazy_load_cards, name='lazy_load_cards'),
]
