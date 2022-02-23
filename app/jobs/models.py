from django.db import models


class Job(models.Model):
    company_name = models.CharField(max_length=122)
    company_email = models.EmailField(blank=False)
    job_title = models.CharField(max_length=122)
    job_description = models.TextField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.CharField(max_length=122)
    state = models.CharField(max_length=122)
    created_at = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.job_title} @ {self.company_name}"
