from django.urls import path

from network import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('digifiction/', views.StoryListView.as_view(), name='story'),
    path('digifiction/<slug:slug>/', views.StoryDetailView.as_view(), name='story_article'),
    path('network/', views.ArticleListView.as_view(), name='network'),
    path('network/<slug:slug>/', views.ArticleDetailView.as_view(), name='article'),
    path('series/', views.SeriesListView.as_view(), name='series'),
    path('series/<int:pk>/', views.SeriesDetailView.as_view(), name='series_list'),
    path('lgs/', views.ShopListView.as_view(), name='lgs'),
    path('lgs/<int:pk>/', views.ShopDetailView.as_view(), name='lgs_info'),
    path('lgs/new/', views.ShopAddView.as_view(), name='new_lgs'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('terms/', views.TermsView.as_view(), name='terms'),
    path('gameplay/', views.GameplayView.as_view(), name='gameplay'),
    path('rules/', views.RulesView.as_view(), name='rules'),
    path('colors/', views.ColorsView.as_view(), name='colors'),
    path('decks/', views.DecksListView.as_view(), name='decks'),
    path('decks/<slug:slug>/', views.DeckView.as_view(), name='deck_view'),
    path('trial-sets/', views.TrialSetListView.as_view(), name='trials'),
    path('trial-sets/<slug:slug>/', views.TrialSetDetailView.as_view(), name='trial_set_view'),
    path('boosters/', views.BoosterSetListView.as_view(), name='boosters'),
    path('boosters/<slug:slug>/', views.BoosterSetDetailView.as_view(), name='booster_set_view'),
    path('rulings/', views.RulingsListView.as_view(), name='rulings'),
    path('rulings/<slug:slug>/', views.RulingsDetailView.as_view(), name='rulings_view'),
    path('errata/', views.ErrataListView.as_view(), name='errata'),
    path('errata/<slug:slug>/', views.ErrataDetailView.as_view(), name='errata_view'),
]
