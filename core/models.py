from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class admin(models.Model):
    user =models.ForeignKey(User, on_delete=models.CASCADE)
    name =models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class agent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email =models.EmailField(max_length=254)
    profile =models.ImageField(upload_to='')
    dob = models.DateField(auto_now_add=False)
    address=models.TextField()
    phone=models.IntegerField()

    def __str__(self):
        return self.name

class agent_booking_allowed(models.Model):
    agent=models.ForeignKey(agent,on_delete=models.CASCADE)
    allowed=models.IntegerField()

    def __str__(self):
        return str(self.agent)+"-"+str(self.allowed) 
    
class trains(models.Model):
    name=models.CharField(max_length=50)
    depature =models.CharField(max_length=50,null=True)
    arrival = models.CharField(max_length=50,null=True)
    time=models.TimeField(auto_now=False,null=True)

    def __str__(self):
        return self.name

    def total_seats(self):
        return self.compartment_capacity * 6

class train_charts(models.Model):
    train=models.ForeignKey(trains, on_delete=models.CASCADE)
    compartment_capacity=models.IntegerField()
    seats=models.IntegerField()
    date=models.DateField(auto_now=False)

    def __str__(self):
        return str(self.train)+str(self.date)
    
class passenger(models.Model):
    name = models.CharField(max_length=50)
    age= models.IntegerField()
    gender = models.CharField(max_length=50)
    address=models.TextField()
    phone=models.IntegerField()

    def __str__(self):
        return self.name

    

class seat_booking(models.Model):
    train =models.ForeignKey(train_charts,on_delete=models.CASCADE,null=True)
    agent=models.ForeignKey(agent, on_delete=models.CASCADE)
    date =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Train Name:"+str(self.train) +"\nPassenger Name: "+ str(self.id)
   
class booking_id(models.Model):
    seat_booking=models.ForeignKey(seat_booking, on_delete=models.CASCADE)
    passenger = models.ForeignKey(passenger, on_delete=models.CASCADE)
    seat_no=models.IntegerField(null=True)

    def __str__(self):
        return str(self.seat_booking)
    
