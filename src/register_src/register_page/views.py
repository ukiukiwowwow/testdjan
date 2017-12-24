from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import *


class LoginView(generic.ListView):
    model = Student
    template_name = 'register_page/login.html'
    context_object_name = 'my_list'
    def __init__(self):
        self.login_isSuccess=False
        self.register_isSuccess=False
        self.firsttime=True
        
    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['cookies'] = self.request.COOKIES.get("name")
        return context
        
    def post(self,request):
        if(request.method=="POST"):
            if("login" in request.POST):
                self.firsttime=False
                try:                    
                    s=Student.objects.get(name=request.POST["login_name"])
                    self.login_isSuccess=True
                except:
                    self.login_isSuccess=False
                try:                    
                    q=Student.objects.filter(password__password__contains=request.POST["login_password"])
                    for a in q:
                        print(a.name)
                        b=a.name
                except:
                    self.login_isSuccess=False
                if(self.login_isSuccess):
                    if(str(b)==str(s)):
                        self.login_isSuccess=True
                    else:
                        self.login_isSuccess=False
                if(self.login_isSuccess):
                    login=render(request,"register_page/login.html",{"login_isSuccess":self.login_isSuccess,"firsttime":self.firsttime,"cookie":request.POST["login_name"]})
                    login.set_cookie(key="name",value=request.POST["login_name"],max_age=24*60*60)
                    return login
                else:
                    return render(request,"register_page/login.html",{"login_isSuccess":self.login_isSuccess,"firsttime":self.firsttime,"login_or_register":True}) #login_or_register True:login error ,False:register                     
                
            elif("re" in request.POST):
                try:
                    s=Student.objects.get(name=request.POST["register_name"])
                    self.login_isSuccess=False
                    self.firsttime=False
                    
                    return render(request,"register_page/login.html",{"login_isSuccess":self.login_isSuccess,"firsttime":self.firsttime,"login_or_register":False})
                except:
                    stu=Student(name=request.POST["register_name"])
                    
                    pas=Password(password=request.POST["register_password"])
                    stu.save()
                    pas.student_number=Student.objects.get(name=request.POST["register_name"])
                    pas.save()
                    self.login_isSuccess=True
                    self.firsttime=True
                    login=render(request,"register_page/login.html",{"login_isSuccess":self.login_isSuccess,"firsttime":self.firsttime,"cookie":request.POST["register_name"]})
                    login.set_cookie(key="name",value=request.POST["register_name"],max_age=24*60*60)
                    return login
                return HttpResponse("<p>register_page</p>")
                
            elif("logout" in request.POST):
                self.login_isSuccess=False
                self.firsttime=True
                logout=render(request,"register_page/login.html",{"login_isSuccess":self.login_isSuccess,"firsttime":self.firsttime})
                logout.delete_cookie(key="name")
                return logout
