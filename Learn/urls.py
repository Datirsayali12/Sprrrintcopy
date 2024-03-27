"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Learn import views

urlpatterns = [
    path('get-requirments/<int:course_id>', views.get_course_requirements),
    path('get-video-details/<int:video_id>', views.get_video_details),
    path('get-ebook/<int:ebook_id>', views.get_ebook),
    path('save-ebook/', views.save_ebook),
    path('get-course/<int:course_id>', views.get_course_details),
    path('get-course-review/<int:course_id>', views.get_course_reviews),
    path('get-ebook-review/<int:ebook_id>', views.get_ebook_reviews)

]