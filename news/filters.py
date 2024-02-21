from django_filters import FilterSet, ModelChoiceFilter, DateFilter, CharFilter
from .models import Post, Author, Category
from django import forms
import django_filters



class PostFilter(FilterSet):
   
        
   class Meta:
      
       model = Post
       
       fields = {
       
           'title': ['icontains',],
           'author': ['exact'],
        #    'post_time': ['gt'],
        }
#    title = CharFilter(
#         label='Содержит',
#         lookup_expr='icontains'
#     )
#    author = ModelChoiceFilter(
#         queryset=Author.objects.all(),
#         lookup_expr='exact',
#         label='Автор',
#         empty_label='Все авторы',
#     )
#    post_time = DateFilter(
#         label='Опубликованы после',
#         lookup_expr='gt',
#     )
   
   start_date = django_filters.DateFilter(field_name="post_time", lookup_expr='gte', widget=forms.DateInput(attrs={'type': 'date'}), label='Дата публикации начиная с')

   end_date = django_filters.DateFilter(field_name="post_time", lookup_expr='lte', widget=forms.DateInput(attrs={'type': 'date'}), label='Дата публикации до' )


