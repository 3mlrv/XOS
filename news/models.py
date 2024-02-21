from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.views.generic import ListView, DetailView
from django.core.validators import MinValueValidator


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)


    def update_rating(self):
        posts_rating = Post.objects.filter(author=self).aggregate(pr=Coalesce(Sum('rating'), 0))['pr']
        comments_rating = Comment.objects.filter(user=self.user).aggregate(cr=Coalesce(Sum('rating'), 0))['cr']
        posts_comments_rating = Comment.objects.filter(post__author=self).aggregate(pcr=Coalesce(Sum('rating'), 0))['pcr']

        print(posts_rating)
        print('---------------')
        print(comments_rating)
        print('---------------')
        print(posts_comments_rating)

        self.rating = posts_rating * 3 + comments_rating + posts_comments_rating
        self.save()




class Category(models.Model):
    name = models.CharField(max_length=110, unique=True)
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories')

    def __str__(self):
        return self.name

class Post(models.Model):
    article = "AR"
    news = "NE"
    

    POSITIONS = [
        (article, "Статья"),
        (news, "Новости"),
        
    ]
    
    post_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=2, choices=POSITIONS, default=news)
    category = models.ManyToManyField(Category, through="PostCategory", related_name="posts_categories")
    title = models.CharField(max_length=255)
    text = models.TextField()
    rating = models.IntegerField(default=0)


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


    def preview(self):
        small_text = self.text[0:124] + '...'
        return small_text
    

    def __str__(self):
        return f'id-{self.pk}: {self.title}'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class NewsSearch(ListView):
    model = Post
    ordering = '-post_time'
    template_name = 'search.html'
    context_object_name = 'posts'



class Comment(models.Model):
    text = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_time = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    
    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


