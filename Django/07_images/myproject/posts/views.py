from django.shortcuts import render,get_object_or_404
from .models import Post
from django.http import HttpResponse

# Create your views here.
def posts_list(request):
    all_posts= Post.objects.all().order_by('-date') #newest first
    return render(request,'posts/posts_list.html',{'posts':all_posts});

def post_page(request,slug):
    my_post= get_object_or_404(Post,slug=slug  )
    return render(request,'posts/post_page.html',{'post':my_post});