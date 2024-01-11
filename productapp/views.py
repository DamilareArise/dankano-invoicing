from django.shortcuts import render, get_object_or_404, redirect,HttpResponse
from .forms import *
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy, reverse
from django.http import HttpResponsePermanentRedirect
from .pdf import html2pdf




# Create your views here.

@login_required
def  displayInvoice(request): 
    invoices = Invoice.objects.all().exclude(payment_status = 'Credit').order_by('date_created').reverse()

    return render (request, 'productapp/display_invoices.html', {'invoices':invoices})

@login_required
def  displayDebitInvoice(request): 
    invoices = Invoice.objects.all().filter(payment_status = 'Credit').order_by('date_created').reverse()

    return render (request, 'productapp/debit_invoices.html', {'invoices':invoices})

@login_required
def createInvoice(request):
    number = 'INV-'+str(uuid4()).split('-')[1]
    newInvoice = Invoice.objects.create(number=number)
    newInvoice.save()

    inv = Invoice.objects.get(number=number)
    return redirect('create-build-invoice', inv_id=inv.invoice_id)

def createBuildInvoice(request, inv_id):
    #fetch that invoice
    try:
        invoice = Invoice.objects.get(invoice_id=inv_id)
        pass
    except:
        messages.error(request, 'Something went wrong')
        return redirect('invoices')

    #fetch all the products - related to this invoice
    products = Product.objects.filter(invoice=invoice)


    context = {}
    context['invoice'] = invoice
    context['products'] = products

    if request.method == 'GET':
        prod_form  = ProductForm()
        inv_form = InvoiceForm(instance=invoice)
        context['prod_form'] = prod_form
        context['inv_form'] = inv_form
        return render(request, 'productapp/create_invoice.html', context)

    if request.method == 'POST':
        prod_form  = ProductForm(request.POST)
        inv_form = InvoiceForm(request.POST, instance=invoice)
       
        if prod_form.is_valid():
            Qty = prod_form.cleaned_data['quantity']
            total_price = prod_form.cleaned_data['price_per_Qty']
            obj = prod_form.save(commit=False)
            obj.invoice = invoice 
            obj.total_price = total_price * Qty

            print(total_price)
            obj.save()

            messages.success(request, "Invoice product added succesfully")
            return redirect('create-build-invoice', inv_id=invoice.invoice_id)
        elif inv_form.is_valid:
            inv_form.save()

            messages.success(request, "Invoice updated succesfully")
            return redirect('create-build-invoice', inv_id=invoice.invoice_id)
        
        else:
            context['prod_form'] = prod_form
            context['inv_form'] = inv_form
            messages.error(request,"Problem processing your request")
            return render(request, 'productapp/create_invoice.html', context)


    return render(request, 'productapp/create_invoice.html', context)


@login_required
def editInvoice(request, inv_id):
    if inv_id is not None:
        # Editing an existing invoice
        invoice = get_object_or_404(Invoice, invoice_id=inv_id)
    else:
        # Creating a new invoice
        invoice = None

    if request.method == 'POST':
        if invoice:
            # Editing an existing invoice
            inv_form = InvoiceForm(request.POST, instance=invoice)
            if inv_form.is_valid():
                inv_form.save()
                messages.success(request, "Invoice updated successfully")
                return redirect('edit_invoice', inv_id)
            else:
                pass
                # messages.error(request, "Invoice form is not valid. Please check the data.")
                

            prod_form = ProductForm(request.POST)
            if prod_form.is_valid():
                Qty = prod_form.cleaned_data['quantity']
                total_price = prod_form.cleaned_data['price_per_Qty']
                product = prod_form.save(commit=False)
                product.invoice = invoice
                product.total_price = total_price * Qty
                product.save()
                messages.success(request, "Product added successfully")
                return redirect('edit_invoice', inv_id)
            else:
                messages.error(request, "Product form is not valid. Please check the data.")
        else:
            # Creating a new invoice
            inv_form = InvoiceForm(request.POST)
            if inv_form.is_valid():
                invoice = inv_form.save()
                messages.success(request, "Invoice created successfully")
                return redirect('display_invoices')
            else:
                messages.error(request, "Invoice form is not valid. Please check the data.")

            prod_form = ProductForm(request.POST)
            if prod_form.is_valid():
                product = prod_form.save(commit=False)
                product.invoice = invoice
               
                product.save()
                messages.success(request, "Product added successfully")
                return redirect('display_invoices')
            else:
                messages.error(request, "Product form is not valid. Please check the data.")
    else:
        if invoice:
            inv_form = InvoiceForm(instance=invoice)
        else:
            inv_form = InvoiceForm()

        prod_form = ProductForm()

    products = Product.objects.filter(invoice=invoice)

    context = {
        'invoice': invoice,
        'products': products,
        'inv_form': inv_form,
        'prod_form': prod_form,
    }

    return render(request, 'productapp/edit_invoice.html', context)


