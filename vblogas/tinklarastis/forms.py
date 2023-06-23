from django import forms
from .models import Video, Category, Comment, BlogPost, Image

class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['video']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content', 'featured', 'categories']


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']
        
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']