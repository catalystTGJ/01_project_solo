from django.conf.urls import url
from django.db import models
from django.db.models.fields import TextField

class Word_Manager():
    pass

class Definition_Manager():
    pass

class Job_Manager():
    pass

class Li_Job_Manager():
    pass

class Li_Company_Manager():
    pass

class Li_Poster_Manager():
    pass

class Background_Task_Manager():
    pass

class Web_Scrape_Error_Manager():
    pass

# Create your models here.

class Word(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    word = models.CharField(max_length=255)
    status = models.IntegerField()
    objects = Word_Manager()
    @property
    def word_lower(self):
        return f"{self.word.lower()}"

class Definition(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    word = models.ForeignKey(Word, related_name="definitions", on_delete=models.DO_NOTHING)
    definition = models.TextField()
    source = models.CharField(max_length=255)
    source_url = models.CharField(max_length=255)
    objects = Definition_Manager()

class Job(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    status = models.IntegerField()
    objects = Job_Manager()

class Li_Poster(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    objects = Li_Poster_Manager()

class Li_Company(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    objects = Li_Company_Manager()

class Li_Job(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    data_id = models.CharField(max_length=64)
    data_search_id = models.CharField(max_length=64)
    title = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    details = TextField()
    criteria = TextField()
    job = models.ForeignKey(Job, related_name="Li_jobs", on_delete=models.DO_NOTHING)
    poster = models.ForeignKey(Li_Poster, related_name="Li_Jobs", on_delete=models.DO_NOTHING)
    company = models.ForeignKey(Li_Company, related_name="Li_Jobs", on_delete=models.DO_NOTHING)
    post_date = models.DateTimeField()
    status = models.IntegerField()
    objects = Li_Job_Manager()

class Background_Task(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    activity = models.CharField(max_length=255)
    status = models.IntegerField()
    url = models.CharField(max_length=255)
    current = models.IntegerField()
    total = models.IntegerField()
    objects = Background_Task_Manager()

class Web_Scrape_Error(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.IntegerField()
    count = models.IntegerField()
    url = models.CharField(max_length=255)
    objects = Web_Scrape_Error_Manager()

