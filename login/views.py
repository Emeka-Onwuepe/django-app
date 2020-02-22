from django.shortcuts import render, reverse
from django.http import Http404,HttpResponseRedirect
#from publishers.models import Section, Publisher, Article
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm,PasswordResetForm
from django.contrib.auth import login,logout
from django.conf import settings
# Create your views here.
def loginView(request):
    if request.user.is_authenticated:
            user= request.user
            return HttpResponseRedirect(reverse("publisher:publisherView",
            kwargs={"username":user.username}))
    if request.method=="POST":
        form= AuthenticationForm(data=request.POST)
        if form.is_valid():
            user=form.get_user()
            login(request,user)
            return HttpResponseRedirect(reverse("publisher:publisherView",
            kwargs={"username":user.username}))
    else:
        form=AuthenticationForm()
    return render(request,"login/login.html",{"form":form})

def logoutView(request):
    if request.method=="POST":
        logout(request)
    return HttpResponseRedirect(reverse('login:loginView'))


# def passwordResetView(request):
#         form=PasswordResetForm
#         if request.method=="POST":
#             form=PasswordResetForm(data=request.POST or None)
#             if form.is_valid():
#                 form.save(from_email=settings.EMAIL_HOST_USER, email_template_name='registration/password_reset_email.html', request=request)
#         return render(request,"login/passwordreset.html",{"form":form})
           