from django.shortcuts import render, redirect, get_object_or_404
from . forms import invoiceForm
from . models import invoice
from django.forms.models import model_to_dict


# Create your views here.
def home(request):
    context={'home':'active'}
    invoices=invoice.objects.all()
    context['invoices']=invoices
    return render(request, 'InvoiceApp/home.html', context)

def create_invoice(request):
    context={'create':'active'}
    if request.method=='POST':
        form=invoiceForm(request.POST)
        if form.is_valid():
            name=form.cleaned_data['name']
            address=form.cleaned_data['address']
            email=form.cleaned_data['email']
            start_date=form.cleaned_data['start_date']
            end_date=form.cleaned_data['end_date']
            hours=form.cleaned_data['hours']
            salary_per_hour=form.cleaned_data['salary_per_hour']
            status=form.cleaned_data['status']
            invoice.objects.create(name=name, address=address, email=email, start_date=start_date,
             end_date=end_date, hours=hours, salary_per_hour=salary_per_hour,status=status)
            form=invoiceForm()
            context['form']=form
            context['msg']='Successfully saved the data'
            return render(request,'InvoiceApp/create_invoice.html', context)
        else:
            context['form']=form
            return render(request,'InvoiceApp/create_invoice.html', context)

    form=invoiceForm()
    context['form']=form
    return render(request,'InvoiceApp/create_invoice.html', context)


def details_invoice(request, pk):
    context={}
    invoice1=get_object_or_404(invoice,pk=pk )
    if request.method=='POST':
        form=invoiceForm(request.POST, initial=model_to_dict(invoice1))
        if form.is_valid():
            if form.has_changed():
                for field in form.changed_data:
                    setattr(invoice1, field, form.cleaned_data[field])
                    invoice1.save()
                invoice1.refresh_from_db()
                context['msg']='Successfully updated.'
                form = invoiceForm(initial=model_to_dict(invoice1))
                context['form']=form
                return render(request,'InvoiceApp/edit_invoice.html', context)
            else:
                context['msg']='Please edit any field to make an update.'
                context['form']=form
                return render(request,'InvoiceApp/edit_invoice.html', context)

        else:
            context['form']=form
            return render(request,'InvoiceApp/edit_invoice.html', context)

    form = invoiceForm(initial=model_to_dict(invoice1))
    context['form']=form
    return render(request,'InvoiceApp/edit_invoice.html', context)

def delete_invoice(request, pk):
    invoice1=get_object_or_404(invoice,pk=pk)
    invoice1.delete()
    return redirect('home')

