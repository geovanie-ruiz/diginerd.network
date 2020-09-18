from django.urls import path

from network import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('story/', views.StoryListView.as_view(), name='story'),
    path('story/<slug:slug>/', views.StoryDetailView.as_view(), name='story_article'),
    path('network/', views.ArticleListView.as_view(), name='network'),
    path('network/<slug:slug>/', views.ArticleDetailView.as_view(), name='article'),
    path('series/', views.SeriesListView.as_view(), name='series'),
    path('series/<int:pk>/', views.SeriesDetailView.as_view(), name='series_list'),
]
