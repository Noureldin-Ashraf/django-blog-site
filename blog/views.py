from django.shortcuts import render, get_object_or_404
from datetime import date

from .models import Post

# healper function for date sorting


def get_date(post):
    return post['date']


def starting_page(request):
    # adding the minus means that we order in desc// slicing to get first 3 (sql command will be built accordingly)
    latest_posts = Post.objects.all().order_by("-date")[:3]
    # push the latest posts to the view
    return render(request, "blog/index.html", {"posts": latest_posts})


def posts(request):
    all_posts = Post.objects.all().order_by("-date")
    # push all posts to the view
    return render(request, "blog/all-posts.html", {"all_posts": all_posts})


# adding the slug as a parameter for the view function
def post_details(request, slug):
    # use the slug to get the post from the list using next function
    # target_post =Post.objects.get(slug=slug)
    # a better practice to use get_object_or_404
    target_post = get_object_or_404(Post, slug=slug)
    return render(request, "blog/post-details.html", {
        "post": target_post,
        # as its a many to many relation so it cannot be read directly through the post model
        # it should be handled like this unlike the author which is a one to many relation
        "post_tags": target_post.tags.all()
    })
