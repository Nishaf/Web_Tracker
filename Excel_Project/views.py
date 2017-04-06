from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.views.generic import View
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate, login,logout,user_logged_in
from .forms import *
from .extra_functions import *
from pymongo import *
import base64
import json
from .forms import *
import tablib

from import_export import resources
from Images.models import ExcelFiles
##PrimaryKey== Sector + user + timestamp

class HomePage(View):

    def get(self, request):
        if not request.user.is_authenticated():
            return render(request, 'login.html')
        else:
            mongo = MongoClient()
            db = mongo['Database1']
            context1 = db.Table_data.find()
            MongoClient().close()
            posts = [post for post in context1]
            mongo.close()
            return render(request,'home.html', {'posts': posts})

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

class EditPost(View):
    def get(self, request, username, timestamp, sector):
        mongo = MongoClient()
        db = mongo['Database1']
        post_data = db.Table_data.find_one({'username':username,'timestamp':timestamp,'Sector':sector})

        return render(request,'edit_post.html', {'post':post_data,
                                                'username':username,
                                                 'timestamp':timestamp,
                                                'sector':sector})

    def post(self, request, username, timestamp, sector):
        mongo = MongoClient()
        db = mongo['Database1']
        db.Table_data.update({'username':username,'timestamp':timestamp,'Sector':sector},get_post_data(request))
        mongo.close()
        return HttpResponse("Successful")

class AddImage(View):
    def insert_image(self,request):
        with open("E:/6th Semester/Psychology/Pyschology notes/3.jpeg", "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())
        print(encoded_string)
        mongo = MongoClient()
        db = mongo['Database1']
        db.images.insert({"username": request.session['username'] ,"image":encoded_string})




    def retrieve_image(self,request):
        mongo = MongoClient()
        db = mongo['Database1']
        dataa = db.images.find_one({'username': request.session['username']})
        print(dataa)
        data = dataa['image']
        data1 = json.loads(json.dumps(data))
        img = data1[0]
        img1 = img['image']
        decode = img1.decode()
        img_tag = '<img alt="sample" src="data:image/png;base64,{0}">'.format(decode)
        return HttpResponse(img_tag)

    def get(self, request, username, timestamp, sector):
        form = PostImages(request.GET or None)
        context = {
            "form": form,
            "username":username,
            "timestamp": timestamp,
            "sector": sector,
        }
        return render(request, "add_image.html", context)

    def post(self, request, username, timestamp, sector):
        print(username)
        print(timestamp)
        print(sector)
        form = ImageForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save()
            instance.save()
            return HttpResponse("Added Successfully")


class RetrieveImage(View):
    def get(self, request, username, timestamp, sector):
        instance = PostImages.objects.all().filter(username=username,timestamp=timestamp, sector=sector)
        return render(request, 'view_image.html', {'instance':instance})


class UploadExcelFile(View):
    def get(self, request):
        form = UploadFileForm()
        return render(request, 'upload_file.html', {'form': form})

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved
            form.save()
            return HttpResponse("Hello")


class BlogView(View):
    def get(self, request):
        mongo = MongoClient()
        db = mongo['Database1']
        context1 = db.Table_data.find()
        MongoClient().close()
        posts = [post for post in context1]
        posts.reverse()
        mongo.close()
        return render(request, 'blog_view.html', {'posts': posts})



class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('homepage')


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

