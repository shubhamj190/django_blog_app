from django.shortcuts import render, HttpResponse, redirect
from dapp.models import Post
from dapp.models import Post

# Create your views here.

def home(request):
    post = Post.objects.all().order_by('-views')[0:3]
    return render(request,'home/index.html', {'context':post})
    
def about(request):
    return HttpResponse('we are in about home page')


from .models import Contact
from django.contrib import messages

def contact(request):
    if request.method=="POST":
        name=request.POST['name']
        email=request.POST['email']
        contact=request.POST['contact']
        query=request.POST['query']
        if len(name)<2 or len(email)<3 or len(contact)<3 or len(query)<3:
            messages.error(request,'Please fill the form correctly')
        else: 
            contact=Contact(name=name, email=email,contact=contact, query=query)
            contact.save()
            messages.success(request,'Your message has been sent succussfully !!')
    return render(request,'home/contact.html')

def search(request):
    search=request.GET['search']
    if len(search)>78:
        allPosts=Post.objects.none()
    else:
        allPostsTitle= Post.objects.filter(title__icontains=search)
        allPostsAuthor= Post.objects.filter(author__icontains=search)
        allPostsContent =Post.objects.filter(content__icontains=search)
        allPosts=  allPostsTitle.union(allPostsContent, allPostsAuthor)
    if allPosts.count()==0:
        messages.warning(request, "No search results found. Please refine your query.")
    data={'allPosts': allPosts,'search': search}
    return render(request,'home/search.html',data)

from django.contrib.auth.models import User

def signup(request):
    if request.method=='POST':
        username=request.POST['username']
        fname=request.POST['fname']
        lname=request.POST['lname']
        email=request.POST['email']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        #check for errorneous input
        if len(username)>10:
            messages.error(request,"User name should not be greater than 10 character")
            return redirect('/')

        if pass1!=pass2:
            messages.error(request,"password is not matching , please enter the correct password")
            return redirect('/')

        if not username.isalnum():
            messages.error(request,"Username should only contain letters and numbers")
            return redirect('/')

        #create the user
        myUser =User.objects.create_user(username,email,pass1)
        myUser.first_name=fname
        myUser.last_name=lname
        myUser.save()
        messages.success(request,"your account has been created successfully")
        return redirect('/')
    else:
        return HttpResponse('something is wrong')

from django.contrib.auth import authenticate, login, logout

def handleLogin(request):
        if request.method=="POST":
        # Get the post parameters
            loginusername=request.POST['loginusername']
            loginpassword=request.POST['loginpassword']

            user=authenticate(username= loginusername, password= loginpassword)
            if user is not None:
                login(request,user)
                messages.success(request, "Successfully Logged In")
                return redirect("/")
            else:
                messages.error(request, "Invalid credentials! Please try again")
                return redirect("/")

            return HttpResponse("404- Not found")
   

            return HttpResponse("login")
        


def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/')


