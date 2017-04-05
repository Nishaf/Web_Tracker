from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate, login,logout,user_logged_in
from .forms import *
from .extra_functions import *
from pymongo import *
##PrimaryKey== Sector + user + timestamp

class HomePage(View):
    def get(self, request):
        db = MongoClient()['Database1']
        context1 = db.Table_data.find()
        MongoClient().close()
        for i in context1:
            posts = i


        return render(request,'check.html', {'posts': posts})

class Add_Post(View):
    def get(self, request):
        return render(request, 'add_post.html')

    def post(self, request):
        db = MongoClient()['Database1']
        context1 = get_post_data(request)
        db.Table_data.insert(get_post_data(request))
        print(context1['Cluster'])
        MongoClient().close()
        return redirect('homepage')




class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('index')

class Login(View):
    #@my_login_required
    def post(self,request):
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session['username'] = user.username
                return render(request, 'home.html', {'name':user})
            else:
                return render(request, 'login.html', {'error_message': 'Invalid login'})
        return render(request, 'login.html')

class SignUp(View):
    #@my_login_required
    def get(self, request):
        form = UserForm(request.GET or None)
        return render(request, 'signup.html', context={'form':form})

    def post(self, request):
        form = UserForm(request.POST or None)
        print("Form")
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    request.session['username'] = user.username
                    return redirect('index')
        else:
            context = {
                'form': form,
            }
            return render(request, 'signup.html',context)

