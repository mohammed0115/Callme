from django.shortcuts import render,redirect
from call import data
import json
import phonenumbers
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
# Create your views here.
def _convert_mobile_number(mobile_number):
    if not mobile_number.startswith("+"):
        return "+"+mobile_number
    else:
        return mobile_number
def getElement():
    element=[]
    language={}
    for lan in data.langs:
        print(data.langs[lan]['name'])
        tom_index = next((index for (index, d) in enumerate(data.countries) if d["code"] == lan), None)
        if tom_index:
            language["name"]=data.langs[lan]['name']
            language["languages"]=data.langs[lan]['languages']
            language["dial_code"]=data.countries[tom_index]['dial_code']
            language["code"]=data.countries[tom_index]['code']
            print(language)
            element.append(language)
            language={}
        return element
def getSpecificEelement(lan):
    element=[]
    language={}
    tom_index = next((index for (index, d) in enumerate(data.countries) if d["dial_code"] == lan), None)
    lan=data.countries[tom_index]['code']
    if tom_index:
        print(data.langs[lan])
        language["name"]=data.langs[lan]['name']
        language["languages"]=data.langs[lan]['languages']
        language["dial_code"]=data.countries[tom_index]['dial_code']
        language["code"]=data.countries[tom_index]['code']
        print(language)
        element.append(language)
        language={}
        return element
    
def read_File():
    a_file = open("call/numbers.txt", "r")
    list_of_lists = [(line.strip()).split() for line in a_file]
    a_file.close()
    return list_of_lists
@csrf_exempt
def login(request):
    if request.method=="GET":
       
                # print(element)      
                
        context={
            "phone":read_File(),
            # "lans":element
        }
        return render(request,"callme.html",context)
    else:
        phone=request.POST['phone']
        
        
        return redirect(reverse('select-phone', kwargs={'phone':_convert_mobile_number(phone)}))
        # return redirect('seleect/phone/')
 
@csrf_exempt
def selected(request,phone):
    if request.method=="POST":
        country_code=phonenumbers.parse(phone)
        country_inf=getSpecificEelement("+"+str(country_code.country_code))
        context={
            "coountry_inf":country_inf,
            "phone":phone,
            "code_call":str(country_inf[0]['languages'][0]).lower()+"-"+str(country_inf[0]['code']).lower()
        }
        print("POS ok")
        return redirect("https://support.microsoft.com/"+context['code_call']+"/contact/callback/6/?fbclid=IwAR2J2PdfGy4W-p6YckCM9NkP99qOp8xrwnrMX0XxsFZ4ozWxf45waq-E_n4&returnFromSignIn=true&OSMCSignIn=true&wa=wsignin1.0")
    else:
        # phone=request.POST['phone']
        country_code=phonenumbers.parse(phone)
        country_inf=getSpecificEelement("+"+str(country_code.country_code))
        context={
            "coountry_inf":country_inf,
            "phone":phone,
            "code_call":str(country_inf[0]['languages'][0]).lower()+"-"+str(country_inf[0]['code']).lower()
        }
        return render(request,"select.html",context)
        