from django.shortcuts import render,redirect
from django.http import JsonResponse , HttpResponse
# Create your views here.
from .others import read_student_info
from .models import *
import json
import datetime
from django.forms import model_to_dict
def is_octet(dic):
  gets = Users.objects.filter(name = dic["name"], phoneNumber = dic["phoneNumber"], studentNumber = dic["studentNumber"])
  print(gets)
  if len(gets)==1:
    return True 
  else:
    return False
def is_octet2(dic):
  gets = Users.objects.filter(name = dic["name"], studentNumber = dic["studentNumber"])
  print(gets)
  if len(gets)==1:
    return True 
  else:
    return False
  
def home(request):
  if request.method == "POST":
    name = request.POST.get('name')
    student_number = request.POST.get('studentNumber')
    phone_number = request.POST.get('phoneNumber')
    print(name, student_number , phone_number)
    if not name or not student_number or not phone_number:
      return render(request, 'app/home.html', {'text': '모든 필드를 입력하세요.'})
    dic = {"name":name, "studentNumber":student_number, "phoneNumber":phone_number}
    if (is_octet(dic)):
      data = Users.objects.get(name =name, phoneNumber = phone_number , studentNumber = student_number)
      if data.isSignUp ==0:
        return render(request, "app/home.html", context = {"text" : "직원 등록 먼저 부탁"})
      elif data.isSignUp == 1:
        request.session['name'] = name
        request.session['studentNumber'] = student_number
        return redirect("/main")
    return render(request, "app/home.html", context = {"text" : "옥텟이 아닙니다"})
  
  elif request.method == "GET":
    name = request.session.get('name')
    studentNumber= request.session.get("studentNumber")
    if (is_octet2({"name":name, "studentNumber":studentNumber})):
      print(name , studentNumber, "입장")
      return redirect("/main")
    else:
      return render(request, "app/home.html")
def signup(request):
  if request.method == "POST":
    name = request.POST.get('name')
    student_number = request.POST.get('studentNumber')
    phone_number = request.POST.get('phoneNumber')
    print(name, student_number , phone_number)
    if not name or not student_number or not phone_number:
      return render(request, 'app/signup.html', {'text': '모든 필드를 입력하세요.'})
    dic = {"name":name, "studentNumber":student_number, "phoneNumber":phone_number}
    if (is_octet(dic)):
      data = Users.objects.get(name =name, phoneNumber = phone_number , studentNumber = student_number)
      if data.isSignUp ==0:
        return render(request, "app/signup.html", context = {"text" : "200", "name":name, "studentNumber":student_number, "phoneNumber":phone_number})
      elif data.isSignUp == 1:
        return render(request, "app/signup.html", context = {"text" : "직원등록이 이미 되어있습니다."})
    return render(request, "app/signup.html", context = {"text" : "옥텟이 아니라서 직원 등록 불가"})
  else:
    return render(request, "app/signup.html")
def main(request):
  name = request.session.get('name')
  studentNumber= request.session.get("studentNumber")
  is_change = request.GET.get("ischange")
  if (is_octet2({"name":name, "studentNumber":studentNumber})):
    print(name , studentNumber, "입장")
    student = Users.objects.get(name = name, studentNumber = studentNumber)
    if student.role == None or (is_change=="true"):
      return render(request, "app/select_role.html")
    else:
      return render(request, "app/%s.html"%student.role)
  else:
    return redirect("/home")

def signout(request):
  a = request.session.pop('name', None)
  request.session.pop('studentNumber', None)
  print(a + "zzz")
  return HttpResponse(1)
def register(request):
  if (request.method == "POST"):
    json_data = json.loads(request.body)
    a = Users.objects.filter(name =json_data["name"], studentNumber = json_data["studentNumber"], phoneNumber = json_data["phoneNumber"])
    if (len(a)!=0):
      a[0].isSignUp =1
      a[0].save()
    return HttpResponse("200")
def rerole(request):
  if request.method == "POST":
    json_data = json.loads(request.body)
    print(json_data["role"])
    name = request.session.get('name')
    studentNumber= request.session.get("studentNumber")
    student = Users.objects.get(name = name, studentNumber = studentNumber)
    student.role = json_data["role"]
    student.save()
  return HttpResponse(1)

def register_order(request):
  if request.method == "POST":
    json_data = json.loads()
    food = json_data["food"]
    count = json_data["count"]
    tableNumber = json_data["tableNumber"]
    detail = json_data["detail"]
    isService = json_data["isService"]
    order = Order.objects.create(food = food , count =count, tableNumber = tableNumber , detail = detail, isService = isService,receptionTime = datetime.datetime.now())
    order.save()
    return HttpResponse(1)

  return HttpResponse(1)
  
def register_serve_complete(request):
  if request.method == "POST":
    json_data = json.loads()
    id = json_data["id"]
    food = json_data["food"]
    count = json_data["count"]
    order = Order.objects.get(id = id, name = food, count = count)
    order.servedTime = datetime.datetime.now()
    ##
    order.save()
    
  return HttpResponse(12)
def render_(request):
  return render(request, "app/1.html")

def get_not_served(request):
  unserved_orders = Order.objects.filter(servedTime__isnull=True)
  lis = []
  for unserved_order in unserved_orders:
    lis.append(model_to_dict(unserved_order))
  return JsonResponse(lis, safe =False)
