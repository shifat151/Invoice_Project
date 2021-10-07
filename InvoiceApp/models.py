from django.db import models
from django.urls import reverse

# Create your models here.

class invoice(models.Model):

    status_choices=[
        ('paid', 'paid'),
        ('unpaid', 'unpaid'),
        ('due', 'due')
    ]
    name=models.CharField(max_length=50)
    address=models.TextField(max_length=200)
    email=models.EmailField(max_length=100)
    start_date=models.DateField(auto_now=False, auto_now_add=False)
    end_date=models.DateField(auto_now=False, auto_now_add=False)
    hours=models.FloatField()
    salary_per_hour=models.FloatField()
    total_salary=models.FloatField()
    status=models.CharField(choices=status_choices, max_length=6)

    def save(self, *args, **kwargs):
        self.total_salary=round(self.salary_per_hour*self.hours, 2)
        super(invoice, self).save(*args, **kwargs)
    
    def __str__(self):
        return "{} ({}-{})".format(self.name, str(self.start_date), str(self.end_date))
    
    def get_absolute_url(self):
        return reverse('details_invoice', kwargs={'pk' : self.pk})

