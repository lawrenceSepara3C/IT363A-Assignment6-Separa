from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Album, Photo
from django.shortcuts import get_object_or_404


class AlbumListView(LoginRequiredMixin, ListView):
    model = Album
    template_name = 'albums/album_list.html'
    context_object_name = 'albums'

    def get_queryset(self):
        # RBAC: Administrators see all albums. Standard users only see public or owned items.
        if self.request.user.groups.filter(name='Administrators').exists():
            return Album.objects.all()
        return Album.objects.filter(Q(is_public=True) | Q(owner=self.request.user))


class AlbumDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Album
    template_name = 'albums/album_detail.html'
    context_object_name = 'album'

    def test_func(self):
        album = self.get_object()
        is_admin = self.request.user.groups.filter(
            name='Administrators').exists()
        return album.is_public or album.owner == self.request.user or is_admin


class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    fields = ['title', 'description', 'is_public']
    template_name = 'albums/album_form.html'
    success_url = reverse_lazy('album-list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class AlbumUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Album
    fields = ['title', 'description', 'is_public']
    template_name = 'albums/album_form.html'
    success_url = reverse_lazy('album-list')

    def test_func(self):
        album = self.get_object()
        is_admin = self.request.user.groups.filter(
            name='Administrators').exists()
        return album.owner == self.request.user or is_admin


class AlbumDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Album
    template_name = 'albums/album_confirm_delete.html'
    success_url = reverse_lazy('album-list')

    def test_func(self):
        album = self.get_object()
        is_admin = self.request.user.groups.filter(
            name='Administrators').exists()
        return album.owner == self.request.user or is_admin


class PhotoUploadView(LoginRequiredMixin, CreateView):
    model = Photo
    fields = ['title', 'image']
    template_name = 'albums/photo_form.html'

    def form_valid(self, form):
        # Dynamically link this photo to the specific album id passed in the URL
        album_id = self.kwargs.get('album_id')
        form.instance.album = get_object_or_404(
            Album, id=album_id, owner=self.request.user)
        return super().form_valid(form)

    def get_success_url(self):
        # Redirect back to the album detail view after upload succeeds
        return reverse_lazy('album-detail', kwargs={'pk': self.kwargs.get('album_id')})
