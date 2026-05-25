"""
URL configuration for photo_album_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from albums import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='albums/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='album-list'), name='logout'),

    path('', views.AlbumListView.as_view(), name='album-list'),
    path('album/new/', views.AlbumCreateView.as_view(), name='album-create'),
    path('album/<int:pk>/', views.AlbumDetailView.as_view(), name='album-detail'),
    path('album/<int:pk>/edit/',
         views.AlbumUpdateView.as_view(), name='album-update'),
    path('album/<int:pk>/delete/',
         views.AlbumDeleteView.as_view(), name='album-delete'),
    path('album/<int:album_id>/add-photo/',
         views.PhotoUploadView.as_view(), name='photo-upload'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
