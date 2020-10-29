from django.shortcuts import render, HttpResponse, redirect
from .models import Post, BlogComment
from django.contrib import messages 
from django.contrib.auth.models import User
from dapp.templatetags import extras
# Create your views here.

def blogHome(request):
    allPost=Post.objects.all()
    data={'allPost':allPost}
    print(data)
    return render(request,'dapp/bloghome.html', data)

def blogPost(request, slug): 
    post=Post.objects.filter(slug=slug).first()
    post.views=post.views +1
    post.save()
    comments= BlogComment.objects.filter(post=post, parent=None)
    replies= BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    print(replyDict)
    context={'post':post, 'comments': comments, 'user': request.user, 'replyDict':replyDict}
    return render(request, "dapp/blogpost.html", context)

def postComment(request):
    if request.method == "POST":
        comment=request.POST.get('comment')
        print(comment)
        user=request.user
        print(user)
        postSno =request.POST.get('postSno')
        print('postSno------->',postSno)
        post= Post.objects.get(sno=postSno)
        print( print('post------->',post))
        parentSno= request.POST.get('parentSno')
        if parentSno=="":
            comment=BlogComment(comment= comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent= BlogComment.objects.get(sno=parentSno)
            comment=BlogComment(comment= comment, user=user, post=post , parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")
        
    return redirect(f"/blog/{post.slug}")