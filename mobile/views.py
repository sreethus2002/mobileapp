from django.shortcuts import render,redirect
from mobile.forms import MobileForm,RegistrationForm,LoginForm
from django.views.generic import View
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.utils.decorators import method_decorator


from mobile.models import Mobiles


def signin_required(fn):
    def wrapper(request,*args,**kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"Invalid session")
            return redirect("sigin")
        else:
            return fn(request,*args,**kwargs)
    return wrapper 

@method_decorator(signin_required,name="dispatch")

class MobileListView(View):
    def get(self,request,*args,**kwargs):
        print(request.GET)#{brand:samsang}
        qs=Mobiles.objects.all()
        if "brand" in request.GET:
            brand=request.GET.get("brand")
            qs=qs.filter(brand_iexact=brand)
        if "display" in request.GET:
            display=request.GET.get("display")
            qs=qs.filter(display_iexact=display)
        if "price_lt" in request.GET:
            amount=request.GET.get("price_lt")
            qs=qs.filter(price_lte=amount)
        

        return render(request,"mobile_all.html",{"data":qs})
    

    #localhost:8000/Mobiles/{id}/
@method_decorator(signin_required,name="dispatch")
class MobileDetailsView(View):
    def get(self,request,*args,**kwargs):
        if request.user.is_authenticated:
           return redirect("signin")
        id=kwargs.get("pk")
        print(id)
        qs=Mobiles.objects.get(id=id)
        return render(request,'mobile_details.html',{'data':qs})
        
    

    #localhost:8000/mobiles/{pk:num}/remove
@method_decorator(signin_required,name="dispatch")

class MobileDeleteView(View):
    def get(self,request,*args,**kwargs):
        if not request.user.is_authenticated:
            return redirect("signin")

        id=kwargs.get("pk")
        Mobiles.objects.get(id=id).delete()
        messages.success(request,"mobile has been removed")

        return redirect("mobile-all")
    #localhost:8000/mobiles/add
    #get=> mobile_add.html form
    #post=> save from data

#class MobileCreateView(View):
   # def get(self,request,*args,**kwargs):
     #   return render(request,"mobile_add.html")
    
#    def post(self,request,*args,**kwargs):
#        print(request.POST)
#        Mobiles.objects.create(
#            name=request.POST.get("name"),
#            price=request.POST.get("price"),
#            brand=request.POST.get("brand"),
#            specs=request.POST.get("specs"),
#            display=request.POST.get("display")
#        )
#        return render(request,"mobile_add.html")

@method_decorator(signin_required,name="dispatch")

class MobileCreateView(View):
    def get(self,request,*args,**kwargs):
        form=MobileForm()
        return render(request,"mobile_add.html",{"form":form})
    def post(self,request,*args,**kwargs):
        form=MobileForm(request.POST,files=request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request,"mobile has been added")
            return redirect("mobile-all")
        else:
            messages.error(request,"failed to add mobile")
            return render(request,"mobile_add.html",{"form":form})
        
#localhost:8000/mobiles/{mobile_id}/change
#get
#post

@method_decorator(signin_required,name="dispatch")
class MobileUpdateView(View):
    def get(self,request,*args,**kwargs):
        id=kwargs.get("pk")
        obj=Mobiles.objects.get(id=id)
        form=MobileForm(instance=obj)


        return render(request,"mobile_edit.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        
        id=kwargs.get("pk")
        obj=Mobiles.objects.get(id=id)
        form=MobileForm(request.POST,instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request,"mobile details changed")
            return redirect("mobile-all")
        else:
            messages.error(request,"failed to chage mobile details")
            return render(request,"mobile_edit.html",{"form":form})
        

class SignUpView(View):

    def get(self,request,*args,**kwargs):
        form=RegistrationForm()
        return render(request,"register.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data)
            User.objects.create_user(**form.cleaned_data)
            messages.success(request,"account has been created")
            return render(request,"register.html",{"form":form})
        else:
            messages.error(request,"failed to create account")
            return render(request,"register.html",{"form":form})
        
@method_decorator(signin_required,name="dispatch")
class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,"login.html",{"form":form})
    
    def post(self,request,*args,**kwargs):
        form=LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            psword=form.cleaned_data.get("password")
            print("..",uname,psword)
            user_object=authenticate(request,username=uname,password=psword)
            if user_object:
                print ("valid credentails")
                login(request,user_object)
                print(request.user)
                return redirect("mobile-all")
            else:
                print("invalid credentials")
            return render(request,"login.html",{"form":form})
        else:
            return render(request,"login.html",{"form":form})
        
class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")

            

            

        

    

    

        
        


