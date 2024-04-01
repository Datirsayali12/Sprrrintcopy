
from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.db import models
from django.conf import settings

from UIAsset.models import Subcategory, Asset, Pack, TransactionType, Category


# Create your models here.


class Video(models.Model):
    title = models.CharField(max_length=255, help_text="for video title")
    tag= models.CharField(max_length=255, help_text="for video title")
    hero_video_url = models.URLField()
    overview = models.TextField(help_text="for video overview")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="for video creator")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text="for category")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="for refer user")
    video = models.ForeignKey(Video, on_delete=models.CASCADE, help_text="for refer particular video")
    is_liked = models.BooleanField(help_text="is_liked or not")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Dislike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="for refer particular user")
    video = models.ForeignKey(Video, on_delete=models.CASCADE, help_text="for refer video")
    is_disliked = models.BooleanField(help_text="is_disliked or not")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Share(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="for refer particular user")
    video = models.ForeignKey(Video, on_delete=models.CASCADE, help_text="for refer video")
    is_shared = models.BooleanField(help_text="is_shared or not")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LikesDislikesCount(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, help_text="for refer video table")
    likes = models.IntegerField(default=0, help_text="to store total likes of particular video")
    dislikes = models.IntegerField(default=0, help_text="to store total dislikes of particular video")
    shares = models.IntegerField(default=0, help_text="to store total shares of particular video")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Level(models.Model):
    name = models.CharField(max_length=255, help_text="for level like advanced,begineers")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Content(models.Model):
    course_hrs = models.IntegerField(help_text="for course hours")
    assignments_and_projects = models.IntegerField(help_text="for total number of assignment_and_projects")
    quizzes = models.IntegerField(help_text="for number of quizzes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Course(models.Model):
    name = models.CharField(max_length=255, help_text="for course name")
    tag= models.CharField(max_length=255, help_text="for cours tag")
    short_desc = models.TextField(help_text="for course short description")
    course_lesson = models.IntegerField(help_text="for number of course lesson ")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="for course creator")
    long_desc = models.TextField(help_text="for course long description")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text="for course category")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, help_text="For content of course")
    course_level = models.ForeignKey(Level, on_delete=models.CASCADE,
                                     help_text="for refer level like(begineers,advanced)")
    

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=255, help_text="for section name")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CourseVideo(models.Model):
    course_video_url = models.URLField(max_length=200)
    section = models.ForeignKey(Section, on_delete=models.CASCADE,
                                help_text="for refer to which course section related")
    is_hero_video = models.BooleanField(help_text="is course video is on main card video")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, help_text="refer to  course video is belongs")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_free = models.BooleanField(help_text="if video is free or not")


class WatchedVideo(models.Model):
    video = models.ForeignKey(CourseVideo, on_delete=models.CASCADE, help_text="refer to courseVideo")
    is_completed = models.BooleanField(default=False, help_text="is course completed or not (True and False)")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="refer to particular user")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Resource(models.Model):
    video = models.ForeignKey(Video, on_delete=models.CASCADE, help_text="refer to particular video")
    file = models.URLField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Ebook(models.Model):
    name = models.CharField(max_length=100)
    tag = models.CharField(max_length=100)
    no_of_chapters = models.IntegerField(help_text="for number of chapters in Ebook")
    no_of_pages = models.IntegerField(help_text="for number of pages in Ebook")
    description = models.TextField(max_length=255, help_text="for Ebook description")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="for creator of Ebook")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, help_text="For subcategory of Ebook")
    # asset = models.ForeignKey(Asset, on_delete=models.CASCADE,help_text="for store Ebook images")
    content = models.ForeignKey(Content, on_delete=models.CASCADE, help_text="For content of course")
    ebook_desc = models.TextField(max_length=200, help_text="ebook description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, help_text="for refer level like(begineers,advanced)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class EbookImages(models.Model):
    Ebook_url = models.URLField(max_length=200)
    Ebook = models.ForeignKey(Ebook, on_delete=models.CASCADE, help_text="for store Ebook images")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Requirement(models.Model):
    name = models.CharField(max_length=255, help_text="requirment name")
    courses = models.ManyToManyField(Course, related_name='requirements',
                                     help_text="refer to courses to which requirments are belongs")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class CourseReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="refer to user")
    text = models.CharField(max_length=255, help_text="for course review description")
    rating = models.IntegerField(help_text="for course ratings")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, help_text="refer to course")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class EbookReview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="refer to user")
    text = models.CharField(max_length=255, help_text="for course review description")
    rating = models.IntegerField(help_text="for course ratings")
    ebook = models.ForeignKey(Ebook, on_delete=models.CASCADE, null=True, blank=True, help_text="for refer Ebook")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserWallet(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="for refer user")
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="for user balance in wallet")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class CourseTransaction(models.Model):
    credit_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="for credit amount for course")
    debit_amount = models.DecimalField(max_digits=10, decimal_places=2,
                                       help_text="for debit amount record for debit transaction")
    tran_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE,
                                  help_text="refer transaction type i.e purchase ,sale etc.")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="refer particular user")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, help_text="for refer course")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SavedCourse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="refer to user")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, help_text="refer to course")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class Question(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    questions = models.TextField()
    question_image = models.URLField()
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, help_text="questions")
    answer = models.TextField(help_text="for answer")
    is_correct = models.BooleanField(help_text="ans is correct or not")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class SavedEbook(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="refer to user")
    ebook = models.ForeignKey(Ebook, on_delete=models.CASCADE, help_text="refer to course")
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class EbookTransaction(models.Model):
    credit_amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="for credit amount for course")
    debit_amount = models.DecimalField(max_digits=10, decimal_places=2,
                                       help_text="for debit amount record for debit course")
    tran_type = models.ForeignKey(TransactionType, on_delete=models.CASCADE,
                                  help_text="refer transaction type i.e purchase ,sale etc.")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, help_text="refer particular user")
    Ebook = models.ForeignKey(Ebook, on_delete=models.CASCADE, help_text="for refer Ebook")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Certificate(models.Model):
    date = models.DateField()
    venu = models.CharField(max_length=100)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
