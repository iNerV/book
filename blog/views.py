from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, render, redirect, render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf

from blog.models import Post
from blog.forms import AddPostForm


class PostsListView(ListView):
    model = Post


class PostDetailView(DetailView):
    model = Post


@login_required
def add_post(request):
    c = {}
    if request.method == 'POST':
        form = AddPostForm(request.POST or None)
        c.update(csrf(request))
        if form.is_valid():
            post = form.save(request.user)
            return redirect(post)
    else:
        form = AddPostForm()

    c = RequestContext(request, {'form': form})
    return render_to_response('blog/add_post.html', c)