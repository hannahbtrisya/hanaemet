from django.contrib import admin

# Register your models here.
from .models import UserProfile, Attraction, TourPackage, Booking, Payment, Review

admin.site.register(UserProfile)
admin.site.register(Attraction)
admin.site.register(TourPackage)
admin.site.register(Booking)
admin.site.register(Payment)
admin.site.register(Review)
