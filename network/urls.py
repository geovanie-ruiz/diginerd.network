from django.urls import path

from network import views

urlpatterns = [
    # General Landing Page
    path('', views.IndexView.as_view(), name='index'),

    # Network
    path('network/', views.ArticleCategoriesListView.as_view(), name='network'),
    path('network/series/<int:pk>/', views.ArticlesByArticlesCategoryView.as_view(),
         name='articles_by_article_category'),
    path('network/<slug:slug>/', views.ArticleDetailView.as_view(), name='article'),

    # Cards
    #path('rulings/', views.RulingsListView.as_view(), name='rulings'),
    #path('rulings/<slug:slug>/', views.RulingsDetailView.as_view(), name='rulings_view'),
    #path('errata/', views.ErrataListView.as_view(), name='errata'),
    #path('errata/<slug:slug>/', views.ErrataDetailView.as_view(), name='errata_view'),

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
]
