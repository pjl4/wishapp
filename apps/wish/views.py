from django.shortcuts import render,redirect
from apps.wish.models import *
from django.contrib import messages
import bcrypt
# Create your views here.
def index(req):
    return render(req,'wish/index.html')

def login(req):
    valid,result=User.objects.validate_login(req.POST)
    if not valid:
        messages.error(req,result)
        return redirect(f'/')
    else:
        user=User.objects.get(email=req.POST['email'])
        req.session['name']=user.first_name
        req.session['id']=user.id
        return redirect(f'/wishes/')

def register(req):
    errors=User.objects.validateData(req.POST)
    if errors:
        for key,value in errors.items():
            messages.error(req,value)
        return redirect(f'/')
    else:
        pw_hash=bcrypt.hashpw(req.POST['password'].encode(),bcrypt.gensalt())
        user=User.objects.create(first_name=req.POST['first_name'],last_name=req.POST['last_name'],email=req.POST['email'],pw_hash=pw_hash)
        req.session['name']=user.first_name
        req.session['id']=user.id
        return redirect(f'/wishes/')
def wishes(req):
    if 'id' not in req.session:
        return redirect(f'/')
    try:
        context={
            'wishes': Wish.objects.filter(createdby=req.session['id']),
            'granted': Wish.objects.filter(granted=True),
        }
    except Wish.DoesNotExist:
        return render(req,'wish/wishes.html')
    return render(req,'wish/wishes.html',context)
def new(req):
    if 'id' not in req.session:
        return redirect(f'/')

    return render(req,'wish/new.html')
def create(req):
    errors=Wish.objects.validateWish(req.POST)
    if errors:
        for key,value in errors.items():
            messages.error(req,value)
        return redirect(f'/wishes/new/')
    else:
        user= User.objects.get(id=req.session['id'])
        Wish.objects.create(item=req.POST['item'],desc=req.POST['desc'],createdby=user)

        return redirect(f'/wishes/')
def logout(req):
    req.session.clear()
    return redirect(f'/')
def edit(req,id):
    if 'id' not in req.session:
        return redirect(f'/')
    context={
        'wish':Wish.objects.get(id=id)
    }
    return render(req,'wish/edit.html',context)

def update(req,id):
    if 'id' not in req.session:
        return redirect(f'/')
    errors=Wish.objects.validateWish(req.POST)
    if errors:
        for key,value in errors.items():
            messages.error(req,value)
        return redirect(f'/wishes/{id}/edit/')
    else:
        user= User.objects.get(id=req.session['id'])
        wish= Wish.objects.get(id=id)
        wish.item=req.POST['item']
        wish.desc=req.POST['desc']
        wish.save()
    return redirect(f'/wishes/')

def remove(req,id):
    if 'id' not in req.session:
        return redirect(f'/')
    wish= Wish.objects.get(id=id)
    wish.delete()
    return redirect(f'/wishes/')
def granted(req,id):
    if 'id' not in req.session:
        return redirect(f'/')
    wish= Wish.objects.get(id=id)
    wish.granted=True
    wish.save()
    return redirect(f'/wishes/')

def stats(req):
    if 'id' not in req.session:
        return redirect(f'/')
    context={
            'wishes': Wish.objects.filter(createdby=req.session['id'], granted=False).count(),
            'granted': Wish.objects.filter(granted=True).count(),
            'userGranted':Wish.objects.filter(createdby=req.session['id'], granted=True).count()
        }
    return render(req,'wish/stats.html',context)

def like(req,id):
    if 'id' not in req.session:
        return redirect(f'/')
    user= User.objects.get(id=req.session['id'])
    wish= Wish.objects.get(id=id)
    user.liked.add(wish)
    return redirect(f'/wishes/')