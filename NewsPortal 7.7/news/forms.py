from django import forms
from .models import Post
from django.core.exceptions import ValidationError

class ProductForm(forms.ModelForm):
   post_type = forms.CharField(widget=forms.HiddenInput(), required=False)
   
   class Meta:
       model = Post
       fields = [
           'author',
           'post_type',
           'category',
           'title',
           'text',
           'rating',
       ]
   def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        if title is not None and len(title) < 2:
            raise ValidationError({
                "title": "Заголовок не может быть менее 2-х символов."
            })

        return cleaned_data