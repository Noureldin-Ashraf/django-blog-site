from django.shortcuts import render, get_object_or_404
from datetime import date
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.views import View

from .models import Post, Comment
from .forms import CommentForm


# Class Based Approach
class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]
    # change the returned object name to posts
    context_object_name = "posts"

    # override the get_queryset function to manipulate returned data
    def get_queryset(self):
        queryset = super().get_queryset()
        data = queryset[:3]
        return data


class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    context_object_name = "all_posts"
    ordering = ["-date"]


class SinglePostView(View):

    # check if post is is session stored posts
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts")
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False

        return is_saved_for_later

    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-details.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)

        if comment_form.is_valid():
            # calling commit false will initiate the model object without saving for us to edit it before manually saving
            comment = comment_form.save(commit=False)
            # add the post object to the comment model
            comment.post = post
            comment.save()

            return HttpResponseRedirect(reverse("post-details-page", args=[slug]))

        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": comment_form,
            "comments": post.comments.all().order_by("-id"),
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-details.html", context)


class ReadLaterView(View):
    def get(self, request):
        stored_posts = request.session.get("stored_posts")

        context = {}

        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            # get posts where id in the list of saved ids
            posts = Post.objects.filter(id__in=stored_posts)
            context["posts"] = posts
            context["has_posts"] = True

        return render(request, "blog/stored-posts.html", context)

    def post(self, request):
        stored_posts = request.session.get("stored_posts")

        if stored_posts is None:
            stored_posts = []

        post_id = int(request.POST["post_id"])

        if post_id not in stored_posts:
            stored_posts.append(post_id)
        else:
            stored_posts.remove(post_id)

        request.session["stored_posts"] = stored_posts

        return HttpResponseRedirect("/")


# # Detail View Approach before needing to revert back to view for form submission (FOR REFERENCE)

# class SinglePostView(DetailView):
#     template_name = "blog/post-details.html"
#     model = Post
#     # automatically search by a slug

#     # override get_context_data function to manipulate context for the tags field
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # to access and get all tags from the object
#         context["post_tags"] = self.object.tags.all()
#         # Pass the form in the context
#         context["comment_form"] = CommentForm
#         return context


# # Function Based Approach (FOR REFERENCE)

# def starting_page(request):
#     latest_posts = Post.objects.all().order_by("-date")[:3]
#     return render(request, "blog/index.html", {"posts": latest_posts})

# def posts(request):
#     all_posts = Post.objects.all().order_by("-date")
#     # push all posts to the view
#     return render(request, "blog/all-posts.html", {"all_posts": all_posts})

# def post_details(request, slug):
#     target_post = get_object_or_404(Post, slug=slug)
#     return render(request, "blog/post-details.html", {
#         "post": target_post,
#         "post_tags": target_post.tags.all()
#     })
