from django.shortcuts import render, redirect, get_object_or_404
from . forms import invoiceForm
from . models import invoice
from django.forms.models import model_to_dict
from io import BytesIO
from django.http import HttpResponse, request, JsonResponse
from django.template.loader import get_template, render_to_string
from xhtml2pdf import pisa
import os, uuid
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.core.mail import EmailMessage

media_root = settings.MEDIA_ROOT
media_url=settings.MEDIA_URL


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

def render_to_pdf(template_src, context_dict={}):
    # template = get_template(template_src)
    # html  = template.render(context_dict)
    # result = BytesIO()
    # pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)#, link_callback=fetch_resources)

    html = render_to_string(template_src, context_dict)
    filename='invoice-'+str(uuid.uuid4())+'.pdf'
    pdf_file_path = os.path.join(media_root, filename)
    write_to_file = open(pdf_file_path, "w+b")
    pdf= pisa.CreatePDF(html, dest = write_to_file)
    write_to_file.close()

    if not pdf.err:
        return(filename)
        # return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def generate_pdf(request, pk):
    context={}
    invoice1=get_object_or_404(invoice,pk=pk)
    if request.method== 'POST':
        ajax_mess={}
        subject="Salary Invoice"
        receiver_email=invoice1.email
        message="Your salary invoice"

        if request.session['filename']:
            pdf_file_path = os.path.join(media_root, request.session['filename'])
            try:
                mail=EmailMessage(subject=subject,body= message,to=[receiver_email,])
                mail.attach_file( path=pdf_file_path, mimetype='application/pdf')
                mail.send()
                ajax_mess['success']="Mail sent successfully"
            except:
                ajax_mess['danger']="Mail sending failed"
                return JsonResponse({'ajax_mess': ajax_mess}, status=400)
            return JsonResponse({'ajax_mess': ajax_mess}, status=200)

        else:
            ajax_mess['danger']="Something went wrong! Please reload the page."
            return JsonResponse({'ajax_mess': ajax_mess}, status=400)
        
        

    else:
        data = model_to_dict(invoice1)
        filename = render_to_pdf('InvoiceApp/pdf_invoice.html', data)
        request.session['filename']=filename
        # print(filename)
        saved_file_path = os.path.join(media_url, filename)
        context['pdf_url']=saved_file_path
        # return HttpResponse(pdf, content_type='application/pdf')
        return render(request,'InvoiceApp/show_pdf.html',context)

    


