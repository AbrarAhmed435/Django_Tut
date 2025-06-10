from django.shortcuts import render,redirect,get_object_or_404
from .models import Post
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from . import forms

# Create your views here.
def posts_list(request):
    all_posts= Post.objects.all().order_by('-date') #newest first
    return render(request,'posts/posts_list.html',{'posts':all_posts});

def post_page(request,slug):
    my_post= get_object_or_404(Post,slug=slug  )
    return render(request,'posts/post_page.html',{'post':my_post});

@login_required(login_url='/users/login/')# this check if user is logged in if not redirect them to /users/login page
def post_new(request):
    if request.method=='POST':
        form=forms.CreatePost(request.POST,request.FILES)
        if form.is_valid():
            newpost=form.save(commit=False)
            newpost.author=request.user
            newpost.save()
            return redirect('posts:list')
    else:   
        form = forms.CreatePost()
    return render(request,'posts/post_new.html',{'form':form})
    
    
