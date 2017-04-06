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
import xlrd

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
            db.Table_data.insert({
                    'timestamp': time,
                    'username': request.session['username'],
                    'Sector':sheet.cell_value(i,0),
                    'Cluster':sheet.cell_value(i,1),
                    'Sub-Cluster':sheet.cell_value(i,2),
                    'Congested':sheet.cell_value(i,3),
                    'Leakage':sheet.cell_value(i,4),
                    'DCR':sheet.cell_value(i,5),
                    'AFR':sheet.cell_value(i,6),
                    'Misc':sheet.cell_value(i,7),
                    'Analysis(Why this site is on the list)':sheet.cell_value(i,8),
                    'Last updated (Date)':sheet.cell_value(i,9),
                    'Comments (What can be done short term)':sheet.cell_value(i,10),

                    'Optimization Completed(Yes/No)':sheet.cell_value(i,11),
                    'Status(Complete/In-progress)':sheet.cell_value(i,12),
                    'Perm Solution (Describe the solution)':sheet.cell_value(i,13),
                    'Development Priority':sheet.cell_value(i,14),
                    'Cell Split':sheet.cell_value(i,15),
                    'Coverage Strategy':sheet.cell_value(i,16),
                    'DART':sheet.cell_value(i,17),
                    'Hardening National':sheet.cell_value(i,18),
                    'L1900 Capacity':sheet.cell_value(i,19),
                    'L2100 Capacity':sheet.cell_value(i,20),
                    'L700':sheet.cell_value(i,21),
                    'Market Infill':sheet.cell_value(i,22),
                    'Modernization':sheet.cell_value(i,23),
                    'New Build Infill':sheet.cell_value(i,24),
                    'Replacement':sheet.cell_value(i,25),
                    'ROB':sheet.cell_value(i,26),
                    'Rural America':sheet.cell_value(i,27),
                    'Sector Add':sheet.cell_value(i,28),
                    'Small Cell Strategy':sheet.cell_value(i,29),
                    'T-Mobile Store':sheet.cell_value(i,30),
                    'Venue ACS':sheet.cell_value(i,31),
                    'Cell Split ID':sheet.cell_value(i,32),
            })

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
                login(request, user)
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
                    return redirect('index')
        else:
            context = {
                'form': form,
            }
            return render(request, 'signup.html',context)

