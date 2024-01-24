from django.shortcuts import render

# Create your views here.


from app.forms import *
from app.models import *
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse,HttpResponseRedirect

def registration (request):
    ufo=UserForm()
    pfo=ProfileForm()
    d={'ufo':ufo,'pfo':pfo}

# Checking POST Method is active or Not.

    if request.method == 'POST' and request.FILES:
        ufd=UserForm(request.POST)
        pfd=ProfileForm(request.POST,request.FILES)


# To convert Non-Modified Function Data object into Modified Function Data object (2)
    #userform module
        if ufd.is_valid() and pfd.is_valid():
            MUFDO=ufd.save(commit=False)
            pw=ufd.cleaned_data['password']
            MUFDO.set_password(pw)
            MUFDO.save()

    #profile module
            MPFDO=pfd.save(commit=False)
            MPFDO.username=MUFDO
            MPFDO.save()

#-----------------------------------------------------------------------#

# Sending the Registration Mail to User (3)

            send_mail(
                #/Subject/
                'Registration',

                #/Message/
                'Hiii User You are Successfully Registered',

                #/From Email to Send a Mail to the User/
                'ramanikanthsasi@gmail.com',

                #/User Receipent Email/
                [MUFDO.email],

                #/fail_silently = True or False/
                #(True Means will the see the Exception otherwise False means We can't see the exception)
                fail_silently = False
                )

            return HttpResponse('Registration is Sucessfull')

        else:
            return HttpResponse('Invalid data')

#-----------------------------------------------------------------------#
      
    return render (request,'registration.html',d)

#-----------------------------------------------------------------------#
# Home Page

def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username' : username}
        return render(request,'home.html',d)

    return render (request,'home.html')


#-----------------------------------------------------------------------#
# Login



def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        AUO=authenticate(username=username,password=password)
        
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else :
            return HttpResponse('Invalid Credentials')
    
    return render(request,'user_login.html')


#-----------------------------------------------------------------------#
# Logout

@login_required
def user_logout (request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


#-----------------------------------------------------------------------#
# Display the User Details


@login_required
def profile_display (request):
    un=request.session.get('username')
    uo=User.objects.get(username=un)
    po=Profile.objects.get(username=uo)
    d={'uo':uo,'po':po}

    return render(request,'profile_display.html',d)
