from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse,redirect
from django.contrib import messages
from models import *
import bcrypt

def index(request):
    if 'id' not in request.session:
        return render(request,'regis_app/index.html') 
    else:
        return redirect('/user')
def user(request):
    user = {'users': User.objects.filter(id=request.session['id'])}
    return render(request, 'regis_app/login.html', user)  
def register(request):
    if request.method == 'POST':
        errors = User.objects.regis_validator(request.POST)
        if len(errors):
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags=tag)
            return redirect('/')
        else:
            psw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'],email=request.POST['email'], password = psw)
            request.session['id'] = user.id
        return redirect('/user')
def login(request):
    if request.method == 'POST':
        user = User.objects.get(email = request.POST['user_email'])
        if bcrypt.checkpw(request.POST['psw'].encode(), user.password.encode()):
            request.session['id'] = user.id
            return redirect('/user')
        else:
            messages.warning(request, 'Email or password you entered is incorrect.')
            return redirect('/')
def logout(request):
    del request.session['id']
    return redirect('/')