from django.db import models

class UserProfile(models.Model):
    userID = models.AutoField(primary_key=True)  
    username = models.CharField(max_length=150)  
    password = models.CharField(max_length=128)  
    ic_passport = models.CharField(max_length=50, unique=True)  
    phone_number = models.CharField(max_length=15)  
    address = models.TextField()  

class TourPackage(models.Model):
    packageID = models.AutoField(primary_key=True)  
    name_package = models.CharField(max_length=200)  
    description = models.TextField()  
    price = models.DecimalField(max_digits=10, decimal_places=2) 
    duration = models.CharField(max_length=100)  
    available = models.BooleanField(default=True) 

class Attraction(models.Model):
    name = models.CharField(max_length=200)  
    description = models.TextField()  
    location = models.CharField(max_length=200)  
    package_type = models.ForeignKey('TourPackage', on_delete=models.CASCADE, related_name='attractions')  

class Booking(models.Model):
    userID = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  
    tour_package = models.ForeignKey(TourPackage, on_delete=models.CASCADE, related_name='bookings')  
    booking_date = models.DateTimeField(auto_now_add=True)  
    number_of_people = models.PositiveIntegerField(default=1)  
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  
    confirmation = models.BooleanField(default=False)  
    booking_id = models.AutoField(primary_key=True) 
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)

class Payment(models.Model):
    paymentId = models.AutoField(primary_key=True)  
    bookingId = models.ForeignKey(Booking, on_delete=models.CASCADE)  
    amount = models.DecimalField(max_digits=10, decimal_places=2) 
    payment_date = models.DateTimeField(auto_now_add=True)  
    payment_status = models.CharField(max_length=50, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Failed', 'Failed')])  
    payment_method = models.CharField(max_length=20, default='Credit Card')  
    card_number = models.CharField(null=True,max_length=16)  

class Review(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)  
    rating = models.IntegerField()  
    comment = models.TextField() 
    tour_package = models.ForeignKey(TourPackage, on_delete=models.CASCADE) 
