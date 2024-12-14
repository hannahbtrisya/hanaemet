from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page
    path('profile/', views.user_profile, name='user_profile'),  # User profile
    path('register/', views.register, name='register'),  # Register page
    path('login/', views.login_view, name='login'),  # Login page
    path('attractions/', views.attractions, name='attractions'),  # Attractions page
    path('attraction/<int:package_id>/', views.attraction_detail, name='attraction_detail'),
    path('tourpackages/', views.tour_packages, name='tourpackages'),  # Tour Packages page
    path('tourpackage/<int:package_id>/', views.tour_package_detail, name='tour_package_detail'),
    path('booking/<int:package_id>/', views.booking, name='booking'),  # Booking page for a specific package
    path('process-booking/<int:package_id>/', views.process_booking, name='process_booking'),  # Booking process
    path('payment/<int:booking_id>/', views.payment, name='payment'),  # Payment page
    path('review/', views.submit_review, name='submit_review'),
    path('profile/update/', views.update_user_profile, name='update_user_profile'),
    path('bookings/', views.user_bookings, name='bookings'),
    path('bookings/update/<int:booking_id>/', views.update_booking, name='update_booking'),
    path('bookings/delete/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('search/', views.search_results, name='search_results'),
    path('logout/', views.logout_view, name='logout'),
    path('tourpackages/adventure-sabah/', views.adventure_sabah, name='adventure_sabah'),
    path('tourpackages/wildlife-sabah/', views.wildlife_sabah, name='wildlife_sabah'),
    path('tourpackages/island-getaway/', views.island_getaway, name='island_getaway'), 
    path('tourpackages/eco-tourism/', views.eco_tourism, name='eco_tourism'), 
    path('tourpackages/nature-retreat/', views.nature_retreat, name='nature_retreat'),

]



