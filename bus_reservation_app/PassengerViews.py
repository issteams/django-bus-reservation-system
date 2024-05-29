from django.shortcuts import render, redirect, get_object_or_404
from .models import BusRoute, Schedule, Ticket, Payment, Passenger
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from datetime import datetime
import paystack
# from paystack.transaction import Transaction



def passenger_home(request):
    return render(request, "passenger_templates/passenger_home.html", {})

def make_reservation(request):
    return render(request, "passenger_templates/make_reservation.html", {})

def bus_schedules(request):
    schedules = Schedule.objects.all()
    return render(request, "passenger_templates/schedules.html", {
        "schedules": schedules,
    })

@login_required
def search_result(request):
    if request.method == "GET":
        origin = request.GET.get('origin')
        destination = request.GET.get('destination')
        date = request.GET.get('date')

        if origin and destination and date:
            # Parse the date string into a datetime object
            try:
                travel_date = datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                return render(request, "passenger_templates/search_result.html", {
                    "message": "Invalid date format. Please use YYYY-MM-DD."
                })

            # Find routes that match the origin and destination
            routes = BusRoute.objects.filter(Q(origin__iexact=origin) & Q(destination__iexact=destination))

            # Find schedules that match the routes and the given date
            schedules = Schedule.objects.filter(route__in=routes, departure_time__date=travel_date)

            if schedules.exists():
                return render(request, "passenger_templates/search_result.html", {
                    "schedules": schedules,
                    "date": date,
                })
            else:
                return render(request, "passenger_templates/search_result.html", {
                    "message": "No Result",
                })
        else:
            return render(request, "passenger_templates/search_result.html", {
                "message": "Please provide origin, destination, and date."
            })
    else:
        return render(request, "passenger_templates/search_result.html", {
            "message": "Invalid request method."
        })


def book_seat(request, schedule_id):
    # Retrieve the schedule or return a 404 error if not found
    schedule = get_object_or_404(Schedule, id=schedule_id)
    
    # Create a list of available seats based on the capacity of the bus
    seats = [seat for seat in range(1, schedule.bus.capacity + 1)]
    
    return render(request, "passenger_templates/book_seat.html", {
        "schedule": schedule,
        "seats": seats,
    })
       
@login_required
def get_book_seat(request, schedule_id):
    if request.method == 'POST':
        seat_number = request.POST.get('seat_number')
        user = request.user.id
        try:
            passenger = Passenger.objects.get(admin=user)
        except Passenger.DoesNotExist:
            # Handle the case where the passenger doesn't exist
            messages.error(request, "Passenger not found")
            return redirect("book_seat", schedule_id)

        try:
            schedule = Schedule.objects.get(id=schedule_id)
        except Schedule.DoesNotExist:
            # Handle the case where the schedule doesn't exist
            return HttpResponse("Schedule not found")

        # Check if the seat is already booked
        if Ticket.objects.filter(schedule=schedule, seat_number=seat_number).exists():
            messages.error(request, "Seat already booked")
            return redirect("book_seat", schedule_id)

        # Create a new ticket for the passenger
        Ticket.objects.create(passenger=passenger, schedule=schedule, seat_number=seat_number, status="pending")
        messages.success(request, "Seat booked successfully")
        return redirect("make_payment", schedule_id)

    else:
        # Handle GET request if needed
        pass


def make_payment(request, schedule_id):
    if request.method == 'POST':
        # Get payment details from the form
        card_number = request.POST.get('card_number')
        expiry_date = request.POST.get('expiry_date')
        cvv = request.POST.get('cvv')
        amount = request.POST.get('amount')

        # Initialize Paystack API
        paystack_secret_key = 'your_paystack_secret_key'
        paystack_api = paystack.SecretKey(paystack_secret_key)

        # Create a Paystack transaction
        try:
            transaction = Transaction.initialize(
                amount=amount,
                email=request.user.email,  # Assuming user is logged in
                reference='your_transaction_reference'
            )
            # Redirect to Paystack payment page
            return redirect(transaction['data']['authorization_url'])
        except Exception as e:
            messages.error(request, f"Payment failed: {e}")
            return redirect('make_payment', schedule_id)

    # If request method is GET, render the payment template
    schedule = Schedule.objects.get(id=schedule_id)
    return render(request, "passenger_templates/payment.html", {"schedule": schedule})

@login_required
def comfirm_payment(request, payment_id):
    if request.method == 'POST':
        try:
            payment = Payment.objects.get(pk=payment_id)
            payment.payment_status = 'Paid'
            payment.save()

            Ticket.objects.filter(payment=payment).update(status="comfirmed")
            return HttpResponse("Payment Comfirmed")
        except Payment.DoesNotExist:
            return HttpResponse("Not Found")




    
        

