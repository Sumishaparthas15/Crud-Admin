from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control,never_cache
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib import messages


# Create your views here.
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache
def loginpage(request):
    if 'username' in request.session:
        return redirect('home')
    else:
        if request.method=='POST':
            username=request.POST.get('username')
            password=request.POST.get('password')
            
            user=auth.authenticate(username=username,password=password)
            
            if user is not None:
                request.session['username'] = username
                login(request,user)
                return redirect('home')
            else:
                return HttpResponse("<h1>User name or password is not correct!!!!<h1>")
        else:
            return render(request,'login.html')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache       
def signup(request):
    if 'username' in request.session:
        return redirect('home')
    elif request.method=='POST':
        first_name=request.POST['firstname']
        last_name=request.POST['lastname']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirm=request.POST['confirmpassword']

        if not (first_name and last_name and username and  email and password and confirm):
                messages.info(request,"please fill required field")
                return render(request,'signup.html')
        elif password != confirm:
            messages.info(request,"Password Mismatch")
            return render(request,'signup.html')
        else: 
                if User.objects.filter(username = username).exists():
                    messages.info(request,"Username already taken")
                    return render(request,'signup.html')
                elif User.objects.filter(email = email).exists():
                    messages.info(request,"Email already taken")
                    return render (request,'signup.html')
                else:
                    my_user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
                    my_user.save()
                return redirect('login')  
    else:
        return render(request,'signup.html')



@login_required(login_url='login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache
def home(request):
    return render(request,'home.html')




@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@never_cache
def logout(request):
    if 'username' in request.session:
        del request.session['username']
        auth.logout(request)
        return redirect('login')
    

@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache
def crudadmin(request):
    if 'crudadmin' in request.session:
        return redirect('dashboard')
    else:
        if request.method=='POST':
            username = request.POST['username']
            password=request.POST['password']
            user=auth.authenticate(username=username,password=password)
            if user is not None and user.is_superuser:
                request.session['crudadmin']=username
                login(request,user)
                return redirect('dashboard')
            
    return render(request,'crudadmin.html')       

@login_required(login_url='crudadmin')
# @login_required(login_url='login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
@never_cache
def dashboard(request):
    if 'crudadmin' in request.session:
        users = User.objects.filter(is_staff= False)
        context = {
            'users': users,
        }
        return render(request, 'dashboard.html', context)
    return render('crudadmin')
    
    
def add(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')


        user = User.objects.create_user(
            username = name,
            email    = email,
            password = password,
            first_name=first_name,
            last_name=last_name,
            
        )
        
        return redirect('dashboard')
    
    return render(request,'dashboard.html')

def edit(request):
    des = des.objects.all()

    context = {
        'des' : des,

    }


    return redirect(request,'dashboard.html',context)

def update(request, id):
    
    user = User.objects.get(id=id)
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')
        user.username = name
        user.email = email
        user.first_name=first_name
        user.last_name=last_name
        if password:
            user.set_password(password)
        user.save()
        return redirect('dashboard')
    else:
        context = {
            'user': user
        }
        return render(request, 'dashboard.html', context)
    

def delete(request,id):
    des = User.objects.filter(id=id)
    des.delete()

    context ={
        'des':des,

    }
    
    return redirect( 'dashboard')

def search(request):
    query = request.GET.get('q')
    if query :
        results = User.objects.filter(username__icontains=query).exclude(username='admin')   
    else:
        results = []
    context = {
        'users': results,
        'query': query,
    }
    return render(request, 'dashboard.html', context)


@login_required(login_url='login')
@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def admin_logout(request):
    if 'crudadmin' in request.session:
        del request.session['crudadmin']
    auth.logout(request)
    return redirect('crudadmin')