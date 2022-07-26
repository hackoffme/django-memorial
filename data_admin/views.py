from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, DetailView
from django.db.models import Count
from data_admin.models import Posts, Areas
from . import forms


class PostsMixin:
    def get_user_context(self, **kwargs):
        context = kwargs
        context['areas'] = Areas.objects.annotate(
            Count('posts')).order_by('id')
        return context


class PostsView(PostsMixin, ListView):
    model = Posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context())
        return context

    def get_queryset(self):
        return Posts.objects.filter(is_active=True)


class PostsViewAreas(PostsMixin, ListView):
    model = Posts

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context())
        return context

    def get_queryset(self):
        return Posts.objects.filter(area__slug=self.kwargs['areas_slug'], is_active=True)


class PostShow(PostsMixin, DetailView):
    model = Posts
    slug_url_kwarg = 'post_slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.get_user_context())
        print(context)
        return context


class PostsCreate(CreateView):
    form_class = forms.PostForm
    template_name = 'data_admin/posts_form.html'
    success_url = reverse_lazy('post_view')
