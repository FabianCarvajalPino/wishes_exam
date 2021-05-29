from django.shortcuts import render, redirect
from . models import Wish
from ..login_reg_app.models import User
from django.contrib import messages
from datetime import date
from django.db.models import Count
# Create your views here.

def wishes(request):
    #cargar los deseos al context dirigido al html
    wishes = Wish.objects.all()
    user_selected = User.objects.get(id = request.session['userid'])

    wishes_user_selected = Wish.objects.filter(wisher = user_selected)
    '''
    wishes_user_selected_non = wishes_user_selected.exclude(granted = True)
    '''

    context = {
        'wishes_user_selected': wishes_user_selected,
        'wishes': wishes,
        'user_selected': user_selected
    }
    return render(request, 'wishes.html', context)

def new_wish(request):
    #si la solicitud es get, hacer render al html
    if request.method == 'GET':
        return render(request, 'new_wish.html')
    #si la solicitud es el post del form para agregar deseos
    else:
        #existen errores en el form?
        errors = Wish.objects.wish_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/wishes/new')
        #si no existe, agregar a bd
        else:
            wisher = User.objects.get(id = request.session['userid'])
            Wish.objects.create(
                wisher = wisher,
                wish = request.POST['wish'],
                description = request.POST['description'],
                granted = False
            )
            return redirect('/wishes')

def edit_wish(request, id_wish):
    #crear variable para la funcion
    
    #si la solicitud es get
    if request.method == 'GET': 
        wish = Wish.objects.get(id = int(id_wish))
        context = {
            'wish': wish
        }
        return render (request, 'edit.html', context)
    #si la solicitud es post
    else:
        #si hay errores en el form
        errors = Wish.objects.wish_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/wishes/edit/{id_wish}')
        #Si no hay errores, editar el deseo
        else:
            wish_to_update = Wish.objects.get(id = int(id_wish))
            #.update(wish=request.POST['wish'], description=request.POST['description'])

            wish_to_update.wish = request.POST['wish']
            wish_to_update.description = request.POST['description']
            wish_to_update.save()

            return redirect('/wishes')

def stats(request):
    #cargar los deseos y agregarlos al context del render
    wishes = Wish.objects.all()
    user_selected = User.objects.get(id = request.session['userid'])
    cumplidos = Wish.objects.filter(granted=True)
    cumplidos_user = cumplidos.filter(wisher=user_selected)
    no_cumplidos = Wish.objects.filter(granted=False)
    no_cumplidos_user = no_cumplidos.filter(wisher=user_selected)
    context = {
        'wishes': wishes,
        'user_selected': user_selected,
        'cumplidos': cumplidos,
        'cumplidos_user': cumplidos_user,
        'no_cumplidos_user': no_cumplidos_user
    }
    return render(request, 'stats.html', context)

def remove_wish(request, id_wish):
    wish_to_remove = Wish.objects.get(id = int(id_wish))
    wish_to_remove.delete()
    return redirect('/wishes')

def grant_wish(request, id_wish):
    wish_to_grant = Wish.objects.get(id = int(id_wish))
    wish_to_grant.granted = True
    wish_to_grant.date_granted = date.today()
    wish_to_grant.save()
    return redirect('/wishes')


def like_wish(request, id_wish):
    wish_to_like = Wish.objects.get(id=int(id_wish))
    user_like = User.objects.get(id=request.session['userid'])
    wish_to_like.likes.add(user_like)
    return redirect('/wishes')