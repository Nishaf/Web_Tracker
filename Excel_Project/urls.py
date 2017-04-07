"""Excel_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from .views import *
from Excel_Project import settings
from django.contrib.staticfiles import views
from django.views.static import serve
from django.conf.urls.static import static
admin.autodiscover()
urlpatterns = [
    url(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
    url(r'^export_data/', ExportExcel.as_view(), name="export_data"),
    url(r'^blog_view/', BlogView.as_view(), name="blog_view"),
    url(r'^search_results/', SearchPost.as_view(), name="search_post"),
    url(r'^upload_file/', UploadExcelFile.as_view(), name="upload_file"),
    url(r'^view_image/(?P<username>.+)/(?P<timestamp>.+)/(?P<sector>.+)/', RetrieveImage.as_view(), name="retrieve_image"),
    url(r'^add_image/(?P<username>.+)/(?P<timestamp>.+)/(?P<sector>.+)/', AddImage.as_view(), name="add_image"),
    url(r'^edit_post/(?P<username>.+)/(?P<timestamp>.+)/(?P<sector>.+)/', EditPost.as_view(), name='edit_post'),
    url(r'^logout/', Logout.as_view(), name="logout"),
    url(r'^login/', Login.as_view(), name="login"),
    url(r'^signup/', SignUp.as_view(), name="signup"),
    url(r'^add_post/',Add_Post.as_view(), name='Add_Post'),
    url(r'', HomePage.as_view(), name='homepage'),
]



if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

