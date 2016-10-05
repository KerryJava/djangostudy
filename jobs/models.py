#!/usr/bin/env python
#coding:utf-8
from django.db import models
from django.contrib import admin
import datetime

from django.forms import ModelForm, Textarea
from django.utils import timezone

# Create your models here.
TITLE_CHOICES = (
    ('MR', 'Mr.'),
    ('MRS', 'Mrs.'),
    ('MS', 'Ms.'),
)

class Person(models.Model):
	name = models.CharField(max_length=30)
	age = models.IntegerField()

	def __unicode__(self):
		return self.name

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Jet Published recently?'

    def __unicode__(self):
        return self.question_text

class Choice(models.Model):
    	question = models.ForeignKey(Question, on_delete=models.CASCADE)
    	choice_text = models.CharField(max_length=200)
    	votes = models.IntegerField(default=0)

	def __unicode__(self):
		return self.choice_text

class Author(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE,default=True)
    headImg = models.FileField(upload_to = './upload/', null=True)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=3, choices=TITLE_CHOICES)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Book(models.Model):
    name = models.CharField(max_length=100)
    authors = models.ManyToManyField(Author)

class AuthorForm(ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'title', 'birth_date']

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'authors']

# class AuthorForm(ModelForm):
#     class Meta:
#         model = Author
#         fields = ('name', 'title', 'birth_date')
#         widgets = {
#             'name': Textarea(attrs={'cols': 80, 'rows': 20}),
#         }

class BookAuthor(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    def __str__(self):              # __unicode__ on Python 2
        return self.name
class Picture(models.Model):
    DOG = 1
    CAT = 2
    ANIMAL_KIND_CHOICES = (
        (DOG, 'dog'),
        (CAT, 'cat'),
    )

    title = models.CharField(max_length=200)
    author = models.ForeignKey(BookAuthor, related_name='pictures')
    animal_kind = models.IntegerField(choices=ANIMAL_KIND_CHOICES)
    photo = models.ImageField(upload_to='animals')
    is_promoted = models.BooleanField(default=False)
    def __str__(self):              # __unicode__ on Python 2
        return self.title + " " + str(self.animal_kind)




class Comment(models.Model):
    author = models.ForeignKey(BookAuthor, related_name='comments')
    picture = models.ForeignKey(Picture, related_name='comments')
    comment = models.TextField()
    editors_note = models.TextField()
    def __str__(self):              # __unicode__ on Python 2
        return self.author.name + " " +  self.comment

admin.site.register(Person)
# admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Author)
