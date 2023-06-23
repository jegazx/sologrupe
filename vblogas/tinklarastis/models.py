from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from tinymce.models import HTMLField
import subprocess


User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = _("category")
        verbose_name_plural = _("categorys")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"pk": self.pk})
    
class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = HTMLField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(Category)
    image = models.ManyToManyField('Image', blank=True)
    videos = models.ManyToManyField('Video', blank=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)

    class Meta:
        verbose_name = _("blogpost")
        verbose_name_plural = _("blogposts")

    def __str__(self):
        return f'{self.title} by {self.author} at {self.created_at}'

    def get_absolute_url(self):
        return reverse("blogpost_detail", kwargs={"pk": self.pk})
    
class Image(models.Model):
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name='image_posts')

    

    class Meta:
        verbose_name = _("Image")
        verbose_name_plural = _("Images")

    def __str__(self):
        return self.image.name

    def get_absolute_url(self):
        return reverse("Image_detail", kwargs={"pk": self.pk})


class Video(models.Model):
    video = models.FileField(upload_to='media/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='thumbnails/', null=True, blank=True)

    class Meta:
        verbose_name = _("Video")
        verbose_name_plural = _("Videos")

    def __str__(self):
        return self.video.name

    def get_absolute_url(self):
        return reverse("Video_detail", kwargs={"pk": self.pk})



class Comment(models.Model):
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(BlogPost, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")

    def __str__(self):
        return f'{self.author} commented on {self.post} at {self.created_at}'

    def get_absolute_url(self):
        return reverse("comment_detail", kwargs={"pk": self.pk})
    