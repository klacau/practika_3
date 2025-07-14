from django import forms
from .models import Post, Category

class PostForm(forms.ModelForm):
    slug = forms.CharField(required=True)
    
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'image', 'is_published', 'featured']

    def clean_title(self):
        title = self.cleaned_data['title']
        if not title.strip():
            raise forms.ValidationError("Title cannot be empty")
        return title


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description']