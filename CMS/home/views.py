from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.

from . models import User, Article, Comment
from . forms import UserForm, CommentForm

def index(request):
    return render(request, 'index.html')

def showUserDetail(request, pk):
    user = get_object_or_404(User, id=pk)
    context = {'user': user}

    return render(request, 'home/user/user_detail.html' , context)

def updateUser(request, pk):
    user = get_object_or_404(User)
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user', pk=pk) 
        
    context = {'form': form}

    return render(request, 'home/user/user_update.html' , context)

def articleList(request): 
    article = Article.objects.all().order_by('-created_at')
    context = {'article': article, }
    return render(request, 'index.html', context)

def articleDetail(request, pk): 
    article = get_object_or_404(Article, id=pk)
    comments = Comment.objects.filter(article=article)
    # context = {'article': article, 'new_comment': new_comment, 'comment_form': comment_form}
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.article = article
            comment.user = request.user
            comment.save()
    else: 
        comment_form = CommentForm()

    return render(request, 'home/article/article_detail.html', {'article': article,
                                                                'comments': comments,
                                                                'comment_form': comment_form})

