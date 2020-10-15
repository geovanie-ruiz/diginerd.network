"""digimontcg URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.static import serve
from network import views as NetworkViews
from cards import views as CardViews

urlpatterns = [
    # POST paths
    path('load-cards/', CardViews.lazy_load_cards, name='lazy_load_cards'),
    path('load-articles/', NetworkViews.lazy_load_articles, name='lazy_load_articles'),
    path('load-comments/', NetworkViews.lazy_load_comments, name='lazy_load_comments'),
    path('new-comment/', NetworkViews.store_comment, name='new_comment'),

    # Root paths
    path('cards/', include('cards.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('summernote/', include('django_summernote.urls')),
    path('', include('network.urls')),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]