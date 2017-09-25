from django.shortcuts import render,redirect,HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.messages import *

import bcrypt

def index(request):
    if 'user_id' not in request.session:
        return render(request,"LoginReg/index.html")
    else:
        request.session['user_id']=request.session['user_id']
        user_id=request.session['user_id']
        messages.add_message(request, INFO ,"Hello:",user_id)
        # return redirect('/success')
    print "index"
    return render(request,"LoginReg/index.html")

def register(request):
    errors = Users.objects.validChecker(request.POST)
    if len(errors)==0:
        for u in Users.objects.all():
            if u.email == request.POST['email']:
                messages.add_message(request, INFO ,"email already taken, try logging in")

                return redirect('/')
        user = Users.objects.create(first_name=request.POST["first_name"],last_name=request.POST["last_name"],email=request.POST["email"],password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
        request.session['user_id'] = user.id
        print request.session['user_id']
        # messages.add_message(request, INFO ,"success")
        return redirect('/success')
    else:
        for i in errors:
            messages.add_message(request, INFO , errors[i])
        return redirect('/')

def success(request):
    if 'user_id' not in request.session:
        messages.add_message(request, INFO ,"Please log in")
        return redirect('/')


    if 'user_id' in request.session:
        context = {
        "user":Users.objects.get(id=request.session['user_id']),
        "user_list":Users.objects.all(),
        }

        messages.add_message(request, INFO ,"Success")
        return render(request,"LoginReg/success.html", context)

def login(request):
    user_list = Users.objects.all()
    for u in user_list:
        if u.email == request.POST['email'] and bcrypt.checkpw(request.POST['password'].encode(),u.password.encode()):
            request.session['user_id'] = u.id
            return redirect('/success')
    messages.add_message(request, INFO, "Invalid password or email, or both")
    return redirect('/')
def delete(request, user_id):
    Users.objects.get(id=user_id).delete()

    return redirect('/success')

def clearsession(request):
    request.session.clear()
    messages.add_message(request, INFO ,"Logged out")
    return redirect('/')
