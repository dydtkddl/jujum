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
    json_data = json.loads(request.body)
    for data in json_data:
      food = data["food"].replace("'","")
      food = Food.objects.get(name = food)
      count = data["count"]
      tableNumber = data["tableNo"]
      detail = data["detail"]
      isService = data["isService"]
      if isService =="on":
        isService = 1
      else:
        isService = 0
      print(food, count, tableNumber, detail, isService)
      order = Order.objects.create(food = food , count =count, tableNumber = tableNumber , detail = detail, isService = isService,receptionTime = datetime.datetime.now())
      order.save()
      if food not in ["콜라","생수","사이다"]:
        for i in range(int(count)):
          nth = i+1
          eachorder = EachOrder.objects.create(order=order, nth = nth)
          eachorder.save()
    
    return HttpResponse(1)

  return HttpResponse(1)
  
def register_serve_complete(request):
  if request.method == "POST":
    json_data = json.loads(request.body)
    id = json_data["orderID"]
    nth = json_data["nth"]
    order = Order.objects.get(id = id)
    eachorder = EachOrder.objects.get(nth = nth,order= order)
    print(eachorder)
    eachorder.servedTime = datetime.datetime.now()
    eachorder.save()
    print(order.count , len(EachOrder.objects.filter(order=order,servedTime__isnull = False)))
    print(type(order.count) , type(len(EachOrder.objects.filter(order=order,servedTime__isnull = False))))
    if (order.count == len(EachOrder.objects.filter(order=order,servedTime__isnull = False))):
      order.servedTime =  datetime.datetime.now()
      order.save()
  return HttpResponse(12)
def render_(request):
  return render(request, "app/1.html")

def get_not_served(request):
  unserved_orders = EachOrder.objects.filter(servedTime__isnull=True).exclude(order__food__in=['콜라','생수', '사이다']).order_by('order__receptionTime')
  lis = []
  for unserved_order in unserved_orders:
    dd = model_to_dict(unserved_order)
    dd["id"] = unserved_order.order.id
    dd["nth"] = unserved_order.nth
    dd["tableNumber"] = unserved_order.order.tableNumber
    dd["food"] = unserved_order.order.food.name
    dd["receptionTime"] = unserved_order.order.receptionTime
    lis.append(dd)
  return JsonResponse(lis, safe =False)
def get_served(request):
  served_orders = EachOrder.objects.filter(servedTime__isnull=False).exclude(order__food__in=['콜라','생수', '사이다']).order_by('order__receptionTime')
  lis = []
  for served_order in served_orders:
    dd = model_to_dict(served_order)
    dd["id"] = served_order.order.id
    dd["nth"] = served_order.nth
    dd["tableNumber"] = served_order.order.tableNumber
    dd["food"] = served_order.order.food.name
    dd["receptionTime"] = served_order.order.receptionTime
    lis.append(dd)
  return JsonResponse(lis, safe =False)

def reception_withdraw(request):
  if request.method == "POST":
    json_data = json.loads(request.body)
    id = json_data["orderID"]
    nth= json_data["nth"]
    order = Order.objects.get(id = id)
    eachorder= EachOrder.objects.get(order= order, nth = nth)
    print(order)
    eachorder.servedTime = None
    order.servedTime = None
    order.save()
    eachorder.save()
    
  return HttpResponse(12)
def deleteReception(request):
  if request.method == "POST":
    json_data = json.loads(request.body)
    id = json_data["orderID"]
    order = Order.objects.get(id = id)
    order.delete()  
  return HttpResponse(12)
def get_not_cook(request):
    
  uncooked_orders = EachOrder.objects.filter(isCooked = 0, cooker__isnull=True).exclude(order__food__in=['콜라','생수', '사이다']).exclude(order__servedTime__isnull=False).order_by('order__receptionTime')
  print(uncooked_orders)
  lis = []
  for uncooked_order in uncooked_orders:
    dd = model_to_dict(uncooked_order)
    dd["food"] = uncooked_order.order.food.name
    dd["count"] = uncooked_order.order.count
    dd["receptionTime"] = uncooked_order.order.receptionTime
    dd["detail"] = uncooked_order.order.detail
    dd["orderId"] = uncooked_order.order.id
    lis.append(dd)
  print(lis)
  return JsonResponse(lis, safe =False)
def cookOccupy(request):
  if request.method == "POST":
    json_data = json.loads(request.body)
    id = json_data["orderID"]
    nth= json_data["nth"]
    studentNumber = request.session.get("studentNumber")
    print(id,nth,studentNumber)
    order = Order.objects.get(id = id)
    cooker = Users.objects.get(studentNumber = studentNumber)
    eachorder = EachOrder.objects.get(order = order , nth = nth)
    eachorder.isCooked = 1
    eachorder.cooker = cooker
    eachorder.save()
  return HttpResponse(12)
