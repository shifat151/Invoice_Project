from django import forms
from django.forms import fields
from . models import invoice

class invoiceForm(forms.Form):
    status_choices=[
        ('paid', 'paid'),
        ('unpaid', 'unpaid'),
        ('due', 'due')
    ]
    name=forms.CharField(label="Name:*",max_length=50)
    address=forms.CharField(label="Address:*",widget=forms.Textarea(attrs={'rows':'5'}))
    email=forms.EmailField(label="Email:*",max_length=100)
    start_date=forms.DateField(label="Start Date:*", widget=forms.DateInput(attrs={'autocomplete':'off','placeholder':'YYYY-MM-DD'}))
    end_date=forms.DateField(label="End Date:*", widget=forms.DateInput(attrs={'autocomplete':'off','placeholder':'YYYY-MM-DD'}))
    hours=forms.FloatField(label="Total working hour:*")
    salary_per_hour=forms.FloatField(label="Salary per hour:*")
    status=forms.ChoiceField(label="status:*",choices=status_choices)


# class editForm(forms.ModelForm):
#     class Meta:
#         model=invoice
#         exclude=['id', 'total_salary']
