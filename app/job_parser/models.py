from django.db import models

class Vacancy(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    vacancy_name = models.TextField()
    archived = models.BooleanField(null=True)
    area = models.CharField(max_length=255)
    information = models.TextField()
    min_salary = models.IntegerField(null=True, default=0)
    max_salary = models.IntegerField(null=True, default=2**31 -1)
    currency = models.CharField(null=True, default="RUR", max_length=5)
    schedule = models.CharField(max_length=255, null=True)
    professional_roles = models.TextField(null=True)
    employment = models.CharField(max_length=255, null=True)
    experience = models.CharField(max_length=255, null=True)
    published_at = models.DateTimeField()
    url = models.CharField(max_length=255)

    def __str__(self):
        return self.vacancy_name