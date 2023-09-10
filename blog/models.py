from django.db import models
from django.core.validators import MinLengthValidator


# TAG CLASS
class Tag(models.Model):
    caption = models.CharField(max_length=20)

    def __str__(self):
        return self.caption


# AUTHOR CLASS
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email_address = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# POST CLASS
class Post(models.Model):
    title = models.CharField(max_length=150)
    excerpt = models.CharField(max_length=200)
    image_name = models.CharField(max_length=100)
    date = models.DateField(auto_now=True)
    slug = models.SlugField(unique=True)
    content = models.TextField(validators=[MinLengthValidator(10)])
    # ForeignKey is used for one to many relations
    author = models.ForeignKey(
        Author, on_delete=models.SET_NULL, null=True, related_name="posts")
    # ManyToManyField is used for the many to many realtions
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f"{self.title} by {self.author.first_name}"
