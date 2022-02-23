```
$ conda activate MyDjangoEnv
$ django-admin startproject app
$ cd app
$ python3 manage.py startapp jobs
$ python3 manage.py migrate
$ python3 manage.py makemigrations
$ python3 manage.py createsuperuser
$ python3 manage.py runserver
```
```py
# app/settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'jobs'
]
```
```py
# app/jobs/models.py
from django.db import models


class Job(models.Model):
    company_name = models.CharField(max_length=122)
    company_email = models.EmailField(blank=False)
    job_title = models.CharField(max_length=122)
    job_description = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.CharField(max_length=122)
    state = models.CharField(max_length=122)
    created_at = models.DateTimeField(auto_now=True))
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.job_title} @ {self.company_name}"
```
```
$ python3 manage.py makemigrations
$ python3 manage.py migrate 
```
```py
# app/jobs/amdin.py
from django.contrib import admin
from .models import Job

admin.site.register(Job)
```

## Seed Data
- within `app` create folder `management` and create a folder withing `management` called `commands`. Within `commands` create files `seed.py` and `__init__.py` and `data.py`

```py
# app/jobs/management/commands/data.py
job_data = [
    {
        "company_name": "Virtus Financial",
        "company_email": "virtus@gmail.com",
        "job_title": "Equity Analyst",
        "job_description": "Analyze Equities",
        "salary": 150000.00,
        "city": "Princeon",
        "state": "NJ",
        "available": True
    },
    {
        "company_name": "Princeton University",
        "company_email": "princeton@gmail.com",
        "job_title": "Janitor",
        "job_description": "Clean",
        "salary": 75000.00,
        "city": "Princeon",
        "state": "NJ",
        "available": True
    },
    {
        "company_name": "Activision",
        "company_email": "activision@gmail.com",
        "job_title": "Software Engineer",
        "job_description": "Create video games",
        "salary": 200000.00,
        "city": "New York",
        "state": "NY",
        "available": True
    },
]
```
```py
# app/jobs/management/commands/seed.py
from django.core.management.base import BaseCommand
from jobs.models import Job
from .data import job_data


class Command(BaseCommand):

    def handle(self, *args, **options):
        """ handle() function needed in BaseCommand class """
        self.stdout.write("Seeding Data")
        self.stdout.write("Deleting Data")
        delete_database()
        self.stdout.write("Creating Data")
        create_jobs()


def delete_database():
    Job.objects.all().delete()


def create_jobs(data=job_data):
    for job in data:
        new_job = Job.objects.create(**job)
        new_job.save()
        print(f"Creating {new_job.job_title} @ {new_job.company_name}")
```
```
$ python3 manage.py seed 
```
```
terminal:
############################################
Seeding Data
Deleting Data
Creating Data
Creating Equity Analyst @ Virtus Financial
Creating Janitor @ Princeton University
Creating Software Engineer @ Activision
#############################################
```
- Create `serliaziers.py` in `app/jobs`
```py
# app/jobs/serializers.py
from rest_framework import serializers
from .models import Job


class JobSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = '__all__'

```
go to `app/jobs/views`
```py
# app/jobs/views.py
from distutils import errors
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist

from .models import Job
from .serializers import JobSerializer


@api_view(['GET', 'POST'])
def job_list_view(request):
    if request.method == "GET":
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == "POST":
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, staus=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def article_detail_view(request, pk=None):
    try:
        job = Job.objects.get(pk=pk)
    except ObjectDoesNotExist:
        return Response({"error": "Job does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":
        serializer = JobSerializer(job)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = JobSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        job.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

```

- Create `urls.py` in `app/jobs`
```py
# app/jobs/urls.py
from django.urls import path
from .views import job_list_view

urlpatterns = [
    path('jobs/', job_list_view, name='job-list')
]
# reverse_url = reverse(jobs:job-list)
```
- Go to `app/app/urls.py`
```py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('jobs.urls'))
]
```

now go to `http://127.0.0.1:8000/api/jobs/` to view the job list view