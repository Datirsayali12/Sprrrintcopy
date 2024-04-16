# Generated by Django 5.0.2 on 2024-04-16 15:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('UIAsset', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_hrs', models.IntegerField(help_text='for course hours')),
                ('assignments_and_projects', models.IntegerField(help_text='for total number of assignment_and_projects')),
                ('quizzes', models.IntegerField(help_text='for number of quizzes')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Level',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='for level like advanced,begineers', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='for section name', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='for course name', max_length=255)),
                ('tag', models.CharField(help_text='for cours tag', max_length=255)),
                ('short_desc', models.TextField(help_text='for course short description')),
                ('course_lesson', models.IntegerField(help_text='for number of course lesson ')),
                ('long_desc', models.TextField(help_text='for course long description')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(help_text='for course category', on_delete=django.db.models.deletion.CASCADE, to='UIAsset.category')),
                ('content', models.ForeignKey(help_text='For content of course', on_delete=django.db.models.deletion.CASCADE, to='Learn.content')),
                ('creator', models.ForeignKey(help_text='for course creator', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('course_level', models.ForeignKey(help_text='for refer level like(begineers,advanced)', on_delete=django.db.models.deletion.CASCADE, to='Learn.level')),
            ],
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('venu', models.CharField(max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Learn.course')),
            ],
        ),
        migrations.CreateModel(
            name='CourseReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(help_text='for course review description', max_length=255)),
                ('rating', models.IntegerField(help_text='for course ratings')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(blank=True, help_text='refer to course', null=True, on_delete=django.db.models.deletion.CASCADE, to='Learn.course')),
                ('user', models.ForeignKey(help_text='refer to user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CourseTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit_amount', models.DecimalField(decimal_places=2, help_text='for credit amount for course', max_digits=10)),
                ('debit_amount', models.DecimalField(decimal_places=2, help_text='for debit amount record for debit transaction', max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(help_text='for refer course', on_delete=django.db.models.deletion.CASCADE, to='Learn.course')),
                ('tran_type', models.ForeignKey(help_text='refer transaction type i.e purchase ,sale etc.', on_delete=django.db.models.deletion.CASCADE, to='UIAsset.transactiontype')),
                ('user', models.ForeignKey(help_text='refer particular user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Ebook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('tag', models.CharField(max_length=100)),
                ('no_of_chapters', models.IntegerField(help_text='for number of chapters in Ebook')),
                ('no_of_pages', models.IntegerField(help_text='for number of pages in Ebook')),
                ('description', models.TextField(help_text='for Ebook description', max_length=255)),
                ('ebook_desc', models.TextField(help_text='ebook description', max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(help_text='For subcategory of Ebook', on_delete=django.db.models.deletion.CASCADE, to='UIAsset.category')),
                ('content', models.ForeignKey(help_text='For content of course', on_delete=django.db.models.deletion.CASCADE, to='Learn.content')),
                ('creator', models.ForeignKey(help_text='for creator of Ebook', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('level', models.ForeignKey(help_text='for refer level like(begineers,advanced)', on_delete=django.db.models.deletion.CASCADE, to='Learn.level')),
            ],
        ),
        migrations.CreateModel(
            name='EbookImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Ebook_url', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('Ebook', models.ForeignKey(help_text='for store Ebook images', on_delete=django.db.models.deletion.CASCADE, to='Learn.ebook')),
            ],
        ),
        migrations.CreateModel(
            name='EbookReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(help_text='for course review description', max_length=255)),
                ('rating', models.IntegerField(help_text='for course ratings')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ebook', models.ForeignKey(blank=True, help_text='for refer Ebook', null=True, on_delete=django.db.models.deletion.CASCADE, to='Learn.ebook')),
                ('user', models.ForeignKey(help_text='refer to user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EbookTransaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('credit_amount', models.DecimalField(decimal_places=2, help_text='for credit amount for course', max_digits=10)),
                ('debit_amount', models.DecimalField(decimal_places=2, help_text='for debit amount record for debit course', max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('Ebook', models.ForeignKey(help_text='for refer Ebook', on_delete=django.db.models.deletion.CASCADE, to='Learn.ebook')),
                ('tran_type', models.ForeignKey(help_text='refer transaction type i.e purchase ,sale etc.', on_delete=django.db.models.deletion.CASCADE, to='UIAsset.transactiontype')),
                ('user', models.ForeignKey(help_text='refer particular user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('questions', models.TextField()),
                ('question_image', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Learn.course')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Learn.section')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.TextField(help_text='for answer')),
                ('is_correct', models.BooleanField(help_text='ans is correct or not')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('question', models.ForeignKey(help_text='questions', on_delete=django.db.models.deletion.CASCADE, to='Learn.question')),
            ],
        ),
        migrations.CreateModel(
            name='Requirement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='requirment name', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('courses', models.ManyToManyField(help_text='refer to courses to which requirments are belongs', related_name='requirements', to='Learn.course')),
            ],
        ),
        migrations.CreateModel(
            name='SavedCourse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('course', models.ForeignKey(help_text='refer to course', on_delete=django.db.models.deletion.CASCADE, to='Learn.course')),
                ('user', models.ForeignKey(help_text='refer to user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SavedEbook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now=True)),
                ('ebook', models.ForeignKey(help_text='refer to course', on_delete=django.db.models.deletion.CASCADE, to='Learn.ebook')),
                ('user', models.ForeignKey(help_text='refer to user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CourseVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_video_url', models.URLField()),
                ('is_hero_video', models.BooleanField(help_text='is course video is on main card video')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_free', models.BooleanField(help_text='if video is free or not')),
                ('course', models.ForeignKey(help_text='refer to  course video is belongs', on_delete=django.db.models.deletion.CASCADE, to='Learn.course')),
                ('section', models.ForeignKey(help_text='for refer to which course section related', on_delete=django.db.models.deletion.CASCADE, to='Learn.section')),
            ],
        ),
        migrations.CreateModel(
            name='UserWallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, default=0.0, help_text='for user balance in wallet', max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(help_text='for refer user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='for video title', max_length=255)),
                ('tag', models.CharField(help_text='for video title', max_length=255)),
                ('hero_video_url', models.URLField()),
                ('overview', models.TextField(help_text='for video overview')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('category', models.ForeignKey(help_text='for category', on_delete=django.db.models.deletion.CASCADE, to='UIAsset.category')),
                ('creator', models.ForeignKey(help_text='for video creator', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Share',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_shared', models.BooleanField(help_text='is_shared or not')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(help_text='for refer particular user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(help_text='for refer video', on_delete=django.db.models.deletion.CASCADE, to='Learn.video')),
            ],
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.URLField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('video', models.ForeignKey(help_text='refer to particular video', on_delete=django.db.models.deletion.CASCADE, to='Learn.video')),
            ],
        ),
        migrations.CreateModel(
            name='LikesDislikesCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('likes', models.IntegerField(default=0, help_text='to store total likes of particular video')),
                ('dislikes', models.IntegerField(default=0, help_text='to store total dislikes of particular video')),
                ('shares', models.IntegerField(default=0, help_text='to store total shares of particular video')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('video', models.ForeignKey(help_text='for refer video table', on_delete=django.db.models.deletion.CASCADE, to='Learn.video')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_liked', models.BooleanField(help_text='is_liked or not')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(help_text='for refer user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(help_text='for refer particular video', on_delete=django.db.models.deletion.CASCADE, to='Learn.video')),
            ],
        ),
        migrations.CreateModel(
            name='Dislike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_disliked', models.BooleanField(help_text='is_disliked or not')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(help_text='for refer particular user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(help_text='for refer video', on_delete=django.db.models.deletion.CASCADE, to='Learn.video')),
            ],
        ),
        migrations.CreateModel(
            name='WatchedVideo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_completed', models.BooleanField(default=False, help_text='is course completed or not (True and False)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(help_text='refer to particular user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('video', models.ForeignKey(help_text='refer to courseVideo', on_delete=django.db.models.deletion.CASCADE, to='Learn.coursevideo')),
            ],
        ),
    ]
