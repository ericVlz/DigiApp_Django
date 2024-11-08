from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.core.paginator import Paginator

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .models import Documento, Tag
from .forms import DocumentoForm, SignUpForm, LoginForm

from .decorators import admin_required, login_required_directivo_or_admin


from PyPDF2 import PdfReader

import re

from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'




def extract_text_from_pdf(file):
    reader = PdfReader(file)
    content = ""
    for page in reader.pages:
        content += page.extract_text()
    return content

def clean_text(text):
    #new_text = re.sub(r'\b\w{1,2}\b', '', text)
    new_text = re.sub(r'\W+', ' ', text).strip()
    new_text = re.sub(r'\s+', ' ', new_text)
    return new_text

def user_groups(user):
    groups = []
    if user.is_authenticated:
        groups = list(user.groups.values_list('name', flat=True)) 
    return groups


#-----------------------------------------------------
#@user_passes_test(lambda u: u.groups.filter(name__in=['Administradores', 'Directivos']).exists(),login_url='/login/')

@login_required(login_url='/login/')
def home(request):

    return render(request, 'home.html', {'grupos_usuario':user_groups(request.user)})

#----- Usuario ----------------------------------------

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            #group = Group.objects.get(name='Operativo')
            #user.groups.add(group)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form, 'grupos_usuario':user_groups(request.user)})



def login_view(request):

    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user) 
            return redirect('home') 
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form, 'grupos_usuario':user_groups(request.user)})



def logout_view(request):
    logout(request)
    return redirect('login')

#===== END Usuario ====================================

#----- Documento --------------------------------------

@login_required_directivo_or_admin
def subir_documento(request):
    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES)
        
        """new_tag_name = form.data.get('new_tag')
        if new_tag_name:
            
            Tag.objects.get_or_create(nombre=new_tag_name)
            
            #return redirect(reverse('subir_documento'))

            #form = DocumentoForm(request.POST, request.FILES)
            #form = DocumentoForm(initial=request.POST.dict())
            #form.fields['new_tag'].initial = '' 

            form = DocumentoForm(request.POST, request.FILES)
            form.new_tag().clean()
            
        elif form.is_valid():"""

        if form.is_valid():

            documento = form.save(commit=False)
            archivo = request.FILES.get('archivo')
            
            
            if archivo.name.endswith('.pdf'):
                texto = extract_text_from_pdf(archivo)
                documento.contenido = clean_text(texto)
                
            elif archivo.name.endswith('.jpg') or archivo.name.endswith('.png'):
                img = Image.open(archivo)
                texto = pytesseract.image_to_string(img)
                documento.contenido = clean_text(texto)

            documento.save()
            
            documento.tags.set(form.cleaned_data['tags'])
            
            
            return redirect('lista_documentos')
    else:
        form = DocumentoForm()
    return render(request, 'subir_documento.html', {'form': form, 'grupos_usuario':user_groups(request.user)})


@login_required(login_url='/login/')
def lista_documentos(request):
    query = request.GET.get('q')
    tag_selected = request.GET.get('tag')

    documentos = Documento.objects.all().order_by('id')

    if tag_selected:
        documentos = documentos.filter(tags__id=tag_selected)

    if query:
        documentos = documentos.filter(Q(nombre__icontains=query) | Q(contenido__icontains=query) | Q(propietario__username__icontains=query))
    
    
    tags = Tag.objects.all()


    paginator = Paginator(documentos, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    return render(request, 'lista_documentos.html', {'documentos': documentos, 'tags':tags, 'page_obj': page_obj, 'grupos_usuario':user_groups(request.user)})



@login_required(login_url='/login/')
def editar_documento(request, documento_id):
    documento = get_object_or_404(Documento, id=documento_id)

    if request.method == 'POST':
        form = DocumentoForm(request.POST, request.FILES, instance=documento)
        
        if form.is_valid():
            form.save()

            return redirect('lista_documentos')
    else:
        form = DocumentoForm(instance=documento)

    return render(request, 'editar_documento.html',{'form': form, 'documento': documento, 'grupos_usuario':user_groups(request.user)})


@login_required(login_url='/login/')
def ver_documento(request, documento_id):
    documento = get_object_or_404(Documento, id=documento_id)
    return render(request, 'ver_documento.html', {'documento': documento, 'grupos_usuario':user_groups(request.user)})

#===== END Documento =====================================