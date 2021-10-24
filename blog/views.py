from django.shortcuts import render
from django.views import generic
from .models import Post, Comment
from .forms import CommentForm, PostForm
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy


# Create your views here.

class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'

def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True).order_by("-created_on")
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})

def delete_comment(request, comment_id):
    comments = Comment.objects.get(id=int(comment_id))
    comments.delete()
    return HttpResponseRedirect(reverse_lazy('home'))

def add_post(request):
    template = "add_post.html"
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse_lazy('blog:home'))
    else:
        context = {
            'post_form': PostForm(),
        }
        return render(request, template, context)

def update_post(request, post_id):
    template = "update_post.html"
    post = Post.objects.get(id=int(post_id))

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse_lazy('blog:home'))
    else:
        context = {
            'post_form': PostForm(instance=post),
        }
        return render(request, template, context)
