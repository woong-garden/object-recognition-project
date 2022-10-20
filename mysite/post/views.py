from django.shortcuts import get_object_or_404, render, redirect, get_list_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from user.models import User
from django.db.models import Q
from notification.utilities import create_notification
# Create your views here.

def index(request):
    if request.method == 'GET':
        context = dict()
        context['users'] = User.objects.all()
        context['posts'] = Post.objects.all().order_by('-created_at')
        return render(request, 'post/post/index.html', context=context)
    
@login_required(login_url='user:signin')
def post_detail(request, post_id):
    if request.method == 'GET':
        context = dict()
        context['post'] = Post.objects.get(id=post_id)
        context['comment'] = Comment.objects.filter(post_id=post_id).order_by('-created_at')
        return render(request, 'post/post/post_detail.html', context=context)
    
@login_required(login_url='user:signin')
def my_list(request, user_id):
    if request.method == 'GET':
        context = dict()
        context['user'] = User.objects.get(id=user_id)
        context['posts'] = Post.objects.filter(author=user_id).order_by('-created_at')
        return render(request, 'post/post/post_mylist.html', context=context)

# 게시글 생성
@login_required(login_url='user:signin')
def post_create(request):
    if request.method == 'GET':
        context = dict()
        context['users'] = User.objects.all()
        context['posts'] = Post.objects.all()
        return render(request,'post/post/post_create.html', context=context)
    
    elif request.method =='POST':
        post = Post()
        post.title = request.POST.get('title')
        post.image = request.FILES.get('image')
        post.content = request.POST.get('content')
        post.author = request.user
        post.save()
        return redirect('post:post-detail',post_id=post.id)

#게시글 수정
@login_required(login_url='user:signin')
def post_update(request, post_id):
    if request.method == 'GET':
        post = get_object_or_404(Post,id=post_id)
        if request.user == post.author:
            context={'post':post}
            return render(request,'post/post/post_update.html',context)
        return redirect('/')
    
    elif request.method == 'POST':
        post = Post.objects.get(id=post_id)
        post.title = request.POST.get('title')
        post.image = request.FILES.get('image')
        post.content = request.POST.get('content')
        post.save()
        return redirect('/')
    
#게시글 삭제
@login_required(login_url='user:signin')
def post_delete(request, post_id):
        post = get_object_or_404(Post,id=post_id)
        if request.user == post.author:
            post.delete()
            return redirect('/')
        return redirect(request.META['HTTP_REFERER'])

# 댓글 생성
@login_required(login_url='user:signin')
def comment_create(request, comment_id):
    if request.method == 'POST':
        user = request.user
        post = Post.objects.get(id=comment_id)
        content = request.POST.get('content')
        Comment.objects.create(content=content, author=user, post=post)
        create_notification(request, user, 'comment', post)
        return redirect('post:post-detail', post.id)

#댓글 수정
@login_required(login_url='user:signin')
def comment_update(request, comment_id):
    if request.method == 'GET':
        comment = get_object_or_404(Comment,id=comment_id)
        context={'comment':comment}
        return render(request, 'post/post/comment_update_form.html', context=context)

    elif request.method == 'POST':
        update_comment = Comment.objects.get(id=comment_id)
        post_id = update_comment.post.id
        update_comment.content = request.POST.get('content')
        update_comment.save()
        return redirect('post:post-detail', post_id)

#댓글 삭제
@login_required(login_url='user:signin')
def comment_delete(request, comment_id):
    comment = Comment.objects.get(id=comment_id)
    current_post = comment.post.id
    comment.delete()
    return redirect('post:post-detail', current_post)

#좋아요
@login_required(login_url='user:signin')
def likes(request, post_id):
    if request.method == 'POST':
        user = User.objects.get(id=request.user.id)
        post = Post.objects.get(id=post_id)
    if post.like_authors.filter(id=request.user.id).exists():
        post.like_authors.remove(request.user)
    else:
        post.like_authors.add(request.user)
        create_notification(request, user, 'post_like', post)
        
    return redirect(request.META['HTTP_REFERER'])

#좋아요 리스트
@login_required(login_url='user:signin')
def likes_list(request, post_id):
    if request. method == 'GET':
        context = dict()
        context['user'] = User.objects.get(id=post_id)
        context['liked_posts'] = get_list_or_404(Post,like_authors=post_id)
        return render(request, 'post/post/post_like_list.html', context=context)

#검색
def search(request):
    post_result = Post.objects.all()
    keyword = request.GET.get('keyword')
    if keyword: 
        post_result = post_result.filter(
            # Q 함수 OR조건으로 데이터 조회
            # icontains 대소문자 구분없이 필드에 단어 포함되어 있는지 검사
            Q(title__icontains=keyword) |
            Q(content__icontains=keyword)
        )
    
    return render(request, 'post/post/search_results.html', {'search':post_result ,'keyword':keyword})

#팔로우게시물
@login_required(login_url='user:signin')
def follow_list(request, post_id):
    if request. method == 'GET':
        context = dict()
        context['user'] = User.objects.get(id=post_id)
        context['follow_posts'] = get_list_or_404(Post,author__followers=request.user)
        return render(request, 'post/post/post_following.html', context=context)
