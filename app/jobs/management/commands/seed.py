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