def get_your_cook(request):
  studentNumber = request.session.get("studentNumber")
  you = Users.objects.get(studentNumber = studentNumber)
  uncooked_orders = EachOrder.objects.filter(cooker = you,isCooked = 1).exclude(order__servedTime__isnull=False).order_by('order__receptionTime')
  print(uncooked_orders)
  lis = []
  for uncooked_order in uncooked_orders:
    dd = model_to_dict(uncooked_order)
    dd["food"] = uncooked_order.order.food.name
    dd["count"] = uncooked_order.order.count
    dd["receptionTime"] = uncooked_order.order.receptionTime
    dd["detail"] = uncooked_order.order.detail
    dd["orderId"] = uncooked_order.order.id
    dd["is_delivery_call"] = uncooked_order.is_delivery_call
    if (uncooked_order.delivery_user!=None):
      dd["is_delivery_user"] = uncooked_order.delivery_user.name
    else:
      dd["is_delivery_user"] = 0
    lis.append(dd)
  print(lis)
  return JsonResponse(lis, safe =False)
def delivery_call(request):
  if request.method == "POST":
    json_data = json.loads(request.body)
    id = json_data["orderID"]
    nth= json_data["nth"]
    on_off = json_data["on_off"]
    studentNumber = request.session.get("studentNumber")
    print(id,nth,studentNumber)
    order = Order.objects.get(id = id)
    cooker = Users.objects.get(studentNumber = studentNumber)
    eachorder = EachOrder.objects.get(order = order , nth = nth)
    print(type(on_off))
    if on_off == "1":
      eachorder.is_delivery_call = 0
      eachorder.delivery_user = None
    else:
      eachorder.is_delivery_call = 1

    eachorder.save()
  return HttpResponse(12)
def get_delivery_call_list(request):
  delivery_calls = EachOrder.objects.filter(isCooked = 1, cooker__isnull=False, is_delivery_call = 1,delivery_user__isnull = True).exclude(order__servedTime__isnull=False).order_by('order__receptionTime')
  print(delivery_calls)
  lis = []
  for delivery_call in delivery_calls:
    dd = model_to_dict(delivery_call)
    dd["food"] = delivery_call.order.food.name
    dd["count"] = delivery_call.order.count
    dd["receptionTime"] = delivery_call.order.receptionTime
    dd["detail"] = delivery_call.order.detail
    dd["orderId"] = delivery_call.order.id
    lis.append(dd)
  print(lis)
  return JsonResponse(lis, safe =False)
def get_your_delivery(request):
  studentNumber = request.session.get("studentNumber")
  you = Users.objects.get(studentNumber = studentNumber)
  uncooked_orders = EachOrder.objects.filter(delivery_user = you,isCooked = 1).exclude(order__servedTime__isnull=False).order_by('order__receptionTime')
  print(uncooked_orders)
  lis = []
  for uncooked_order in uncooked_orders:
    dd = model_to_dict(uncooked_order)
    dd["food"] = uncooked_order.order.food.name
    dd["count"] = uncooked_order.order.count
    dd["receptionTime"] = uncooked_order.order.receptionTime
    dd["detail"] = uncooked_order.order.detail
    dd["orderId"] = uncooked_order.order.id
    dd["is_delivery_call"] = uncooked_order.is_delivery_call
    lis.append(dd)
  print(lis)
  return JsonResponse(lis, safe =False)
def delivery_occupy(request):
  if request.method == "POST":
    json_data = json.loads(request.body)
    id = json_data["orderID"]
    nth= json_data["nth"]
    studentNumber = request.session.get("studentNumber")
    print(id,nth,studentNumber)
    order = Order.objects.get(id = id)
    you = Users.objects.get(studentNumber = studentNumber)
    eachorder = EachOrder.objects.get(order = order , nth = nth)
    eachorder.delivery_user = you
    eachorder.save()
  return HttpResponse(12)
def delivery_withdraw(request):
  if request.method == "POST":
    json_data = json.loads(request.body)
    id = json_data["orderID"]
    nth= json_data["nth"]
    studentNumber = request.session.get("studentNumber")
    print(id,nth,studentNumber)
    order = Order.objects.get(id = id)
    you = Users.objects.get(studentNumber = studentNumber)
    eachorder = EachOrder.objects.get(order = order , nth = nth)
    eachorder.delivery_user = None
    eachorder.save()
  return HttpResponse(123)