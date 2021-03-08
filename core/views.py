from django.shortcuts import render,redirect
from .models import agent
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import passenger_form,train_form,chart_form
from django.forms import  modelformset_factory,formset_factory
import datetime
from django.http import HttpResponse
from datetime import date
from django.contrib.auth.models import User


# Create your views here.
@login_required(login_url='/login')
def admin_view(request):
    print(request.user)
    if request.user.is_superuser == False:
        return redirect("/")
    agents=agent.objects.all()
    return render(request,'admin_page.html',{'agents':agents})

@login_required(login_url='/login')
def delete_agent(request,id):
    if request.user.is_superuser == False:
        return redirect("/")
    agents=agent.objects.get(id=id)
    agents.delete()
    return redirect("/admin-page")

@login_required(login_url='/login')
def add_train(request):
    if request.user.is_superuser == False:
        return redirect("/")
    form=train_form(request.POST or None)
    if request.method=="POST":
        if form.is_valid():
            form.save()
            return redirect("/")
    return render(request,'add-train.html',{'form':form})

@login_required(login_url='/login')
def chart_list(request):
    if request.user.is_superuser == False:
        return redirect("/")
    form=chart_form(request.POST or None)
    if request.method=="POST":
        if form.is_valid():
            train=form.cleaned_data['train']
            compartment=form.cleaned_data['compartment_capacity']
            date=form.cleaned_data['date']
            seat=compartment*6
            obj=train_charts.objects.create(train=train,compartment_capacity=compartment,date=date,seats=seat)
            obj.save()
            return redirect("/")
    return render(request,'add-chart.html',{'form':form})

@login_required(login_url='/login')
def home(request):

    agents=agent.objects.all()
    route=trains.objects.all()
    today = date.today()
    today=today.strftime("%Y-%m-%d")
    seat_bookings=booking_id.objects.filter(seat_booking__agent__user=request.user).order_by('-seat_booking__date')
    return render(request,'home_page.html',{'agents':agents,'route':route,'bookings':seat_bookings,'today':today})

@login_required(login_url='/login')
def booking_view(request):
    if request.method=="POST":
        depature=request.POST['depature']
        arrival=request.POST['arrival']
        date=request.POST.get('date')
        train =train_charts.objects.filter(train__depature=depature,train__arrival=arrival,date=date)
        route=trains.objects.all()
    return render(request,'booking.html',{'train':train,'route':route})
@login_required(login_url='/login')
def seat_bookings(request,train,date):
    new=datetime.datetime.strptime(date,'%B %d, %Y')
    train_today =train_charts.objects.get(train__name=train,date=new)
    agents= agent.objects.get(user=request.user)
    formset=formset_factory(passenger_form)
    allowed=agent_booking_allowed.objects.get(agent__user=request.user)
    form=formset()
    lists=train_today.compartment_capacity*6
    train_seat=[]
    for book in range(1,lists+1):
        train_seat.append(book)
    all_seats=booking_id.objects.filter(seat_booking__train=train_today)
    booked=[]
    for j in all_seats:
        booked.append(j.seat_no)
        train_seat.remove(j.seat_no)
    print("Seats Booked:",booked)
    print("seats Avaliable:",train_seat)
    if request.method == "POST":
        seat=seat_booking.objects.create(train=train_today,agent=agents)
        form=formset(request.POST)
        total_forms=int(request.POST['form-TOTAL_FORMS'])
        if total_forms < allowed.allowed: 
            if form.is_valid():
                for forms in form:
                    name=forms.cleaned_data['name']
                    age=forms.cleaned_data['age']
                    gender=forms.cleaned_data['gender']
                    address=forms.cleaned_data['address']
                    phone=forms.cleaned_data['phone']
                    passengers=passenger.objects.create(name=name,age=age,gender=gender,address=address,phone=phone)
                    passengers.save()
                    if total_forms > 1:
                        for i in train_seat:
                            no=i
                            train_seat.remove(i)
                            break
                    elif (age > 60) and (gender=='female' or gender=='male'):
                        for i in train_seat:
                            print(i)
                            if i%6==0 or i%6==1:
                                print("Window Seat Booked",i)
                                no=i
                                train_seat.remove(i)
                                break
                            '''elif i%6==0 or i%6==1 not in train_seat:
                                if i%6==2 or i%6==5:
                                    print("Middle Seat Booked",i)
                                    no=i
                                    break        
                                elif i%6==2 or i%6==5 not in train_seat:
                                    if i%6==3 or i%6==4:
                                        print("Asile Seat Booked",i)
                                        no=i
                                        break'''
                    elif age < 60:
                        for i in train_seat:
                            no=i
                            train_seat.remove(i)
                            break                   
                    
                    booking=booking_id.objects.create(seat_booking=seat,passenger=passengers,seat_no=no)
                    booking.save()
                    train_today.seats=train_today.seats-1
                    train_today.save()
            return redirect("/")
        else:
            return HttpResponse(f"<center><h1>Note :You can book only {allowed.allowed} seats at a time</h1></center>")
    return render(request,'seat_booking.html',{'train':train_today,'form':form,'allowed':allowed})




@login_required(login_url='/login')
def agent_booking_view(request):
    bookings=booking_id.objects.filter(seat_booking__agent__user=request.user)
    return render(request,'agent_booking_view.html',{'booking':bookings})

@login_required(login_url='/login')
def agent_seating_view(request,id):
    
    seats=booking_id.objects.filter(seat_booking__id=id)
    train=seat_booking.objects.get(id=id)
    total_seats =int(train.train.seats)
    return render(request,'agent-seating-view.html',{'seats':seats,'total_seats':range(1,total_seats+1)})


def login_view(request):
    
    if request.method == 'POST':
        username =request.POST.get('uname')
        password=request.POST.get('psw')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            if user.last_login != None:
                login(request,user)
                print("logged in")
                return redirect('/')
            else:
                login(request,user)
                return redirect('/')
 
    return render(request,'login.html')
     
def logout_view(request):
    logout(request)
    return redirect('/login')