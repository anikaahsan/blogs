from django.contrib import admin
from .import models

# Register your models here.
@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
    list_display=['title','author','date','category']
    list_filter=['author','date','title','category']
    list_editable=['date']
    prepopulated_fields={'slug':["title"]}
    

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display=['email','text','post']

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['title']


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display=['title']
