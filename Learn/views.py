from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import status
from .models import *
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_video_details(request,video_id):
    try:
        video= Video.objects.get(id=video_id)
        video_details= {
            "title": video.title,
            "hero_video_url": video.hero_video_url,
            "overview": video.overview,
            "creator": video.creator.id,
            "category": video.category.id,
            "created_at": video.created_at,
            "updated_at": video.updated_at,
        }
        return Response(video_details)
    except Video.DoesNotExist:
        return Response({'error': 'Video not found'}, status=404)







@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_course_requirements(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    requirements = Requirement.objects.filter(course=course)

    requirement_list = []
    for requirement in requirements:
        requirement_data = {
            "requirement_id": requirement.requirement_id,
            "requirement_name": requirement.requirement_name,
            "created_at": requirement.created_at,
            "updated_at": requirement.updated_at
        }
        requirement_list.append(requirement_data)

    return JsonResponse({"requirements": requirement_list})



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_ebook(request, ebook_id):
    ebook = get_object_or_404(Ebook, pk=ebook_id)
    ebook_images = EbookImages.objects.filter(Ebook_id=ebook_id)

    ebook_data = {
        "ebook_id": ebook.id,
        "no_of_chapter": ebook.no_of_chapters,
        "no_of_pages": ebook.no_of_pages,
        "description": ebook.description,
        "creator_id": ebook.creator_id,
        "ebook_desc": ebook.ebook_desc,
        "created_at": ebook.created_at,
        "updated_at": ebook.updated_at,
        "level_id": ebook.level_id,
        "content_id": ebook.content_id,
        "images": []
    }

    for image in ebook_images:
        ebook_data["images"].append({
            "ebook_image_id": image.id,
            "ebook_image_url": image.ebook_image_url
        })

    return JsonResponse(ebook_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_ebook(request):
    user = request.user 
    ebook_id= request.data.get('ebook_id')  

    if ebook_id is None:
        return Response({"error": "Ebook ID is required"}, status=400)

    
    saved_ebook = Ebook.objects.create(user=user, ebook_id=ebook_id)

    return Response({"message": "Ebook saved successfully"}, status=201)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_course(request):
    user = request.user 
    course_id= request.data.get('course_id')  

    if course_id is None:
        return Response({"error": "Course ID is required"}, status=400)

    
    saved_course = Course.objects.create(user=user, course_id=course_id)

    return Response({"message": "Course saved successfully"}, status=201)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_course_details(request, course_id):
    course = get_object_or_404(Course, pk=course_id)

    course_data = {
        "course_id": course.id,
        "course_name": course.name,
        "short_description": course.short_desc,
        "course_lesson": course.course_lesson,
        "creator_id": course.creator_id,
        "long_description": course.long_desc,
        "category_id": course.category_id,
        "created_at": course.created_at,
        "updated_at": course.updated_at,
        "content_id": course.content_id,
        "course_level_id": course.course_level_id,
    }

    return JsonResponse(course_data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_course_reviews(request, course_id):
    reviews = CourseReview.objects.filter(course_id=course_id)

    review_list = []
    for review in reviews:
        review_data = {
            "user_id": review.user_id,
            "text": review.text,
            "rating": review.rating,
            "course_id": review.course_id,
            "created_at": review.created_at,
            "updated_at": review.updated_at
        }
        review_list.append(review_data)

    return JsonResponse({"course_reviews": review_list})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_ebook_reviews(request, ebook_id):
    reviews = EbookReview.objects.filter(ebook_id=ebook_id)

    review_list = []
    for review in reviews:
        review_data = {
            "user_id": review.user_id,
            "text": review.text,
            "rating": review.rating,
            "course_id": review.ebook_id,
            "created_at": review.created_at,
            "updated_at": review.updated_at
        }
        review_list.append(review_data)

    return JsonResponse({"Ebook_reviews": review_list})


