from django.urls import path

from network import views

urlpatterns = [
    # General Landing Page
    path('', views.IndexView.as_view(), name='index'),

    # Network
    #     Article Categories List View
    path('network/', views.ArticleCategoriesListView.as_view(), name='network'),
    #     Article Category List/Articles filtered by Category
    path('network/series/<int:pk>/', views.ArticlesByArticlesCategoryView.as_view(),
         name='articles_by_article_category'),
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

    # Hard-coded Pages
    path('gameplay/', views.GameplayView.as_view(), name='gameplay'),
    path('rules/', views.RulesView.as_view(), name='rules'),
    path('colors/', views.ColorsView.as_view(), name='colors'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('terms/', views.TermsView.as_view(), name='terms'),
    path('roadmap/', views.RoadmapView.as_view(), name='roadmap'),

    # POST paths
    path('load-articles/', views.lazy_load_articles, name='lazy_load_articles'),
    path('load-comments/', views.lazy_load_comments, name='lazy_load_comments'),
    path('new-comment/', views.store_comment, name='new_comment'),
]
