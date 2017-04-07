from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View
from django.contrib.auth import authenticate, login,logout,user_logged_in
from .extra_functions import *
from pymongo import *
from .forms import *
import xlrd
import os
from Images.models import ExcelFiles
from Excel_Project.settings import MEDIA_URL

class HomePage(View):

    def get(self, request):
        if not request.user.is_authenticated():
            return render(request, 'login.html')
        else:

            mongo = MongoClient()
            db = mongo['Database1']
            context1 = db.Table_data.find()
            mongo.close()
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
        form = ImageForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            instance = form.save()
            instance.save()
            return HttpResponse("Added Successfully")


class RetrieveImage(View):
    def get(self, request, username, timestamp, sector):
        instance = PostImages.objects.all().filter(username=username,timestamp=timestamp, sector=sector)
        path = os.getcwd()
        path = '/'.join(path.split('\\'))
        for i in instance:
            print(path+i.image.url)
           # i.image.url = path+i.image.url
        path = "{0}{1}".format(MEDIA_URL, i.image.url)
        return render(request, 'view_image.html', {'instance': instance, 'path':path})


class UploadExcelFile(View):
    def get(self, request):
        form = UploadFileForm(request.GET or None, request.FILES)
        return render(request, 'upload_file.html', {'form': form, 'username': request.session['username'],
                                                    'timestamp':strftime("%a, %d %b %Y %H:%M:%S", gmtime())})

    def add_posts(self,request, time):
        user = request.session['username']
        file = ExcelFiles.objects.get(username=user,timestamp=time)
        print(file.filee.path)
        book = xlrd.open_workbook(file.filee.path)
        sheet = book.sheet_by_index(0)
        mongo = MongoClient()
        db = mongo['Database1']
        for i in range(1, sheet.nrows):
            if sheet.cell_value(i,0) is None or sheet.cell_value(i,0) is "":
                continue
            else:
                db.Table_data.insert(get_excel_data(i,time, sheet,request))

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            instance = form.save()
            instance.save()
            self.add_posts(request, request.POST['timestamp'])
            return redirect('homepage')


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
                login(request , user)
                request.session['username'] = user.username
                return redirect('homepage')
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
                    return redirect('homepage')
        else:
            context = {
                'form': form,
            }
            return render(request, 'signup.html',context)

