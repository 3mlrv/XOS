from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .models import Post
from .filters import PostFilter
from .forms import ProductForm
from django.http import Http404


class NewsList(ListView):
    model = Post
    template_name = 'post_list.html'
    context_object_name = 'posts'
    ordering = '-post_time'
    paginate_by = 10


    def get_queryset(self):
       
       queryset = super().get_queryset()
     
       self.filterset = PostFilter(self.request.GET, queryset)
       
       return self.filterset.qs

    
    def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       
       context['filterset'] = self.filterset
       return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'post_detail.html'
    context_object_name = 'post'

class NewsFilterList(ListView):
    model = Post
    ordering = '-post_time'
    context_object_name = 'posts'
    paginate_by = 10
    template_name = 'search.html'
   
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        page = context['page_obj']
        context['paginator_range'] = page.paginator.get_elided_page_range(
            page.number, on_each_side=1, on_ends=1)
        context['filterset'] = self.filterset
        return context

class NewsCreate(CreateView):
    
    form_class = ProductForm
    model = Post
    template_name = 'post_edit.html'
    success_url = '/news/'

    def form_valid(self, form):
        
        post = form.save(commit=False)
        if self.request.path == '/articles/create/':
            post.type = 'AR'
        post.save()
        return super().form_valid(form)
        

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['get_title'] = self.get_type()['title']
        context['get_type'] = self.get_type()['content']
        return context


    def get_type(self):
        if self.request.path == '/articles/create/':
            return {'title': 'Create article', 'content': 'Добавить статью'}
        else:
            return {'title': 'Create news', 'content': 'Добавить новость'}

class NewsEdit(UpdateView):
    form_class = ProductForm
    model = Post
    template_name = 'post_edit.html'
    # success_url = '/news/'

    def form_valid(self, form):
        post = form.save(commit=False)
        if 'articles' in self.request.path:
            post.type = 'AR'  
        else:
            post.type = 'NE'  
        post.save()
        return super().form_valid(form)
    

    def get_context_data(self, **kwargs):
        
        context = super().get_context_data(**kwargs)
        context['get_title'] = self.get_type()['title']
        context['get_type'] = self.get_type()['content']
        return context

    def get_type(self):
        if 'articles' in self.request.path:
            return {'title': 'Edit article', 'content': 'Редактировать статью'}
        else:
            return {'title': 'Edit news', 'content': 'Редактировать новость'}
    
    



class NewsDelete(DeleteView):
    model = Post
    template_name = 'delete.html'
    success_url = reverse_lazy('post_list')

    