@login_required
def deleteInvoice(request, inv_id):
    try:
        Invoice.objects.get(invoice_id = inv_id).delete()
        messages.info(request, 'Invoice deleted successfully')
    except:
        messages.error(request, 'Something went wrong')
        return redirect('display_invoices')

    return redirect('display_invoices')
    

@login_required
def  displayProduct(request, inv_id): 
    
    products = Product.objects.all().filter(invoice_id = inv_id)
    total = sum([product.price for product in products])
    print(total)
    
    return render (request, 'productapp/display_products.html', {'products':products, 'total':total})


@login_required
def editProduct(request, prd_id, inv_id):
    item = get_object_or_404(Product, product_id = prd_id)
    if request.method == 'POST':
        product = ProductForm(request.POST, instance=item)
        if product.is_valid():
            product.save()

            messages.info(request, 'Item edited succesfully')
            return redirect('display_products', inv_id) 
        else:
            messages.error(request, 'Please correct the error below.')
            return HttpResponsePermanentRedirect(reverse('edit_product', args=(prd_id, inv_id))) 

    else:
        product = ProductForm()    
        return render(request, 'productapp/display_products.html', {'product': product})


@login_required
def deleteProduct(request, prd_id):
    product = Product.objects.get(product_id = prd_id)
    try:
        Product.objects.get(product_id = prd_id).delete()
        messages.info(request, 'Product deleted successfully')
    except:
        messages.error(request, 'Something went wrong')
        return redirect('edit_invoice', product.invoice.invoice_id)

    return redirect('edit_invoice',  product.invoice.invoice_id)

def salesHistory(request):
    products = Product.objects.all().order_by('date_created').reverse()
    len_item = len([item for item in products])
    total = sum([product.total_price for product in products])
    total = f'{total:,}'

    return render (request, 'productapp/saleshistory.html', {'products':products, 'len_item':len_item, 'total':total})


@login_required
def  viewReciept(request, inv_id): 
    invoice = Invoice.objects.get(invoice_id = inv_id)
    products = Product.objects.all().filter(invoice_id = inv_id)
    total = sum([product.total_price for product in products])

    pdf = html2pdf("productapp/reciept.html", {'products':products, 'total':total, 'invoice':invoice})

    return HttpResponse(pdf,content_type = "application/pdf")
    
    # return render (request, 'productapp/reciept.html', {'products':products, 'total':total, 'invoice':invoice})

@login_required
def  viewWaybill(request, inv_id): 
    invoice = Invoice.objects.get(invoice_id = inv_id)
    products = Product.objects.all().filter(invoice_id = inv_id)
    total = sum([product.total_price for product in products])
    print(total)
    pdf = html2pdf("productapp/waybill.html", {'products':products, 'total':total, 'invoice':invoice})

    return HttpResponse(pdf,content_type = "application/pdf")
    # return render (request, 'productapp/waybill.html', {'products':products, 'total':total, 'invoice':invoice})

