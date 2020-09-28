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
]
