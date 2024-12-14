from django.shortcuts import render, redirect
from .models import Attraction, TourPackage, Booking, Payment, UserProfile, Review
from django.db.models import Q


def home(request):
    return render(request, 'homepage.html')

def user_profile(request):
    if 'username' in request.session:
        user_profile = UserProfile.objects.get(username=request.session['username'])
        return render(request, 'user_profile.html', {'user': user_profile})
    else:
        return redirect('login')
    
def search_results(request):
    query = request.GET.get('q', '')
    
    if query:
        tour_packages = TourPackage.objects.filter(
            Q(name_package__icontains=query) |
            Q(description__icontains=query)
        )

        attractions = Attraction.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(location__icontains=query)
        )
    else:
        tour_packages = TourPackage.objects.none()  
        attractions = Attraction.objects.none()  

    return render(request, 'search_results.html', {
        'query': query,
        'tour_packages': tour_packages,
        'attractions': attractions,
    })

def tour_package_detail(request, package_id):
    try:
        tour_package = TourPackage.objects.get(packageID=package_id)
    except TourPackage.DoesNotExist:
        return render(request, 'error.html', {'message': 'Tour Package not found.'})

    return render(request, 'tourpackage.html', {'tour_package': tour_package})
    
def attraction_detail(request, package_id):
    try:
        tour_package = TourPackage.objects.get(packageID=package_id)
        
        attractions = Attraction.objects.filter(package_type=tour_package)
        
    except TourPackage.DoesNotExist:
        return render(request, 'error.html', {'message': 'Tour Package not found.'})

    return render(request, 'tourpackage.html', {'tour_package': tour_package, 'attractions': attractions})

def update_user_profile(request):
    if 'username' not in request.session:
        return redirect('login')  
    
    user_profile = UserProfile.objects.filter(username=request.session['username']).first()

    if request.method == 'POST':
        user_profile.phone_number = request.POST.get('phone_number')
        user_profile.address = request.POST.get('address')
        user_profile.ic_passport = request.POST.get('ic_passport')
        user_profile.save() 
        return redirect('user_profile')  

    return render(request, 'update_profile.html', {'user_profile': user_profile})

def tour_packages(request):
    packages = TourPackage.objects.all()  
    return render(request, 'tourpackage.html', {'packages': packages})

def adventure_sabah(request):
    return render(request, 'adventure_sabah.html')

def wildlife_sabah(request):
    return render(request, 'wildlife_sabah.html')

def island_getaway(request):
    return render(request, 'island_getaway.html')

def eco_tourism(request):
    return render(request, 'eco_tourism.html')

def nature_retreat(request):
    return render(request, 'nature_retreat.html')

def attractions(request):
    all_attractions = Attraction.objects.select_related('package_type').all()
    return render(request, 'attractions.html', {'attractions': all_attractions})

def booking(request, package_id):
    if 'username' not in request.session:
        return redirect('login') 
    
    try:
        tour_package = TourPackage.objects.get(packageID=package_id)
    except TourPackage.DoesNotExist:
        return render(request, 'error.html', {'message': 'Tour Package not found.'})
    
    if request.method == 'POST':
        number_of_people = request.POST['number_of_people']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        
        user_profile = UserProfile.objects.get(username=request.session['username'])
        
        total_price = tour_package.price * int(number_of_people)

        booking = Booking.objects.create(
            userID=user_profile,
            tour_package=tour_package,
            number_of_people=number_of_people,
            start_date=start_date,
            end_date=end_date,
            total_price=total_price,
            confirmation=False
        )

        return redirect('payment', booking_id=booking.booking_id)

    return render(request, 'booking.html', {'tour_package': tour_package})

def process_booking(request, package_id):
    if request.method == 'POST':
        number_of_people = request.POST['number_of_people']
        date = request.POST['date']

        if 'username' not in request.session:
            return redirect('login')  

        tour_package = TourPackage.objects.get(packageID=package_id)
        user_profile = UserProfile.objects.get(username=request.session['username'])
        total_price = tour_package.price * int(number_of_people)

        booking = Booking.objects.create(
            userID=user_profile,
            tour_package=tour_package,
            number_of_people=number_of_people,
            total_price=total_price,
            confirmation=False
        )

        return redirect('payment', booking_id=booking.booking_id)

def payment(request, booking_id):
    if 'username' not in request.session:
        return redirect('login')  

    try:
        booking = Booking.objects.get(booking_id=booking_id)
    except Booking.DoesNotExist:
        return render(request, 'error.html', {'message': 'Booking not found.'})

    if request.method == 'POST':
        payment_method = request.POST['payment_method']
        card_number = request.POST['card_number'] 

        Payment.objects.create(
            bookingId=booking,
            amount=booking.total_price,
            payment_status='Pending', 
            payment_method=payment_method  
        )

        booking.confirmation = True
        booking.save()

        return render(request, 'receipt.html', {'booking': booking, 'payment_method': payment_method})

    return render(request, 'payment.html', {'booking': booking})
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        ic_passport = request.POST['ic_passport']
        phone_number = request.POST['phone_number']
        address = request.POST['address']

        if UserProfile.objects.filter(ic_passport=ic_passport).exists():
            return render(request, 'register.html', {'error': 'IC/Passport already exists.'})

        UserProfile.objects.create(
            username=username,
            password=password,
            ic_passport=ic_passport,
            phone_number=phone_number,
            address=address
        )

        request.session['username'] = username
        return redirect('user_profile')

    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user_profile = UserProfile.objects.get(username=username)
            if user_profile.password == password:
                request.session['username'] = username
                return redirect('user_profile')
            else:
                return render(request, 'login.html', {'error': 'Invalid password'})
        except UserProfile.DoesNotExist:
            return render(request, 'login.html', {'error': 'Invalid username'})

    return render(request, 'login.html')

def submit_review(request):
    if request.method == 'POST':
        package_id = request.POST['tour_package']
        rating = int(request.POST['rating'])
        comment = request.POST['comment']

        if 'username' not in request.session:
            return redirect('login')  

        tour_package = TourPackage.objects.get(packageID=package_id) 
        user_profile = UserProfile.objects.get(username=request.session['username'])

        Review.objects.create(
            user=user_profile,
            tour_package=tour_package,
            rating=rating,
            comment=comment
        )

        return redirect('submit_review')  

    tour_packages = TourPackage.objects.all()
    reviews = Review.objects.filter(tour_package__isnull=False)  

    return render(request, 'review.html', {'tour_packages': tour_packages, 'reviews': reviews})

def user_bookings(request):
    if 'username' not in request.session:
        return redirect('login')  
    
    user_profile = UserProfile.objects.get(username=request.session['username'])
    bookings = Booking.objects.filter(userID=user_profile)

    return render(request, 'booking_cart.html', {'bookings': bookings})

def update_booking(request, booking_id):
    booking = Booking.objects.get(booking_id=booking_id) 
    if request.method == 'POST':
        number_of_people = request.POST.get('number_of_people')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        booking.number_of_people = number_of_people
        booking.start_date = start_date
        booking.end_date = end_date

        tour_package = booking.tour_package  
        booking.total_price = tour_package.price * int(number_of_people)
        booking.save()  
        return redirect('bookings')  

    return render(request, 'update_booking.html', {'booking': booking})

def delete_booking(request, booking_id):
    Booking.objects.filter(booking_id=booking_id).delete()  
    return redirect('bookings')  

def logout_view(request):
    if 'username' in request.session:
        del request.session['username']  
        return redirect('login') 
    else:
        return redirect('home') 