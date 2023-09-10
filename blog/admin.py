from django.contrib import admin
from .models import Post, Author, Tag


# create a post admin class to customize how to display the post model in the admin panel
class PostAdmin(admin.ModelAdmin):
    # define a tuple with fields that we can filter with
    list_filter = ("author", "tags", "date",)
    # define a tuple with fields to display
    list_display = ("title", "date", "author",)
    # define a dictionary with prepopulated fields
    prepopulated_fields = {"slug": ("title",)}


# Register models in the admin panel
# load admin class with the main class
admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Tag)
