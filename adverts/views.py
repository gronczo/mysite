from django.template import *
from django.shortcuts import *
from adverts.models import *
from adverts.forms import *
from adverts.helpers import *
from django.contrib.auth import authenticate, login, logout


from reportlab.platypus import *
from reportlab.lib import *
from reportlab.pdfgen import *
from reportlab.lib import *
from reportlab.lib.pagesizes import *
from reportlab.pdfbase import *
from reportlab.pdfbase.ttfonts import *
from reportlab.lib.styles import *

from django.http import *
from django.conf import settings


import datetime


def new_user(request): # dodaj uzytkownika
    return render_to_response('new_user.html', {'user_form': UserForm()}, context_instance=RequestContext(request))

def new_advert(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("../login_user/")
    elif not request.user.has_perms('add_advert'):
        return HttpResponse("Nie masz uprawnien do dodawania ogloszen")

    if request.method == 'GET':
        return render_to_response('new_advert.html',{'advertiesment_form': AdvertForm(), 'attachment_form': AttachmentForm()}, context_instance=RequestContext(request))

    if request.method == 'POST':
        form = AdvertForm(request.POST, request.FILES)
        if form.is_valid():
            advert = Advert()
            advert.user = request.user
            subactegories = Subcategory.objects.filter(id=request.POST['subcategory'])
            advert.subcategory = subactegories[0]
            advert.title = request.POST['title']
            advert.description = request.POST['description']
            advert.price = request.POST['price']
            advert.city = request.POST['city']
            advert.contact = request.POST['contact']
            advert.save()

            if 'file' in request.FILES:
                file = request.FILES['file']
                attachment = Attachment()
                attachment.user = request.user
                attachment.advert = advert
                attachment.name = file.name
                attachment.extension = file.name[-3:]
                attachment.size = file.size
                attachment.file = file
                attachment.save()
                collect_static()

            return HttpResponseRedirect("../show_advert/" + str(advert.id))
        else:
            return HttpResponse("Blednie wypelniony formularz.")

    return HttpResponse("Blad")

def new_category(request): # dodaj kategorie
    if not request.user.is_authenticated():
        return HttpResponse("musisz sie zalogowac")

    if request.method == 'GET':
        return render_to_response('new_category.html', {'category_form': CategoryForm()}, context_instance=RequestContext(request))

    if request.method == 'POST':
        category =  Category()
        category.title = request.POST['title']
        category.description = request.POST['description']
        category.save()

        return HttpResponse("Rekord zostal dodany")


def new_subcategory(request): # dodaj podkategorie
    if request.method == 'GET':
        return render_to_response('new_subcategory.html', {'subcategory_form': SubcategoryForm()}, context_instance=RequestContext(request))

    if request.method == 'POST':
        subcategory =  Subcategory()
        categories = Category.objects.filter(id=request.POST['category'])
        subcategory.category = categories[0]
        subcategory.title = request.POST['title']
        subcategory.description = request.POST['description']
        subcategory.save()

    return HttpResponse("Rekord zostal dodany")

def show_adverts(request):
    adverts = Advert.objects.all()
    return render_to_response('show_adverts.html',{'adverts': adverts,}, context_instance=RequestContext(request))

def show_advert(request, advert_id):
    if request.method == 'GET':
        advert = Advert.objects.get(id = advert_id)
        attachment = Attachment.objects.filter(advert = advert)
        comments = Comment.objects.filter(advert = advert)
        if attachment.count() > 0:
            return render_to_response('show_advert.html', {'advert': advert, 'attachment': attachment[0], 'comments': comments,}, context_instance=RequestContext(request))
        else:
            return render_to_response('show_advert.html', {'advert': advert, 'comments': comments,}, context_instance=RequestContext(request))
    if request.method == 'POST':
        if not request.user.is_authenticated():
            return HttpResponseRedirect("../login_user/")
        else:
            advert_id = request.POST['advert_id']
            content = request.POST['content']
            comment = Comment()
            comment.user = request.user
            comment.advert = Advert.objects.get(id = advert_id)
            comment.content = content
            comment.save()
            return HttpResponseRedirect('../show_advert/' + str(advert_id))


def show_category(request): # wtswietl kategorie
    return render_to_response('show_category.html', {'categories': Category.objects.all()}, context_instance=RequestContext(request))

def show_subcategory(request):
    return render_to_response('show_subcategory.html', {'subcategories': Subcategory.objects.all()}, context_instance=RequestContext(request))

def login_user(request):
    if request.method ==  'GET':
        return render_to_response('login_user.html', {'login_form': LoginForm()}, context_instance=RequestContext(request))

    if request.method == 'POST':
        # autentykacja uzytkownika
        user = authenticate(username = request.POST['username'], password = request.POST['password'])
        if user is not None: # jezeli taki istnieje to zaloguj
            login(request, user)
            request.session['user_id'] = user.id
            return HttpResponseRedirect('../show_advert/')
        else:
            return HttpResponse('Podales nieprawny login lub haslo')

    return HttpResponse('Blad podczas logowania')

    #if request.session.get('login', True):
    #    del request.session['login']
    #    return HttpResponse('zalogowany')
    #else:
    #    request.session['login'] = True
    #    return HttpResponse("Nie jestes zalogowany222.")

def logout_user(request):
    if request.user.is_authenticated():
        logout(request)

    return render_to_response('logout_user.html', context_instance=RequestContext(request))


def registration(request):
    if request.method == 'GET':
        return render_to_response('registration.html', {'registration_form': RegistrationForm()}, context_instance=RequestContext(request))

    if request.method == 'POST':
        user = User()
        user.username = request.POST['username']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        password = request.POST['password']
        user.set_password(password)
        user.is_staff = False
        user.is_active = True
        user.is_superuser = False
        user.save()
        return HttpResponseRedirect("../login_user/")


def edit_advert(request, advert_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("../login_user/")
    elif not request.user.has_perms('change_advert'):
        return HttpResponse("Nie masz uprawnien do edycji ogloszen")

    if request.method == 'GET':
        advert = Advert.objects.get(id = advert_id)
        return render_to_response('edit_advert.html', {'advert': advert}, context_instance=RequestContext(request))
    if request.method == "POST":
        advert = Advert.objects.get(id = advert_id)
        advert.title = request.POST['title']
        advert.description = request.POST['description']
        advert.price = request.POST['price']
        advert.city = request.POST['city']
        advert.contact = request.POST['contact']
        advert.save()
        return HttpResponseRedirect('../show_advert/' + advert_id)

def delete_advert(request, advert_id):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("../login_user/")
    elif not request.user.has_perms('delete_advert'):
        return HttpResponse("Nie masz uprawnien do usuwania ogloszen")

    advert = Advert.objects.get(id = advert_id)
    advert.delete()
    return render_to_response('delete_advert.html', context_instance=RequestContext(request))


def user(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("../login_user/")
    else:
        return render_to_response('user.html', {'user': request.user}, context_instance=RequestContext(request))

def my_advert(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("../login_user/")
    else:
        adverts = Advert.objects.filter(user = request.user)
        return render_to_response('my_advert.html', {'adverts': adverts}, context_instance=RequestContext(request))



def search(request):
    if request.method == 'POST':
        _search = request.POST['search']
        _where = _search
        adverts = Advert.objects.filter(title = _where)
        return render_to_response('search.html', {'adverts': adverts}, context_instance=RequestContext(request))

    return HttpResponseRedirect('../show_advert/')


def generate_pdf(request, advert_id):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(mimetype='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=advert.pdf'

    advert = Advert.objects.get(id=advert_id)


    # Create the PDF object, using the response object as its "file."
    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    pdfmetrics.registerFont(TTFont('Vera', settings.STATIC_ROOT +  '/Vera.ttf'))

    p.setFont("Vera", 30)
    p.drawString(50, (height - 100), "W Y D R U K   O G L O S Z E N I A")

    p.setFont("Vera", 22)

    p.drawString(50, (height - 260), "kategoria: " + advert.subcategory.title)
    p.drawString(50, (height - 320), "tytul: " +  advert.title)
    p.drawString(50, (height - 380), "opis: " + advert.description)
    p.drawString(50, (height - 440), "cena: " + str(advert.price))
    p.drawString(50, (height - 500), "miasto: " + advert.city)
    p.drawString(50, (height - 560),  "kontakt: " + advert.contact)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()
    return response