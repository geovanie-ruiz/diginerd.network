from django.urls import path

from network import views

urlpatterns = [
    # General Landing Page
    path('', views.IndexView.as_view(), name='index'),
    
    # Network
    #     Article Categories List View
    path('network/', views.ArticleCategoriesListView.as_view(), name='network'),
    #     Article Category List/Articles filtered by Category
    path('network/series/<int:pk>/', views.ArticlesByArticlesCategoryView.as_view(), name='articles_by_article_category'),
    #     Article View
    path('network/<slug:slug>/', views.ArticleDetailView.as_view(), name='article'),
    
    # Digifiction
    #     Landing page
    #path('digifiction/', views.StoryListView.as_view(), name='story'),
    #     Digifiction Categories View
    #path('digifiction/series/', views.SeriesListView.as_view(), name='story_series'),
    #     Digifiction Category List
    #path('digifiction/series/<int:pk>/', views.SeriesListView.as_view(), name='story_series_list'),
    #     Digifiction Article View
    #path('digifiction/<slug:slug>/', views.StoryDetailView.as_view(), name='story_article'),
    
    # Local Game Store
    #     LGS Category (State) List
    #path('lgs/', views.ShopListView.as_view(), name='lgs'),
    #     LGS State View/LGS List filtered by State
    #     LGS View
    #path('lgs/<int:pk>/', views.ShopDetailView.as_view(), name='lgs_info'),
    #     LGS Entry form
    #path('lgs/new/', views.ShopAddView.as_view(), name='new_lgs'),

    # Specific Series
    #path('decks/', views.DecksListView.as_view(), name='decks'),
    path('trial-sets/', views.TrialSetListView.as_view(), name='trials'),
    path('boosters/', views.BoosterSetListView.as_view(), name='boosters'),
    #path('rulings/', views.RulingsListView.as_view(), name='rulings'),
    #path('errata/', views.ErrataListView.as_view(), name='errata'),

    # Specific Article
    #path('decks/<slug:slug>/', views.DeckView.as_view(), name='deck_view'),
    path('trial-sets/<slug:slug>/', views.TrialSetDetailView.as_view(), name='trial_set_view'),
    path('boosters/<slug:slug>/', views.BoosterSetDetailView.as_view(), name='booster_set_view'),
    #path('rulings/<slug:slug>/', views.RulingsDetailView.as_view(), name='rulings_view'),
    #path('errata/<slug:slug>/', views.ErrataDetailView.as_view(), name='errata_view'),

    # Hard-coded Pages
    path('gameplay/', views.GameplayView.as_view(), name='gameplay'),
    path('rules/', views.RulesView.as_view(), name='rules'),
    path('colors/', views.ColorsView.as_view(), name='colors'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('terms/', views.TermsView.as_view(), name='terms'),
    path('roadmap/', views.RoadmapView.as_view(), name='roadmap'),

    # Comments lazy-loading
    path('comments/', views.lazy_load_comments, name='lazy_load_comments'),
]
