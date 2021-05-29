from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt
# Create your views here.

def logreg(request):
    return render(request, "log_reg.html")

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.filter(email=request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.hash_pw.encode()):
                request.session['userid'] = logged_user.id
                request.session['username'] = logged_user.first_name
                return redirect('/wishes')
        else:
            return redirect('/')

def reg(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            hash_pw = pw_hash,
        )
        user = User.objects.last()
        request.session['userid'] = user.id
        request.session['username'] = user.first_name
        return redirect('/wishes')

def logout(request):
    request.session.flush()
    return redirect('/')