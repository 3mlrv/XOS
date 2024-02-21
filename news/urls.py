from django.urls import path

from .views import NewsList, NewsDetail, NewsFilterList, NewsCreate, NewsEdit, NewsDelete

urlpatterns = [
    path('', NewsList.as_view(), name='post_list'),
    path('search/', NewsFilterList.as_view(), name='post_search'),
    path('<int:pk>/', NewsDetail.as_view(), name='post_detail'),
    path('create/', NewsCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', NewsEdit.as_view(), name='post_edit'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='post_delete'),
    path('articles/create/', NewsCreate.as_view(), name='articles_create'),
    path('articles/<int:pk>/edit/', NewsEdit.as_view(), name='articles_edit'),
    path('articles/<int:pk>/delete/', NewsDelete.as_view(), name='articles_delete'),
]

