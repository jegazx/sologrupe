from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.BlogPost)
admin.site.register(models.Comment)
admin.site.register(models.Category)
admin.site.register(models.Image)
admin.site.register(models.Video)
