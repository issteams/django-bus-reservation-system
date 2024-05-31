from django.shortcuts import render, redirect, get_object_or_404
from .models import BusRoute, Schedule, Ticket, Payment, Student
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from datetime import datetime
import stripe 

stripe.api_key = settings.STRIPE_SECRET_KEY


def student_home(request):
    return render(request, "student_templates/student_home.html", {})

def make_reservation(request):
    routes = BusRoute.objects.all()
    return render(request, "student_templates/make_reservation.html", {
        "routes": routes,
    })

def bus_schedules(request):
    schedules = Schedule.objects.all()
    return render(request, "student_templates/schedules.html", {
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
                return render(request, "student_templates/search_result.html", {
                    "message": "Invalid date format. Please use YYYY-MM-DD."
                })

            # Find routes that match the origin and destination
            routes = BusRoute.objects.filter(Q(origin__iexact=origin) & Q(destination__iexact=destination))

            # Find schedules that match the routes and the given date
            schedules = Schedule.objects.filter(route__in=routes, departure_time__date=travel_date)

            if schedules.exists():
                return render(request, "student_templates/search_result.html", {
                    "schedules": schedules,
                    "date": date,
                })
            else:
                return render(request, "student_templates/search_result.html", {
                    "message": "No Result",
                })
        else:
            return render(request, "student_templates/search_result.html", {
                "message": "Please provide origin, destination, and date."
            })
    else:
        return render(request, "student_templates/search_result.html", {
            "message": "Invalid request method."
        })


def book_seat(request, schedule_id):
    # Retrieve the schedule or return a 404 error if not found
    schedule = get_object_or_404(Schedule, id=schedule_id)
    
    # Create a list of available seats based on the capacity of the bus
    seats = [seat for seat in range(1, schedule.bus.capacity + 1)]
    
    return render(request, "student_templates/book_seat.html", {
        "schedule": schedule,
        "seats": seats,
    })
       
@login_required
def get_book_seat(request, schedule_id):
    if request.method == 'POST':
        seat_number = request.POST.get('seat_number')
        user = request.user.id
        try:
            student = Student.objects.get(admin=user)
        except Student.DoesNotExist:
            # Handle the case where the student doesn't exist
            messages.error(request, "Student not found")
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

        # Create a new ticket for the student
        ticket = Ticket.objects.create(student=student, schedule=schedule, seat_number=seat_number, status="pending")
        messages.success(request, "Seat booked successfully")
        return redirect("make_payment", schedule_id)

    else:
        # Handle GET request if needed
        pass


@login_required
def make_payment(request, schedule_id):
    if request.method == 'POST':
        seat_number = request.POST.get('seat_number')
        amount = request.POST.get('amount')
        user = request.user

        try:
            schedule = Schedule.objects.get(id=schedule_id)
            student = Student.objects.get(admin=user)

            if Ticket.objects.filter(schedule=schedule, seat_number=seat_number).exists():
                messages.error(request, "Seat Already Booked")
                return redirect('book_seat', schedule_id)

            # Create a Stripe Checkout session
            try:
                session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=[{
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': f'Ticket for {schedule.route.origin} to {schedule.route.destination}',
                            },
                            'unit_amount': int(amount) * 100,  # Stripe requires amount in cents
                        },
                        'quantity': 1,
                    }],
                    mode='payment',
                    success_url=request.build_absolute_uri('/payment/success/'),
                    cancel_url=request.build_absolute_uri('/payment/cancel/'),
                )

                # Create a pending ticket
                ticket = Ticket.objects.create(
                    student=student,
                    schedule=schedule,
                    seat_number=seat_number,
                    status="pending",
                    payment_reference=session.id
                )

                return redirect(session.url)
            except stripe.error.StripeError as e:
                messages.error(request, f"Payment initialization failed: {e.error.message}")
                return redirect('make_payment', schedule_id)

        except Schedule.DoesNotExist:
            return HttpResponse("Schedule Not Found")
        except Student.DoesNotExist:
            return HttpResponse("Student Not Found")
    else:
        schedule = get_object_or_404(Schedule, id=schedule_id)
        seat_number = request.GET.get('seat_number', 'Unknown')
        amount = 10000

        return render(request, "student_templates/payment.html", {
            "schedule": schedule,
            "amount": amount,
            "seat_number": seat_number,
            "stripe_public_key": settings.STRIPE_PUBLIC_KEY
        })


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




    
        

