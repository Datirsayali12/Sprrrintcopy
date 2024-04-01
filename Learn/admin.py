

# Register your models here.
from django.contrib import admin
from .models import *


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'overview', 'creator', 'category', 'created_at', 'updated_at']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'video', 'is_liked', 'created_at', 'updated_at']


@admin.register(Dislike)
class DislikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'video', 'is_disliked', 'created_at', 'updated_at']


@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ['user', 'video', 'is_shared', 'created_at', 'updated_at']


@admin.register(LikesDislikesCount)
class LikesDislikesCountAdmin(admin.ModelAdmin):
    list_display = ['video', 'likes', 'dislikes', 'shares', 'created_at', 'updated_at']


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['course_hrs', 'assignments_and_projects', 'quizzes', 'created_at', 'updated_at']


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'short_desc', 'creator', 'long_desc', 'category', 'created_at', 'updated_at',
                    'course_level']


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(CourseVideo)
class CourseVideoAdmin(admin.ModelAdmin):
    list_display = ['course_video_url', 'section', 'course']


@admin.register(WatchedVideo)
class WatchedVideoAdmin(admin.ModelAdmin):
    list_display = ['video', 'is_completed', 'user', 'created_at', 'updated_at']


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['file', 'created_at', 'updated_at']


@admin.register(Ebook)
class EbookAdmin(admin.ModelAdmin):
    list_display = ['no_of_chapters', 'no_of_pages', 'description', 'creator', 'category', 'ebook_desc',
                    'created_at', 'updated_at', 'level']


@admin.register(Requirement)
class RequirementAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']


@admin.register(CourseReview)
class CourseReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'text', 'rating', 'course', 'created_at', 'updated_at']


@admin.register(EbookReview)
class EbookReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'text', 'rating', 'ebook', 'created_at', 'updated_at']


@admin.register(UserWallet)
class UserWalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')


@admin.register(CourseTransaction)
class CourseTransactionAdmin(admin.ModelAdmin):
    list_display = ['credit_amount', 'debit_amount', 'tran_type', 'user', 'course', 'created_at', 'updated_at']


@admin.register(EbookTransaction)
class EbookTransactionAdmin(admin.ModelAdmin):
    list_display = ['credit_amount', 'debit_amount', 'tran_type', 'user', 'Ebook', 'created_at', 'updated_at']


@admin.register(SavedCourse)
class SavedCourseAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'created_at', 'updated_at')


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('course', 'questions', 'question_image', 'section')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'is_correct')


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('date', 'venu', 'course', 'user')